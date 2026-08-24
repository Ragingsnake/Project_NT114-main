param (
    [ValidateSet("normal", "zkp_block", "label_flip", "byzantine")]
    [string] = "normal"
)
Continue = 'Stop'

 = if ( -eq "normal") { "false" } else { "true" }

Write-Host "Deploying FL Cluster to AKS via Helm (Attack Mode: )..." -ForegroundColor Cyan
helm upgrade --install fl-cluster ./helm/nt114-fl --set attackMode= --set malicious=

Write-Host "Deployed! Watch the pods spin up using: kubectl get pods -w" -ForegroundColor Green
