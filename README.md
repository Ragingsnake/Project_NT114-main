# Blockchain-Based Federated Learning with ZKP Validation

A secure, decentralized Federated Learning (FL) architecture that leverages **Blockchain Reputation Smart Contracts**, **IPFS decentralized storage**, and **Zero-Knowledge Proofs (ZKP)** to protect data privacy and actively defend against adversarial poisoning and Byzantine attacks.

---

## Architecture Overview

Traditional Federated Learning relies on a trusted central server and is highly vulnerable to malicious clients uploading poisoned models (e.g., Backdoor Attacks, Label Flipping, Scaling Attacks). 

This project solves those vulnerabilities using a multi-layered defense:

1. **ZKP Range Proofs (First Line of Defense):** 
   Clients generate cryptographic zero-knowledge proofs demonstrating that their weight updates fall within acceptable mathematical bounds without revealing their local datasets. Massive scaling or exploding gradient attacks are cryptographically blocked before they even reach the server.
2. **IPFS Decentralized Storage:**
   Local model updates are pushed to IPFS, ensuring an immutable, decentralized audit trail.
3. **Blockchain Reputation System (Second Line of Defense):**
   The central aggregator validates updates using Cosine Similarity and Interquartile Range (IQR) analysis. Malicious updates (e.g., sneaky label-flipping) are rejected, and the client's reputation is permanently slashed on the Ethereum blockchain via Smart Contracts.

## Attack Scenarios & Defenses

This repository features built-in adversarial simulation. You can deploy the clients in 4 different ATTACK_MODEs:

* Normal: Honest local training.
* label_flip: Clients flip the sign of their weights to degrade the global model. Caught by the **Blockchain Reputation System**.
* Byzantine: Clients send aggressive Gaussian noise. Caught by the **Blockchain Reputation System**.
* zkp_block: Clients maliciously scale their weights massively. Caught instantly by the **ZKP Node** (fails to generate a valid cryptographic proof).

---

## Local Deployment (Docker Compose)

The entire stack is fully modularized and containerized. 

### Prerequisites
* Docker Desktop & Docker Compose V2
* Node.js (for local Truffle contract compilation if needed)

### Running the Stack
Use the provided PowerShell manager script to control the local lifecycle:

```powershell
## Run a normal, honest FL session
.\scripts\powershell\manage.ps1 -Command start-normal

## Run the malicious attack demo (Clients 4 & 5 turn adversarial)
.\scripts\powershell\manage.ps1 -Command start-attack

## View real-time logs (watch the Server block the attackers!)
.\scripts\powershell\manage.ps1 -Command logs

## Stop and clean up volumes
.\scripts\powershell\manage.ps1 -Command stop
```