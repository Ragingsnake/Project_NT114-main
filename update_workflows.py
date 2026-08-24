import os

workflows = {
    "azure-create.yml": """name: Create Azure FL Infrastructure

on:
  workflow_dispatch:

jobs:
  provision:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Provision AKS Cluster
        run: |
          pwsh ./scripts/azure/1_provision_aks.ps1
""",
    "azure-run-attack.yml": """name: Dispatch FL Attack Scenario

on:
  workflow_dispatch:
    inputs:
      attack_mode:
        description: 'Choose the attack scenario to deploy'
        required: true
        type: choice
        default: 'normal'
        options:
          - normal
          - byzantine
          - label_flip
          - zkp_block

jobs:
  run-attack:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy Attack via Helm to AKS
        run: |
          curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
          chmod 700 get_helm.sh
          ./get_helm.sh
          
          az aks get-credentials --resource-group FL-ZKP-RG --name fl-zkp-aks --overwrite-existing
          
          pwsh ./scripts/azure/2_run_test_aks.ps1 -AttackMode ${{ github.event.inputs.attack_mode }}
""",
    "azure-fetch-results.yml": """name: Fetch FL Results & Charts

on:
  workflow_dispatch:

jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Generate and Download Plots from AKS
        run: |
          az aks get-credentials --resource-group FL-ZKP-RG --name fl-zkp-aks --overwrite-existing
          
          pwsh ./scripts/azure/3_get_results_aks.ps1

      - name: Upload Results to GitHub Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: FL-ZKP-Metrics
          path: az_results/
"""
}

for name, content in workflows.items():
    with open(f".github/workflows/{name}", "w") as f:
        f.write(content)
