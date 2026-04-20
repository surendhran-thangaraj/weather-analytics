import pandas as pd

# Load dataset
df = pd.read_csv("data/GlobalWeatherRepository.csv")

# Select & rename columns
df = df.rename(columns={
    "location_name": "city",
    "temperature_celsius": "temp",
    "last_updated": "timestamp"
})

df = df[["city", "temp", "humidity", "timestamp"]]

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Save as parquet
df.to_parquet("weather_raw.parquet", index=False)

print("✅ Clean dataset ready")