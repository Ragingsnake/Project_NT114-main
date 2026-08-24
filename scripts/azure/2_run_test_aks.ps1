param (
    [ValidateSet("normal", "zkp_block", "label_flip", "byzantine")]
    [string]$attackMode = "normal",
    [int]$rounds = 25
)
$ErrorActionPreference = 'Stop'

$malicious = if ($attackMode -eq "normal") { "false" } else { "true" }

Write-Host "Deploying FL Cluster to AKS via Helm (Attack Mode: $attackMode, Rounds: $rounds)..." -ForegroundColor Cyan
helm upgrade --install fl-cluster ./helm/nt114-fl --set attackMode=$attackMode --set malicious=$malicious --set rounds=$rounds
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Deployed! Watch the pods spin up using: kubectl get pods -w" -ForegroundColor Green
