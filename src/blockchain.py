import json
import os
import time
from pathlib import Path
from web3 import Web3

CONTRACT_ADDRESS_FILE = Path(os.getenv("CONTRACT_ADDRESS_FILE", "runtime/reputation-address.json"))
WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:7545")

_w3 = None
_contract = None


def _init():
    global _w3, _contract
    if _contract is not None:
        return

    # Wait for contract-init to finish deploying
    for attempt in range(60):
        if CONTRACT_ADDRESS_FILE.exists():
            break
        if attempt % 10 == 0:
            print(f"Waiting for contract deployment ({CONTRACT_ADDRESS_FILE})...")
        time.sleep(2)
    else:
        raise RuntimeError(f"Contract address file not found after 120s: {CONTRACT_ADDRESS_FILE}")

    with open(CONTRACT_ADDRESS_FILE, "r") as f:
        info = json.load(f)

    provider = info.get("provider", WEB3_PROVIDER_URI)
    _w3 = Web3(Web3.HTTPProvider(provider))

    if not _w3.is_connected():
        raise RuntimeError(f"Cannot connect to Ethereum provider: {provider}")

    _contract = _w3.eth.contract(address=info["address"], abi=info["abi"])
    print(f"Connected to Reputation contract at {info['address']}")


def submit_update(round_num, client_id, cid, proof_hash, accuracy):
    try:
        _init()
        account = _w3.eth.accounts[int(client_id) % len(_w3.eth.accounts)]
        acc_uint = int(float(accuracy) * 10000)
        tx_hash = _contract.functions.submitUpdate(
            int(round_num), int(client_id), str(cid), str(proof_hash), acc_uint
        ).transact({"from": account})
        receipt = _w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()
    except Exception as e:
        print(f"Blockchain submit_update error: {e}")
        return None


def verify_update(client_id, round_num, result):
    try:
        _init()
        account = _w3.eth.accounts[0]
        tx_hash = _contract.functions.verifyUpdate(
            int(client_id), int(round_num), bool(result)
        ).transact({"from": account})
        _w3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        print(f"Blockchain verify_update error: {e}")
