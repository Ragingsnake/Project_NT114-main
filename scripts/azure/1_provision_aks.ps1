$ErrorActionPreference = 'Stop'
$rgName = "FL-ZKP-RG"
$location = "eastus"
$clusterName = "fl-zkp-aks"

Write-Host "Creating Resource Group: $rgName..." -ForegroundColor Cyan
az group create --name $rgName --location $location -o none

Write-Host "Creating 2-Node AKS Cluster (This takes ~3-5 minutes)..." -ForegroundColor Cyan
az aks create --resource-group $rgName --name $clusterName --node-count 2 --generate-ssh-keys --enable-managed-identity -o none

Write-Host "Fetching kubeconfig..." -ForegroundColor Cyan
az aks get-credentials --resource-group $rgName --name $clusterName --overwrite-existing

Write-Host "AKS Cluster Provisioned Successfully!" -ForegroundColor Green
