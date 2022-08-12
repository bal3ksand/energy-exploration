from airflow import DAG
# https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html#execute-bigquery-jobs
# https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html#create-external-table
# https://www.google.com/search?q=gcs_to_bq
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator

from datetime import datetime, timedelta
import os

from data_source import schema
from transform_queries import QUERIES


LOCATION_NAME = os.getenv("BQ_DATASET_LOCATION", default=os.getenv("COMPOSER_LOCATION"))
BUCKET_NAME = os.getenv("GCS_BUCKET_LAKE")
DATASET_NAME = os.getenv("BQ_DATASET_WH")


with DAG(
    dag_id="transform_data_dag",
    schedule_interval=None,
    start_date=(datetime.now().replace(day=1) - timedelta(days=(datetime.today().replace(day=1) - timedelta(days=1)).day)).replace(hour=0)
) as dag:

    # create raw external table
    create_raw_table = BigQueryCreateExternalTableOperator(
        task_id="create_raw_table",
        destination_project_dataset_table=f"{DATASET_NAME}.raw",
        bucket=BUCKET_NAME,
        source_objects=["dump/*"],
        schema_fields=schema,
        skip_leading_rows=1
    )
    
    # job - create cleaned table from raw
    create_clean_table = BigQueryInsertJobOperator(
        task_id="create_clean_table",
        configuration={
            "query": {
                "query": QUERIES["clean"],
                "useLegacySql": False
            }
        },
        location=LOCATION_NAME
    )
    
    # job - create pivot table from cleaned
    create_fact_table = BigQueryInsertJobOperator(
        task_id="create_fact_table",
        configuration={
            "query": {
                "query": QUERIES["pivot"],
                "useLegacySql": False
            }
        },
        location=LOCATION_NAME
    )
    
    create_raw_table >> create_clean_table >> create_fact_table