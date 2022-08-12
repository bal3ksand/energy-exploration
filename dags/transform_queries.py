import os

PROJECT_ID = os.getenv("GCP_PROJECT")
DATASET_NAME = os.getenv("BQ_DATASET_WH")

CLEANED_TABLE_NAME = os.getenv("CLEANED_TABLE_NAME", default="raw_formatted")
FACT_TABLE_NAME = os.getenv("FACT_TABLE_NAME", default="facts")

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
        "(SELECT Date, Value, REGEXP_REPLACE(CONCAT(DESCRIPTION, '_', UNIT), r'([ (),-.])', '_') AS Element FROM `{PROJECT_ID}.{DATASET_NAME}.{CLEANED_TABLE_NAME}`) ",
        "PIVOT(MAX(Value) FOR Element IN (",
        (SELECT STRING_AGG(DISTINCT CONCAT("'", REGEXP_REPLACE(CONCAT(DESCRIPTION, '_', UNIT), r'([ (),-.])', '_'), "'")) FROM `{PROJECT_ID}.{DATASET_NAME}.{CLEANED_TABLE_NAME}`),
        "))",
        "ORDER BY Date",
        ")"
      )
  """
  
}