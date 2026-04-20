# Load .env file into environment variables
Get-Content .env | ForEach-Object {
    if ($_ -match "^\s*#") { return }   # skip comments
    if ($_ -match "^\s*$") { return }   # skip empty lines

    $name, $value = $_ -split '=', 2

    # Trim spaces
    $name = $name.Trim()
    $value = $value.Trim()

    # ✅ Correct way to set env var
    Set-Item -Path "Env:$name" -Value $value
}


# Debug (optional)
Write-Output "GCP_PROJECT_ID = $env:GCP_PROJECT_ID"
Write-Output "BQ_DATASET = $env:BQ_DATASET"


# Function to run step safely
function Run-Step {
    param (
        [string]$Name,
        [string]$Command
    )

    Write-Host "▶ Running: $Name"

    Invoke-Expression $Command

    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Step failed: $Name"
        exit 1
    }

    Write-Host "✅ Completed: $Name"
}

Run-Step "Ingestion" "python ingestion/load_dataset.py"
Run-Step "Transform" "python spark/transform_weather.py"
Run-Step "Upload to GCS" "python upload_to_gcs.py"
Run-Step "Load to BigQuery" "python load_to_bq.py"

Run-Step "dbt Run" "dbt run"
Run-Step "dbt Test" "dbt test"

Write-Host "🎉 Pipeline completed successfully!"