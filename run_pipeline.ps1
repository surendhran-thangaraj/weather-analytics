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

Run-Step "Ingestion" "py ingestion/load_dataset.py"
Run-Step "Transform" "py spark/transform-weather.py"
Run-Step "Load to BigQuery" "py spark/load_to_bq.py"

push-location "dbt-project/dbt_project"
"dbt run"
"dbt test"

pop-location

Write-Host "🎉 Pipeline completed successfully!"