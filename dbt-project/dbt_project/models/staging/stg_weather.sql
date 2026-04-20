select
    city,
    temp,
    humidity,
    timestamp
from {{ source('external', 'weather_processed') }}