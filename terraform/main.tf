# https://medium.com/rockedscience/how-to-fully-automate-the-deployment-of-google-cloud-platform-projects-with-terraform-16c33f1fb31f

terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {}
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_project" "energy_project" {
  name                = var.project_name
  project_id          = var.project_id
  billing_account     = var.billing_account_id
  auto_create_network = true
}

data "google_project" "project" {
  depends_on = [google_project.energy_project]
}

resource "null_resource" "enable_service_usage_api" {
  provisioner "local-exec" {
    command = "gcloud services enable serviceusage.googleapis.com cloudresourcemanager.googleapis.com --project ${var.project_id}"
  }

  depends_on = [google_project.energy_project]
}

resource "time_sleep" "enable_service_usage_api_wait" {
  create_duration = "60s"

  depends_on = [null_resource.enable_service_usage_api]
}

resource "google_project_service" "enable_service_apis" {
  for_each           = toset(var.services)
  
  project            = var.project_id
  service            = each.key
  disable_on_destroy = false
  
  depends_on = [time_sleep.enable_service_usage_api_wait]
}

resource "time_sleep" "enable_service_apis_wait" {
  create_duration = "60s"

  depends_on = [google_project_service.enable_service_apis]
}

# https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-terraform
resource "google_storage_bucket" "datalake" {
  name          = var.bucket_name
  location      = var.region
  project       = var.project_id
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  
  depends_on = [time_sleep.enable_service_apis_wait]
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "datawarehouse" {
  dataset_id = var.bq_dataset_name
  project    = var.project_id
  location   = var.region
  
  depends_on = [time_sleep.enable_service_apis_wait]
}

resource "google_project_iam_member" "composer_service_agent_role" {
  project = var.project_id
  member  = "serviceAccount:service-${data.google_project.project.number}@cloudcomposer-accounts.iam.gserviceaccount.com"
  # service acct on create env ui: ${var.project_number}-compute@developer.gserviceaccount.com
  role    = "roles/composer.ServiceAgentV2Ext"
  
  depends_on = [time_sleep.enable_service_apis_wait]
}

resource "google_composer_environment" "composer_environment" {
  name             = var.gcc_env_name
  region           = var.region
  project          = var.project_id

  config {
    // Add your environment configuration here
    software_config {
      image_version = "composer-2.0.22-airflow-2.2.5"
      env_variables = {
        BQ_DATASET_WH    = var.bq_dataset_name
        GCS_BUCKET_LAKE = var.bucket_name
      }
    }
    environment_size = "ENVIRONMENT_SIZE_SMALL"
  }
  
  depends_on = [google_project_iam_member.composer_service_agent_role]
}

resource "time_sleep" "create_composer_env_wait" {
  create_duration = "60s"

  depends_on = [google_composer_environment.composer_environment]
}

resource "null_resource" "upload_dags" {
  provisioner "local-exec" {
    command     = <<EOF
gcloud composer environments storage dags import --project ${var.project_id} --environment ${var.gcc_env_name} --location ${var.region} --source="data_source.py"    \
&& gcloud composer environments storage dags import --project ${var.project_id} --environment ${var.gcc_env_name} --location ${var.region} --source="transform_queries.py"    \
&& gcloud composer environments storage dags import --project ${var.project_id} --environment ${var.gcc_env_name} --location ${var.region} --source="bq_transform_dag.py"    \
&& gcloud composer environments storage dags import --project ${var.project_id} --environment ${var.gcc_env_name} --location ${var.region} --source="gcs_ingestion_dag.py"    \
EOF
    working_dir = var.local_dag_dir
  }

  depends_on = [time_sleep.create_composer_env_wait]
}

