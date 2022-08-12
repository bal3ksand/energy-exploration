## Description
**climate inaction.**

## Technology
- Google Cloud Platform
	- Cloud Composer 2 (Airflow)
	- Cloud Storage
	- BigQuery
	- Data Studio
- Terraform

## Instructions
- Clone this repo locally
- Google Cloud Platform Setup
    - Create a GCP account
    - Create a project with **billing enabled**
    - Install [gcloud cli](https://cloud.google.com/sdk/docs/install) for your OS
    - Run `gcloud auth application-default login`

- Terraform
	- [Install](https://www.terraform.io/downloads)
	- Edit [variables.tf](terraform/variables.tf):
		- Enter your project ID and region
		- Choose a name for your bucket and dataset
	- Run `terraform apply` in the [terraform](terraform) directory
    
- Cloud Composer
    - Setup
	    - Just use the console, the account permissions give lots of trouble otherwise.
	    - Before you begin: [Enable the GCC API](https://console.cloud.google.com/flows/enableapi?apiid=composer.googleapis.com)
	- Create environment
	    - [Only Step 1 is required.](https://cloud.google.com/composer/docs/composer-2/create-environments#step_basic_setup)
	    - When you create the first environment in your project, a **Grant required permissions to Cloud Composer service account** section appears on the environment creation page. Follow the guidance in this section to grant required permissions to the Cloud Composer service account.    
	    - Use the same location as in [variables.tf](terraform/variables.tf). If you use a different location, set the vollowing environment variable:
	        - name: "BQ_DATASET_LOCATION", value: the location in [variables.tf](terraform/variables.tf)
	    - Add the following environment variables:
	        - name: "BQ_DATASET_WH", value: the dataset name in [variables.tf](terraform/variables.tf)
	        - name: "GCS_BUCKET_LAKE", value: the bucket name in [variables.tf](terraform/variables.tf)
    - Upload the [DAGs](dags) using the following script:
        - `gcloud composer environments storage dags import --environment ENVIRONMENT_NAME --location LOCATION --source="LOCAL_FILE_TO_UPLOAD"`
    - Check out the Airflow UI
        - Go to the [GCC Environments Page](https://console.cloud.google.com/composer/), choose your GCC Environment, and open the Airflow UI.
        - The DAGs run once when uploaded, and are scheduled to run on the 1st of every month at 4AM.

- [Data Studio](https://datastudio.google.com/) -- [visualization](data-viz.pdf)
