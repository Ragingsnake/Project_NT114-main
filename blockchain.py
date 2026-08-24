import json
import os
import time

from web3 import Web3
from reputation import update_reputation

def _load_contract_json():
    artifact_path = os.getenv("CONTRACT_ARTIFACT", "build/contracts/Reputation.json")

    with open(artifact_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_contract_address(contract_json):
    env_address = os.getenv("CONTRACT_ADDRESS")
    if env_address:
        return env_address

    address_file = os.getenv("CONTRACT_ADDRESS_FILE", "runtime/reputation-address.json")
    if os.path.exists(address_file):
        with open(address_file, "r", encoding="utf-8") as f:
            payload = json.load(f)

        if isinstance(payload, dict):
            if "address" in payload:
                return payload["address"]
            if "contractAddress" in payload:
                return payload["contractAddress"]

    networks = contract_json.get("networks", {})
    if networks:
        network_id = sorted(networks.keys(), key=lambda value: int(value))[0]
        return networks[network_id]["address"]

    raise RuntimeError(
        "Contract address not found. Deploy Reputation.sol first or set CONTRACT_ADDRESS."
    )


def _build_contract():
    provider_uri = os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:7545")
    w3 = Web3(Web3.HTTPProvider(provider_uri))

    last_error = None
    for _ in range(30):
        try:
            if w3.is_connected() and w3.eth.accounts:
                break
        except Exception as error:
            last_error = error
        time.sleep(2)
    else:
        raise RuntimeError(f"Unable to connect to Ethereum provider: {provider_uri}") from last_error

    contract_json = _load_contract_json()
    contract_address = _resolve_contract_address(contract_json)
    abi = contract_json["abi"]
    contract = w3.eth.contract(address=contract_address, abi=abi)

    account_index = int(os.getenv("WEB3_ACCOUNT_INDEX", "0"))
    account = w3.eth.accounts[account_index]

    return w3, contract, account


w3, contract, account = _build_contract()

# ==========================================
# Submit client update
# ==========================================
def submit_update(round_num, client_id, cid, proof_hash, accuracy):

    tx = contract.functions.submitUpdate(
        int(round_num),
        int(client_id),
        str(cid), # cid này có thể là tên hoặc hash (string)
        str(proof_hash),
        int(accuracy * 1000)
    ).transact({"from": account})

    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt.transactionHash.hex()

# ==========================================
# Verify update + update reputation (SỬA LỖI TẠI ĐÂY)
# ==========================================
def verify_update(client_id, round_num, result):
    try:
        tx = contract.functions.verifyUpdate(
            int(client_id),   
            int(round_num),   
            bool(result)      
        ).transact({"from": account})

        w3.eth.wait_for_transaction_receipt(tx)

        score = 1.0 if result else -1.0
        rep = update_reputation(client_id, score)

        print(f"✅ Blockchain Verify → Client {client_id} | Round {round_num} | Rep: {rep:.3f}")
        return True
    except Exception as e:
        print(f"❌ Blockchain Error: {e}")
        return False

# ==========================================
# Query reputation
# ==========================================
def get_reputation(client_id):
    return contract.functions.getReputation(int(client_id)).call()