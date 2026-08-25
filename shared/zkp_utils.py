import hashlib
import json
import os
import requests
import subprocess
import tempfile

ZKP_NODE_URL = os.getenv("ZKP_NODE_URL", "http://fl-zkp-node:8081")

def hash_model(parameters):
    m = hashlib.sha256()
    for p in parameters:
        m.update(p.tobytes())
    return m.hexdigest()

def generate_proof(parameters, client_id, dataset_size=0):
    model_hash = hash_model(parameters)
    secret_chunk = int(client_id)
    expected_hash = secret_chunk**3 + secret_chunk

    try:
        import numpy as np
        total_abs_weight = sum(np.sum(np.abs(p)) for p in parameters)
        weight_magnitude = int(total_abs_weight * 100)
        max_weight_magnitude = 5000000000 # 5 Billion limit
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            input_json = os.path.join(tmpdirname, "input.json")
            with open(input_json, "w") as f:
                json.dump({
                    "secret_dataset_chunk": secret_chunk, 
                    "expected_hash": expected_hash,
                    "weight_magnitude": weight_magnitude,
                    "max_weight_magnitude": max_weight_magnitude
                }, f)
            
            proof_json = os.path.join(tmpdirname, "proof.json")
            public_json = os.path.join(tmpdirname, "public.json")
            
            subprocess.run([
                "snarkjs", "groth16", "fullprove",
                input_json,
                "zkp/dataset_proof.wasm",
                "zkp/circuit_final.zkey",
                proof_json, public_json
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            with open(proof_json, "r") as f:
                proof = json.load(f)
            
            with open(public_json, "r") as f:
                public_signals = json.load(f)
                
            response = requests.post(f"{ZKP_NODE_URL}/verify", json={
                "client_id": client_id,
                "model_hash": model_hash,
                "dataset_size": dataset_size,
                "proof": proof,
                "public_signals": public_signals
            }, timeout=60)
            response.raise_for_status()
            
            return {
                "proof": proof,
                "public_signals": public_signals
            }
    except Exception as e:
        print(f"Error generating ZKP proof: {e}")
        return None

def verify_proof(parameters, proof_data, client_id, dataset_size=0):
    if not proof_data:
        return False
        
    model_hash = hash_model(parameters)
    try:
            response = requests.post(f"{ZKP_NODE_URL}/verify", json={
                "client_id": client_id,
                "model_hash": model_hash,
                "dataset_size": dataset_size,
                "proof": proof_data.get("proof"),
                "public_signals": proof_data.get("public_signals")
            }, timeout=60)
        response.raise_for_status()
        return response.json().get("valid", False)
    except Exception as e:
        print(f"Error verifying ZKP proof: {e}")
        return False
