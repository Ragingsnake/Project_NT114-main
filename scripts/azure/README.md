# AKS (Azure Kubernetes Service) Deployment Workflow

These PowerShell scripts provision a 2-Node AKS Cluster to run your FL ZKP stack natively on Azure (fully compatible with your Azure for Students account limits!).

## Workflows

### 1. Provision Infrastructure
Run .\1_provision_aks.ps1
Creates the FL-ZKP-RG Resource Group and a 2-node AKS cluster. Automatically downloads the kubeconfig to your local machine so you can use kubectl.

### 2. Manual Dispatch Attack Workflow
Run .\2_run_test_aks.ps1 -AttackMode <MODE>
Available modes: 
ormal, yzantine, label_flip, zkp_block.
This uses the existing Helm chart in helm/nt114-fl/, which has been completely modernized to support the new modular Docker images and ZKP Node!

### 3. Fetch Results
Run .\3_get_results_aks.ps1
Triggers plot generation inside the AKS pod and uses kubectl cp to seamlessly download all charts and JSON files locally.

### 4. Cleanup
Run .\4_destroy_rg.ps1
Instantly destroys the Resource Group.
