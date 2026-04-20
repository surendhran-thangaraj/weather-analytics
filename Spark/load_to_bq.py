import os
import glob
from google.cloud import bigquery
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()

# Read config
project_id = os.getenv("GCP_PROJECT_ID")
dataset = os.getenv("BQ_DATASET")

if not project_id or not dataset:
    raise ValueError("Missing environment variables: GCP_PROJECT_ID or BQ_DATASET")

client = bigquery.Client()

# Build table id dynamically
table_id = f"{project_id}.{dataset}.weather_processed"

# Load data from Parquet files in local folder
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition="WRITE_APPEND",

    # THIS makes it reproducible
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

print("Loaded all files")