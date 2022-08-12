from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from google.cloud import storage

import os
from datetime import datetime, timedelta

from data_source import data_sources


BUCKET_NAME = os.getenv("GCS_BUCKET_LAKE")

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
    schedule_interval="0 4 1 * *",
    # start on the first day of the previous month: first of the month minus number of days in prev month.
    # all historical data is included in every download.
    start_date=(datetime.now().replace(day=1) - timedelta(days=(datetime.today().replace(day=1) - timedelta(days=1)).day)).replace(hour=0),
    catchup=True
) as dag:

    trigger_transform_dag = TriggerDagRunOperator(
        task_id="trigger_transform_dag",
        trigger_dag_id="transform_data_dag",
        reset_dag_run=True
    )
    
    delete_temp_csvs = BashOperator(
        task_id="delete_temp_csvs",
        bash_command=f"rm {GCS_DATA_DIR}/*"
    )
    
    for filename, url in data_sources:
    
        download_csv = BashOperator(
            task_id=f"download_{filename}",
            bash_command=f"curl -sSLf {url} > {GCS_DATA_DIR}/{filename}.csv"
        )
        
        upload_to_gcs = PythonOperator(
            task_id=f"{filename}_to_gcs",
            python_callable=upload_blob,
            op_kwargs={
                'bucket_name': BUCKET_NAME,
                'source_file_name': f"{GCS_DATA_DIR}/{filename}.csv",
                'destination_blob_name': f"dump/{filename}.csv"
            }
        )

        download_csv >> upload_to_gcs >> delete_temp_csvs >> trigger_transform_dag
