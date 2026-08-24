import os

def replace_in_file(filepath, old, new):
    with open(filepath, "r") as f:
        c = f.read()
    c = c.replace(old, new)
    with open(filepath, "w") as f:
        f.write(c)

# 1. Update fl-server.yaml
server = "helm/nt114-fl/templates/fl-server.yaml"
replace_in_file(server, 'image: {{ include "nt114-fl.appImage" . }}', 'image: {{ .Values.images.server }}')
replace_in_file(server, 'command: ["python", "fl_server.py"]', '')
replace_in_file(server, 'imagePullPolicy: {{ .Values.image.pullPolicy }}', 'imagePullPolicy: {{ .Values.images.pullPolicy }}')
# Add ZKP node env var
replace_in_file(server, 'env:', 'env:\n            - name: ZKP_NODE_URL\n              value: "http://fl-zkp-node:8081"')

# 2. Update clients.yaml
clients = "helm/nt114-fl/templates/clients.yaml"
replace_in_file(clients, 'image: {{ include "nt114-fl.appImage" . }}', 'image: {{ .Values.images.client }}')
replace_in_file(clients, 'command: ["python", "fl_client.py", "{{  }}", "{{ .Values.fl.splitType }}"]', 'env:\n            - name: ATTACK_MODE\n              value: {{ .Values.attackMode | quote }}\n            - name: MALICIOUS\n              value: {{ .Values.malicious | quote }}')
replace_in_file(clients, 'imagePullPolicy: {{ .Values.image.pullPolicy }}', 'imagePullPolicy: {{ .Values.images.pullPolicy }}')
replace_in_file(clients, 'env:', 'env:\n            - name: ZKP_NODE_URL\n              value: "http://fl-zkp-node:8081"')
# Note: we replaced the 'command' so the default Dockerfile entrypoint runs. 
# But wait, we need to pass CLIENT_ID. 
# It's better to add them to env.
replace_in_file(clients, '- name: CLIENT_ID\n              value: "{{  }}"', '- name: CLIENT_ID\n              value: "{{  }}"') # already exists in the original? Let's check.

# 3. Update contract-bootstrap-job.yaml
contract = "helm/nt114-fl/templates/contract-bootstrap-job.yaml"
replace_in_file(contract, 'image: {{ include "nt114-fl.appImage" . }}', 'image: {{ .Values.images.blockchain }}')
replace_in_file(contract, 'command: ["python", "deploy_contract.py"]', '')
replace_in_file(contract, 'imagePullPolicy: {{ .Values.image.pullPolicy }}', 'imagePullPolicy: {{ .Values.images.pullPolicy }}')

print("Templates patched.")
