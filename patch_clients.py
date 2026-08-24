import os

def replace_in_file(filepath, old, new):
    with open(filepath, "r") as f:
        c = f.read()
    c = c.replace(old, new)
    with open(filepath, "w") as f:
        f.write(c)

clients = "helm/nt114-fl/templates/clients.yaml"
replace_in_file(clients, 'image: {{ include "nt114-fl.appImage"  }}', 'image: {{ .Values.images.client }}')
replace_in_file(clients, 'command: ["python", "fl_client.py", "{{  }}", "{{ .Values.fl.splitType }}"]', 'env:\n            - name: ATTACK_MODE\n              value: {{ .Values.attackMode | quote }}\n            - name: MALICIOUS\n              value: {{ .Values.malicious | quote }}')
replace_in_file(clients, 'imagePullPolicy: {{ .Values.image.pullPolicy }}', 'imagePullPolicy: {{ .Values.images.pullPolicy }}')
# Clean up duplicate env:
with open(clients, "r") as f:
    c = f.read()
c = c.replace('env:\n            - name: ATTACK_MODE', '          env:\n            - name: ATTACK_MODE')
c = c.replace('          env:\n            - name: ZKP_NODE_URL', '            - name: ZKP_NODE_URL')
with open(clients, "w") as f:
    f.write(c)
print("Clients fixed")
