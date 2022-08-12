from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import datetime
import os

from google.cloud import storage


# https://www.eia.gov/totalenergy/data/monthly/index.php

data_sources = (
    ("primary-energy-overview", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T01.01"),
    ("primary-energy-production-by-source", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T01.02"),
    ("primary-energy-consumption-by-source", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T01.03"),
    ("energy-consumption-expenditures-co2", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T01.07"),
    ("consumption-residential-commercial-industrial", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T02.01A"),
    ("consumption-transportation-enduse-electricpower","https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T02.01B"),
    ("govt-consumption-by-agency", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T02.07"),
    ("crude-oil-price", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T09.01"),
    ("avg-electricity-price", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T09.08"),
    ("natural-gas-prices", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T09.10"),
    ("co2-emissions-by-source", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T11.01"),
)

BUCKET_NAME = os.getenv(GCS_BUCKET_LAKE)

# https://cloud.google.com/composer/docs/composer-2/cloud-storage
GCS_DATA_DIR = "/home/airflow/gcs/data"


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    # https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-code-sample
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


with DAG(
    dag_id="ingest_data_dag",
    schedule_interval="@monthly",
    start_date=datetime(2022, 7, 1, 0, 0),
    catchup=True
) as dag:
    
    for filename, url in data_sources:
    
        download_csv_task = BashOperator(
            task_id=f"download_{filename}",
            bash_command=f"curl -sSLf {url} > {GCS_DATA_DIR}/{filename}.csv"
        )
        
        upload_to_gcs_task = PythonOperator(
            task_id=f"{filename}_to_gcs",
            python_callable=upload_blob,
            op_kwargs={
                'bucket_name': BUCKET_NAME,
                'source_file_name': f"{GCS_DATA_DIR}/{filename}.csv",
                'destination_blob_name': f"dump/{filename}.csv"
            }
        )
        
        delete_csv_task = BashOperator(
            task_id=f"remove_{filename}.csv",
            bash_command=f"rm {GCS_DATA_DIR}/{filename}.csv"
        )

        download_csv_task >> upload_to_gcs_task >> delete_csv_task
