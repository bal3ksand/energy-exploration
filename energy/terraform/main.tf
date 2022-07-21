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

# https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-terraform
resource "google_storage_bucket" "bucket" {
  name          = var.bucket_name
  location      = var.region
  project       = var.project_id
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  project    = var.project_id
  location   = var.region
  default_table_expiration_ms = 1000*60*60*24*60 - 1    # 60 days - 1 ms
}