CREATE OR REPLACE TABLE `energy-356822.energy_dataset.f_null_values` AS (
  SELECT * EXCEPT(Value),
    SAFE_CAST(Value AS FLOAT64) AS Value
  FROM (
    SELECT * EXCEPT(Value),
      CASE WHEN Value = 'Not Available' THEN NULL
      ELSE Value END AS Value
    FROM `energy-356822.energy_dataset.raw`
  )
)