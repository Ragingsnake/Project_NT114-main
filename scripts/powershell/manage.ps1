param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("start-normal", "start-attack", "stop", "logs")]
    [string]$Command
)

if (-not $Command) {
    Write-Host "Usage: .\manage.ps1 -Command [start-normal|start-attack|stop|logs]" -ForegroundColor Yellow
    exit
}

# Ensure we run from the project root (one level up from scripts/powershell)
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location -Path $ProjectRoot

# Clear proxy environment variables to prevent Docker Desktop routing bugs on internal traffic
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:http_proxy = ""
$env:https_proxy = ""

switch ($Command) {
    "start-normal" {
        Write-Host "Starting standard federated learning run..." -ForegroundColor Green
        $env:MALICIOUS = "false"
        $env:FAULTY_CLIENTS = ""
        docker compose up -d
    }
    "start-attack" {
        Write-Host "Starting malicious federated learning run (Clients 4 & 5 are attackers)..." -ForegroundColor Red
        $env:MALICIOUS = "true"
        $env:FAULTY_CLIENTS = "4,5"
        docker compose up -d
    }
    "stop" {
        Write-Host "Stopping and cleaning up containers and volumes..." -ForegroundColor Yellow
        docker compose down -v
    }
    "logs" {
        docker compose logs -f
    }
}
