import os
import pandas as pd
from download_kaggle import download_kaggle_dataset
from dotenv import load_dotenv
from google.cloud import bigquery

# Load variables from .env
load_dotenv()

# Read config
project_id = os.getenv("GCP_PROJECT_ID")
dataset = os.getenv("BQ_DATASET")


def get_last_loaded_timestamp(client, table_id):
    query = f"""
        SELECT MAX(timestamp) AS max_ts
        FROM `{table_id}`
    """

    try:
        result = client.query(query).result()
        row = list(result)[0]
        return row.max_ts
    except Exception as e:
        # Table may not exist yet
        print(e)
        return None



def main():
    # Step 0: Download dataset
    #download_kaggle_dataset()
    # Load dataset
    df = pd.read_csv("data/GlobalWeatherRepository.csv")

    last_loaded_ts = get_last_loaded_timestamp(client, table_id)

    print(last_loaded_ts)
    # Select & rename columns
    df = df.rename(columns={
        "location_name": "city",
        "temperature_celsius": "temp",
        "last_updated": "timestamp"
    })

    df = df[["city", "temp", "humidity", "timestamp"]]

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Convert to microseconds (Spark compatible)
    df["timestamp"] = df["timestamp"].astype("datetime64[us]")

    if last_loaded_ts:
        last_loaded_ts = pd.to_datetime(last_loaded_ts).to_datetime64()
        print(f"Filtering records after {last_loaded_ts}")
        df = df[df["timestamp"] > last_loaded_ts]
    else:
        pass

    if df.empty:
        print("No new data to process. Exiting.")
        exit(0)

    # Save as parquet
    df.to_parquet("weather_raw.parquet", index=False)

    print("Clean dataset ready")



if __name__ == "__main__":
    client = bigquery.Client()

# Build table id dynamically
    table_id = f"{project_id}.{dataset}.weather_processed"


    if not project_id or not dataset:
        raise ValueError("Missing environment variables: GCP_PROJECT_ID or BQ_DATASET")
    main()