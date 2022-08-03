EXECUTE IMMEDIATE
  CONCAT(
    "CREATE OR REPLACE TABLE `energy-356822.energy_dataset.facts` AS (",
    "SELECT * FROM ",
    "(SELECT Date, Value, REGEXP_REPLACE(CONCAT(DESCRIPTION, '_', UNIT), r'([ (),-.])', '_') AS Element FROM `energy-356822.energy_dataset.date_formatted_monthly`) ",
    "PIVOT(MAX(Value) FOR Element IN (",
    (SELECT STRING_AGG(DISTINCT CONCAT("'", REGEXP_REPLACE(CONCAT(DESCRIPTION, '_', UNIT), r'([ (),-.])', '_'), "'")) FROM `energy-356822.energy_dataset.date_formatted_monthly`),
    "))",
    "ORDER BY Date",
    ")"
  )