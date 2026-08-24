import os

helm_dir = "helm/nt114-fl"

values = '''namespace: nt114-fl

images:
  server: docker.io/ragingsnake/fl-server:latest
  client: docker.io/ragingsnake/fl-client:latest
  blockchain: docker.io/ragingsnake/fl-blockchain:latest
  zkpNode: docker.io/ragingsnake/fl-zkp-node:latest
  pullPolicy: Always

ganache:
  image: trufflesuite/ganache:v7.9.2
  chainId: "1337"
  mnemonic: "test test test test test test test test test test test junk"

ipfs:
  image: ipfs/kubo:v0.32.1

storage:
  className: azurefile-csi
  resultsSize: 10Gi

fl:
  serverPort: 8080
  clientCount: 5
  splitType: non_iid

attackMode: "normal"
malicious: "false"

plot:
  enabled: false
  mode: non_iid
'''

with open(f"{helm_dir}/values.yaml", "w") as f:
    f.write(values)

values_aks = '''images:
  pullPolicy: Always

storage:
  className: azurefile-csi
  resultsSize: 20Gi

attackMode: "normal"
malicious: "false"
'''

with open(f"{helm_dir}/values-aks.yaml", "w") as f:
    f.write(values_aks)

zkp_node = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: fl-zkp-node
  namespace: {{ .Values.namespace }}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fl-zkp-node
  template:
    metadata:
      labels:
        app: fl-zkp-node
    spec:
      containers:
        - name: fl-zkp-node
          image: {{ .Values.images.zkpNode }}
          imagePullPolicy: {{ .Values.images.pullPolicy }}
          ports:
            - containerPort: 8081
---
apiVersion: v1
kind: Service
metadata:
  name: fl-zkp-node
  namespace: {{ .Values.namespace }}
spec:
  selector:
    app: fl-zkp-node
  ports:
    - protocol: TCP
      port: 8081
      targetPort: 8081
'''

with open(f"{helm_dir}/templates/zkp-node.yaml", "w") as f:
    f.write(zkp_node)

print("Values and ZKP Node added.")
