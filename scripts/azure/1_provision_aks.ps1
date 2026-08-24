Continue = 'Stop'
 = "FL-ZKP-RG"
 = "eastus"
 = "fl-zkp-aks"

Write-Host "Creating Resource Group: ..." -ForegroundColor Cyan
az group create --name  --location  -o none

Write-Host "Creating 2-Node AKS Cluster (This takes ~3-5 minutes)..." -ForegroundColor Cyan
az aks create --resource-group  --name  --node-count 2 --generate-ssh-keys --enable-managed-identity -o none

Write-Host "Fetching kubeconfig..." -ForegroundColor Cyan
az aks get-credentials --resource-group  --name  --overwrite-existing

Write-Host "AKS Cluster Provisioned Successfully!" -ForegroundColor Green
