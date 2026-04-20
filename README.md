# 🌦️ Weather Analytics Data Pipeline

## 📌 Overview

This project implements an end-to-end data engineering pipeline that ingests, processes, and analyzes global weather data. The pipeline is fully automated, incrementally processes new data, and produces analytics-ready datasets for visualization.

---

## 🏗️ Architecture

```
Kaggle API
   ↓
Ingestion (Python)
   ↓
Transformation (Pandas / Spark)
   ↓
BigQuery (Partitioned Table)
   ↓
dbt (Transformations)
   ↓
Looker Studio Dashboard
```

---

## ⚙️ Tech Stack

* Python (Pandas, PyArrow)
* BigQuery (Data Warehouse)
* dbt (Transformations)
* PowerShell (Orchestration)
* Kaggle API (Data Source)
* Looker Studio (Dashboard)

---

## 🚀 Features

* ✅ Automated dataset ingestion using Kaggle API
* ✅ Incremental data loading using `timestamp`
* ✅ Partitioned BigQuery tables (by date)
* ✅ dbt transformations with incremental models
* ✅ Configurable environment using `.env`
* ✅ End-to-end orchestration via script
* ✅ Data quality checks using dbt tests

---

## 📂 Project Structure

```
project/
├── data/
├── ingestion/
├── spark/
├── dbt_project/
│── run_pipeline.ps1
├── .env
├── README.md
```

---

## 🔐 Configuration


Secure access to Google Cloud services is managed through a service account key (gcp.json), referenced via the GOOGLE_APPLICATION_CREDENTIALS environment variable.

Create a `.env` file:

```
GCP_PROJECT_ID=your-project-id
BQ_DATASET=weather_analytics
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_key
GOOGLE_APPLICATION_CREDENTIALS=path/to/gcp.json
```

---

## ▶️ How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```

---

### 2. Run pipeline

```
run_pipeline.ps1
```

---

## 🔄 Incremental Processing

Since the dataset provides full snapshots, incremental ingestion is implemented by:

* Querying the latest `last_updated` timestamp from BigQuery
* Filtering only new records in the ingestion step
* Appending new data to BigQuery

---

## 🗄️ Data Warehouse Design

* Partitioned by: `date`
* Clustered by: `city`
* Incremental loads using append strategy

---

## 📊 Dashboard

Built in Looker Studio:

* 📈 Temperature trends over time
* 📊 Weather distribution by city

---

## ⚠️ Design Decisions

* Local-to-BigQuery loading is used for simplicity
* GCS can be added for scalability in production
* Orchestration is implemented via script for lightweight execution



## 🏁 Conclusion

This project demonstrates a production-style data pipeline with incremental ingestion, cloud data warehousing, and transformation layers, designed for scalability and reproducibility.
