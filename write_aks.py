import os

os.makedirs("scripts/azure", exist_ok=True)

with open("scripts/azure/1_provision_aks.ps1", "w") as f:
    f.write('''Continue = 'Stop'
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
''')

with open("scripts/azure/2_run_test_aks.ps1", "w") as f:
    f.write('''param (
    [ValidateSet("normal", "zkp_block", "label_flip", "byzantine")]
    [string] = "normal"
)
Continue = 'Stop'

 = if ( -eq "normal") { "false" } else { "true" }

Write-Host "Deploying FL Cluster to AKS via Helm (Attack Mode: )..." -ForegroundColor Cyan
helm upgrade --install fl-cluster ./helm/nt114-fl --set attackMode= --set malicious=

Write-Host "Deployed! Watch the pods spin up using: kubectl get pods -w" -ForegroundColor Green
''')

with open("scripts/azure/3_get_results_aks.ps1", "w") as f:
    f.write('''Continue = 'Stop'

Write-Host "Finding FL Server Pod..." -ForegroundColor Cyan
 = kubectl get pods -l app=fl-server -o jsonpath='{.items[0].metadata.name}'

if (-not ) {
    Write-Host "Server pod not found. Is the cluster running?" -ForegroundColor Red
    exit
}

Write-Host "Generating plots on the server..." -ForegroundColor Cyan
# Because Helm mapped results to /results, the history and plots are inside /results!
kubectl exec  -- python /app/shared/plot_results.py

Write-Host "Downloading results..." -ForegroundColor Cyan
if (-not (Test-Path -Path "./az_results")) {
    New-Item -ItemType Directory -Path "./az_results" | Out-Null
}

kubectl cp ":/results/history" ./az_results/history
kubectl cp ":/results/plots" ./az_results/plots

Write-Host "Done! Check the ./az_results folder." -ForegroundColor Green
''')

with open("scripts/azure/README.md", "w") as f:
    f.write('''# AKS (Azure Kubernetes Service) Deployment Workflow

These PowerShell scripts provision a 2-Node AKS Cluster to run your FL ZKP stack natively on Azure (fully compatible with your Azure for Students account limits!).

## Workflows

### 1. Provision Infrastructure
Run .\\1_provision_aks.ps1
Creates the FL-ZKP-RG Resource Group and a 2-node AKS cluster. Automatically downloads the kubeconfig to your local machine so you can use kubectl.

### 2. Manual Dispatch Attack Workflow
Run .\\2_run_test_aks.ps1 -AttackMode <MODE>
Available modes: 
ormal, yzantine, label_flip, zkp_block.
This uses the existing Helm chart in helm/nt114-fl/, which has been completely modernized to support the new modular Docker images and ZKP Node!

### 3. Fetch Results
Run .\\3_get_results_aks.ps1
Triggers plot generation inside the AKS pod and uses kubectl cp to seamlessly download all charts and JSON files locally.

### 4. Cleanup
Run .\\4_destroy_rg.ps1
Instantly destroys the Resource Group.
''')
