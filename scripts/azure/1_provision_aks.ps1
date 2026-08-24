$ErrorActionPreference = 'Stop'
$rgName = "FL-ZKP-RG"
$location = "southeastasia"
$clusterName = "fl-zkp-aks"

Write-Host "Creating Resource Group: $rgName..." -ForegroundColor Cyan
az group create --name $rgName --location $location -o none
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Creating 2-Node AKS Cluster (This takes ~3-5 minutes)..." -ForegroundColor Cyan
az aks create --resource-group $rgName --name $clusterName --node-count 2 --node-vm-size Standard_B2s --generate-ssh-keys --enable-managed-identity -o none
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Fetching kubeconfig..." -ForegroundColor Cyan
az aks get-credentials --resource-group $rgName --name $clusterName --overwrite-existing
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "AKS Cluster Provisioned Successfully!" -ForegroundColor Green
