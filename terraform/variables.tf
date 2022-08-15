variable "project_name" {
    description = "Name your GCP Project."
    default     = ""
}

variable "project_id" {
    description = "Globally unique GCP Project ID. Allowed characters here: https://cloud.google.com/resource-manager/docs/creating-managing-projects#before_you_begin"
    default     = ""
}

variable "billing_account_id" {
    description = "Billing account ID for this project"
    default     = ""
}

variable services {
  type        = list
  default     = [
    "bigquery.googleapis.com",
    "composer.googleapis.com",
    "storage.googleapis.com"
  ]
}

variable "region" {
    description = "Region for GCP resources. Locations: https://cloud.google.com/about/locations"
    default     = ""
    type        = string
}

variable "bucket_name" {
    description = "Globally Unique GCP Bucket Name of the Data Lake"
    default     = ""
}

variable "bq_dataset_name" {
    description = "BigQuery Dataset Name"
    default     = ""
}

variable "gcc_env_name" {
    description = "Cloud Composer Environment Name"
    default     = ""
}

variable "local_dag_dir" {
    description = "Absolute path to local directory containing the DAGs"
    default     = ""
}