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
    ("co2-emissions-by-source", "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T11.01")
)

schema = [
    {"name": "MSN", "type": "STRING", "mode": "NULLABLE"},
    {"name": "YYYYMM", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "Value", "type": "STRING", "mode": "NULLABLE"},  # note
    {"name": "Column_Order", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "Description", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Unit", "type": "STRING", "mode": "NULLABLE"}
]