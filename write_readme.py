import io

readme = '''# Blockchain-Based Federated Learning with ZKP Validation

A secure, decentralized Federated Learning (FL) architecture that leverages **Blockchain Reputation Smart Contracts**, **IPFS decentralized storage**, and **Zero-Knowledge Proofs (ZKP)** to protect data privacy and actively defend against adversarial poisoning and Byzantine attacks.

---

## \U0001f3d7 Architecture Overview

Traditional Federated Learning relies on a trusted central server and is highly vulnerable to malicious clients uploading poisoned models (e.g., Backdoor Attacks, Label Flipping, Scaling Attacks). 

This project solves those vulnerabilities using a multi-layered defense:

1. **ZKP Range Proofs (First Line of Defense):** 
   Clients generate cryptographic zero-knowledge proofs demonstrating that their weight updates fall within acceptable mathematical bounds without revealing their local datasets. Massive scaling or exploding gradient attacks are cryptographically blocked before they even reach the server.
2. **IPFS Decentralized Storage:**
   Local model updates are pushed to IPFS, ensuring an immutable, decentralized audit trail.
3. **Blockchain Reputation System (Second Line of Defense):**
   The central aggregator validates updates using Cosine Similarity and Interquartile Range (IQR) analysis. Malicious updates (e.g., sneaky label-flipping) are rejected, and the client's reputation is permanently slashed on the Ethereum blockchain via Smart Contracts.

## \U0001f6e1 Attack Scenarios & Defenses

This repository features built-in adversarial simulation. You can deploy the clients in 4 different ATTACK_MODEs:

* 
ormal: Honest local training.
* label_flip: Clients flip the sign of their weights to degrade the global model. Caught by the **Blockchain Reputation System**.
* yzantine: Clients send aggressive Gaussian noise. Caught by the **Blockchain Reputation System**.
* zkp_block: Clients maliciously scale their weights massively. Caught instantly by the **ZKP Node** (fails to generate a valid cryptographic proof).

---

## \U0001f4bb Local Deployment (Docker Compose)

The entire stack is fully modularized and containerized. 

### Prerequisites
* Docker Desktop & Docker Compose V2
* Node.js (for local Truffle contract compilation if needed)

### Running the Stack
Use the provided PowerShell manager script to control the local lifecycle:

`powershell
# Run a normal, honest FL session
.\\scripts\\powershell\\manage.ps1 -Command start-normal

# Run the malicious attack demo (Clients 4 & 5 turn adversarial)
.\\scripts\\powershell\\manage.ps1 -Command start-attack

# View real-time logs (watch the Server block the attackers!)
.\\scripts\\powershell\\manage.ps1 -Command logs

# Stop and clean up volumes
.\\scripts\\powershell\\manage.ps1 -Command stop
`

---

## \u2601\ufe0f Cloud Deployment (Azure Kubernetes Service)

If you want to train on the cloud (e.g., using your Azure for Students credits) without burning your local CPU or GitHub Action limits, we provide a fully automated **2-Node AKS Deployment Workflow**.

All cloud scripts are located in scripts/azure/:

1. **Provision Infrastructure:**
   `powershell
   .\\scripts\\azure\\1_provision_aks.ps1
   `
   Creates the Resource Group and a 2-Node AKS cluster, automatically mapping your kubeconfig.

2. **Launch Attack Scenario:**
   `powershell
   .\\scripts\\azure\\2_run_test_aks.ps1 -AttackMode zkp_block
   `
   Uses Helm to deploy the Blockchain, IPFS, ZKP Node, Server, and 5 Clients directly to Kubernetes. (Available modes: 
ormal, yzantine, label_flip, zkp_block).

3. **Fetch Charts & Metrics:**
   `powershell
   .\\scripts\\azure\\3_get_results_aks.ps1
   `
   Executes the plotting scripts directly inside the AKS cluster and seamlessly downloads your JSON history and Stacked Bar Charts locally to ./az_results/.

4. **Cleanup:**
   `powershell
   .\\scripts\\azure\\4_destroy_rg.ps1
   `
   Instantly destroys the Azure resources to halt billing.

---

## \U0001f680 GitHub Actions CI/CD

Prefer clickable buttons? We've wrapped the AKS deployment scripts into **Manual Dispatch Workflows**.
Go to the **Actions** tab in GitHub to easily Provision, Dispatch Attacks, Fetch Results (via Artifacts), and Destroy the cluster right from your browser!

*(Requires setting AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_SUBSCRIPTION_ID, and AZURE_TENANT_ID in your repository secrets).*
'''

with io.open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
