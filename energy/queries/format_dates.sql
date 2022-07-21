CREATE OR REPLACE TABLE `energy-356822.energy_dataset.date_formatted_monthly` AS (
  SELECT PARSE_DATE('%Y%m', CAST(YYYYMM AS STRING)) AS Date,
    * EXCEPT(YYYYMM)  
  FROM (
    SELECT *
    FROM `energy-356822.energy_dataset.f_null_values`
    WHERE CAST(YYYYMM AS STRING) NOT LIKE "____13%"
  )
  ORDER BY Date
)