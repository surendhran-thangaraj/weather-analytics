import pandas as pd

df = pd.read_parquet("weather_raw.parquet")

print(df.head())
print(df.dtypes)
print(len(df.index))