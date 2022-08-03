variable "project_id" {
    description = "Your GCP Project ID"
    default = "energy-356822"
}

variable "region" {
    description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
    default = "us-east4"
    type = string
}

variable "bucket_name" {
    description = "GCP Bucket Name"
    default = "energy-b"
}

variable "bq_dataset_name" {
    description = "BigQuery Dataset Name"
    default = "energy_dataset"
}