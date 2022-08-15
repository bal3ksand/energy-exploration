## Description
**[climate inaction.](visualizations/consumption-emission.pdf)**

## Technology
![pipeline](visualizations/pipeline.png)
- [Terraform](https://www.terraform.io/)
- Google Cloud Platform
	- [Cloud Composer 2](https://cloud.google.com/composer)
	- [Cloud Storage](https://cloud.google.com/storage/)
	- [BigQuery](https://cloud.google.com/bigquery/)
	- [Data Studio](https://cloud.google.com/datastudio/)

## Instructions
- Clone this repo locally
- Google Cloud Platform Setup
    - Create a GCP account.
    - Create a project with **billing enabled**.
    - Install [gcloud cli](https://cloud.google.com/sdk/docs/install) for your OS.
    - Run `gcloud auth application-default login`

- Terraform
    - Terraform will set up the entire environment and upload the DAGs to Cloud Composer.
	- [Install Terraform](https://www.terraform.io/downloads).
	- Edit [variables.tf](terraform/variables.tf):
		- Enter your billing account and region.
		- Choose a name for the default value of all other variables.
		- Do not change the "services" variable.
	- Run `terraform apply` in the [terraform](terraform) directory.
    
- Cloud Composer
    - Check out the Airflow UI:
        - Go to the [GCC Environments Page](https://console.cloud.google.com/composer/), choose your GCC Environment, and open the Airflow UI.
        - The DAGs automatically run once when uploaded (here, on `terraform apply`), and are scheduled to run on the 1st of every month at 4AM.

- [Data Studio](https://datastudio.google.com/) -- [visualization](visualizations/consumption-emission.pdf)
