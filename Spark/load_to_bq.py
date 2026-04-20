import glob
from google.cloud import bigquery

client = bigquery.Client()

# Define table
table_id = "bamboo-depth-486215-u4.weather_analytics.weather_processed"

# Load data from Parquet files in local folder
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition="WRITE_TRUNCATE",

    # ✅ THIS makes it reproducible
    time_partitioning=bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="date"
    )
)

files = glob.glob("weather_processed/**/*.parquet", recursive=True)

for file in files:
    with open(file, "rb") as f:
        job = client.load_table_from_file(
            f,
            table_id,
            job_config=job_config
        )
        job.result()

print("✅ Loaded all files")