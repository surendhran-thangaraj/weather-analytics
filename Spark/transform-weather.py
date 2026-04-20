from pyspark.sql import SparkSession
from pyspark.sql.functions import col,to_date

# Create session
spark = SparkSession.builder \
    .appName("weather-transform") \
    .getOrCreate()

# Read raw data
df = spark.read.parquet("weather_raw.parquet")

# Show schema (debug)
print("=== RAW SCHEMA ===")
df.printSchema()

# Clean data
df_clean = df.select(
    col("city").cast("string"),
    col("temp").cast("double"),
    col("humidity").cast("int"),
    col("timestamp")  # already timestamp
).dropna()

df = df.withColumn("date", to_date("timestamp"))
# Show cleaned schema
print("=== CLEAN SCHEMA ===")
df_clean.printSchema()

# Write processed data
df.write \
    .mode("overwrite") \
    .parquet("weather_processed")

print("✅ Processed data saved")