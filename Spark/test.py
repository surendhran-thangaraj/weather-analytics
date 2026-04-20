import pandas as pd

df = pd.read_parquet("weather_processed")
print(df.head())
print(df.dtypes)