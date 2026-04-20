{{ config(
    materialized='incremental',
    partition_by={
      "field": "date",
      "data_type": "date"
    },
    cluster_by=["city"]
) }}

select
  date(timestamp) as date,
  city,
  avg(temp) as avg_temp,
  avg(humidity) as avg_humidity,
  count(*) as records
from {{ ref('stg_weather') }}

{% if is_incremental() %}
where timestamp >= (select max(timestamp) from {{ this }})
{% endif %}

group by 1,2