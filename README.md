## Description
I seek to analyze United States energy data. There are dimensions and breakdowns such as total energy production and emissions. [I discovered that around 2012, energy production started to rise, while emissions stayed roughly the same (except for a drop when the COVID-19 pandemic began). The percent increase in energy production vastly outweighs the decrease in share of fossil fuel energy production](data-viz.pdf).

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
	- Edit [variables.tf](terraform/variables.tf)
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
	- In BigQuery, grant the 
	
    - Upload the [Ingestion DAG](dags/gcs_ingestion.py) using the following script:
        - `gcloud composer environments storage dags import --environment ENVIRONMENT_NAME --location LOCATION --source="LOCAL_FILE_TO_UPLOAD"`
     - The Ingestion DAG will automatically run and load all files into your [GCS](https://console.cloud.google.com/storage)  bucket. Go to the [GCC Environments Page](https://console.cloud.google.com/composer/), choose your GCC Environment, and open the Airflow UI to check the status of your DAG.

- [BigQuery](https://console.cloud.google.com/bigquery) - Transformations
	- Using the UI, create a table named "raw" for the raw data
		- Table Type - Native
		- Manually Choose the Schema as [shown on the bottom of this page](#raw-table-schema)
		- Individually run each query in [queries](queries) to transform the data (copy/paste them into the BigQuery SQL editor)

- [Data Studio](https://datastudio.google.com/)
	- Line Graph: Total Primary Energy Production vs Total Energy CO2 Emissions
	- Pie Chart: Share of energy production by type

### Raw Table Schema
|Field Name|Type|Mode|
|--|--|--|
|MSN|STRING|NULLABLE|
|YYYYMM|INTEGER|NULLABLE|
|Value|STRING*|NULLABLE|
|Column_Order|INTEGER|NULLABLE|
|Description|STRING|NULLABLE|
|Unit|STRING|NULLABLE|