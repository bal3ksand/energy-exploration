from airflow import DAG
# https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html#execute-bigquery-jobs
# https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html#create-external-table
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator, BigQueryInsertJobOperator

import datetime
import os

PROJECT_ID = os.getenv(GCP_PROJECT)
LOCATION_NAME = os.getenv(BQ_DATASET_LOCATION, default=os.getenv(COMPOSER_LOCATION))
BUCKET_NAME = os.getenv(GCS_BUCKET_LAKE)
DATASET_NAME = os.getenv(BQ_DATASET_WH)

CLEANED_TABLE_NAME = "raw_formatted"
FACT_TABLE_NAME = "facts"

QUERIES = {

  "clean" : 
  f"""
  CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_NAME}.{CLEANED_TABLE_NAME}` AS (
    SELECT PARSE_DATE('%Y%m', CAST(YYYYMM AS STRING)) AS Date,
      * EXCEPT(YYYYMM)  
    FROM (
      SELECT *
      FROM (
        SELECT * EXCEPT(Value),
          SAFE_CAST(Value AS FLOAT64) AS Value
        FROM (
          SELECT * EXCEPT(Value),
            CASE WHEN Value = 'Not Available' THEN NULL
            ELSE Value END AS Value
          FROM `{PROJECT_ID}.{DATASET_NAME}.raw`
        )
      )
      WHERE CAST(YYYYMM AS STRING) NOT LIKE "____13%"
    )
    ORDER BY Date
  )
  """,
  
  "pivot" :
  f"""
    EXECUTE IMMEDIATE
      CONCAT(
        "CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_NAME}.{FACT_TABLE_NAME}` AS (",
        "SELECT * FROM ",
        "(SELECT Date, Value, REGEXP_REPLACE(CONCAT(DESCRIPTION, '_', UNIT), r'([ (),-.])', '_') AS Element FROM `{PROJECT_ID}.{DATASET}.{CLEANED_TABLE_NAME}`) ",
        "PIVOT(MAX(Value) FOR Element IN (",
        (SELECT STRING_AGG(DISTINCT CONCAT("'", REGEXP_REPLACE(CONCAT(DESCRIPTION, '_', UNIT), r'([ (),-.])', '_'), "'")) FROM `{PROJECT_ID}.{DATASET}.{CLEANED_TABLE_NAME}`),
        "))",
        "ORDER BY Date",
        ")"
      )
  """
  
}


with DAG(
    dag_id="ingest_data_dag",
    schedule_interval="@monthly",
    start_date=datetime(2022, 7, 1, 0, 30),
    catchup=True
) as dag:

    # create raw external table
    create_raw_table = BigQueryCreateEmptyTableOperator(
        task_id="create_raw_table",
        destination_project_dataset_table=f"{DATASET_NAME}.raw",
        bucket=BUCKET_NAME,
        source_objects=[f"gs://{BUCKET_NAME}/dump/*"],    ################# ????
        schema_fields=[
            {"name": "MSN", "type": "STRING", "mode": "NULLABLE"},
            {"name": "YYYYMM", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "Value", "type": "STRING", "mode": "NULLABLE"},
            {"name": "Column_Order", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "Description", "type": "STRING", "mode": "NULLABLE"},
            {"name": "Unit", "type": "STRING", "mode": "NULLABLE"}
        ]
    )
    
    # job - create cleaned table from raw
    clean_table = BigQueryInsertJobOperator(
        task_id="clean_table",
        configuration={
            "query": {
                "query": QUERIES["clean"],
                "useLegacySql": False
            }
        },
        location=LOCATION_NAME
    )
    
    # job - create pivot table from cleaned
    pivot_table = BigQueryInsertJobOperator(
        task_id="pivot_table",
        configuration={
            "query": {
                "query": QUERIES["pivot"],
                "useLegacySql": False
            }
        },
        location=LOCATION_NAME
    )
    
    create_raw_table >> clean_table >> pivot_table