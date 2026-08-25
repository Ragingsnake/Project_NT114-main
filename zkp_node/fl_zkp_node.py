import hashlib
import json
import logging
import os
import subprocess
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ZKP_Node")

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
        
    proof = data.get('proof')
    public_signals = data.get('public_signals')
    client_id = data.get('client_id')
    
    if not proof or not public_signals or client_id is None:
        return jsonify({"error": "Missing parameters"}), 400
        
    # FIX #2: Strictly verify the public signal matches the server policy
    expected_limit = "5000000000"
    if len(public_signals) < 2 or str(public_signals[1]) != expected_limit:
        logger.warning(f"🚨 Client {client_id} attempted to bypass max_weight_magnitude limit! (Sent: {public_signals[1] if len(public_signals) > 1 else 'None'})")
        return jsonify({"valid": False, "error": f"Invalid max_weight_magnitude. Expected {expected_limit}."})
        
    # FIX #3: Strictly verify the client identity public signal
    try:
        cid_int = int(client_id)
        expected_hash = str(cid_int**3 + cid_int)
        if str(public_signals[0]) != expected_hash:
            logger.warning(f"🚨 Client {client_id} attempted identity spoofing! (Expected Hash: {expected_hash}, Sent: {public_signals[0]})")
            return jsonify({"valid": False, "error": "Identity verification failed. Spoofed credentials."})
    except ValueError:
        return jsonify({"valid": False, "error": "Invalid client_id format."})
        
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            proof_json = os.path.join(tmpdirname, "proof.json")
            public_json = os.path.join(tmpdirname, "public.json")
            
            with open(proof_json, "w") as f:
                json.dump(proof, f)
            with open(public_json, "w") as f:
                json.dump(public_signals, f)
                
            result = subprocess.run([
                "snarkjs", "groth16", "verify",
                "zkp/verification_key.json",
                public_json, proof_json
            ], capture_output=True, text=True)
            
            if "OK" in result.stdout:
                logger.info(f"? Real zk-SNARK Verification PASSED for client {client_id}")
                is_valid = True
            else:
                logger.warning(f"? Real zk-SNARK Verification FAILED for client {client_id}")
                is_valid = False
                
    except Exception as e:
        logger.error(f"Error during snarkjs verify: {e}")
        is_valid = False
        
    return jsonify({"valid": is_valid})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8081))
    logger.info(f"Starting ZKP Node on port {port}")
    app.run(host='0.0.0.0', port=port)
