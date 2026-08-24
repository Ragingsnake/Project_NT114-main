import os
import time
import requests


def upload_to_ipfs(file_path):

    try:

        api_addr = os.getenv("IPFS_API_ADDR", "http://ipfs:5001")
        if api_addr.startswith("/dns") or api_addr.startswith("/ip4"):
            api_addr = "http://ipfs:5001"
            
        url = f"{api_addr}/api/v0/add"
        
        last_error = None
        for _ in range(30):
            try:
                with open(file_path, 'rb') as f:
                    res = requests.post(url, files={'file': f})
                res.raise_for_status()
                break
            except Exception as error:
                last_error = error
                time.sleep(2)
        else:
            raise RuntimeError(f"Unable to connect to IPFS at {api_addr}") from last_error

        cid = res.json()["Hash"]

        print(f"📦 Uploaded {file_path} -> CID: {cid}")

        return cid

    except Exception as e:

        print("❌ IPFS Upload Failed:", e)

        return "IPFS_ERROR"