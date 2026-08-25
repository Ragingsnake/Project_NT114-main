$ErrorActionPreference = 'Stop'

Write-Host "Creating a temporary extractor pod to mount the results PVC..." -ForegroundColor Cyan

$tempPodYaml = @"
apiVersion: v1
kind: Pod
metadata:
  name: fl-results-extractor
  namespace: nt114-fl
spec:
  containers:
  - name: extractor
    image: ragingsnake/fl-server:latest
    command: ["sleep", "3600"]
    env:
    - name: RESULTS_DIR
      value: /results
    volumeMounts:
    - name: results
      mountPath: /results
  volumes:
  - name: results
    persistentVolumeClaim:
      claimName: fl-results
  restartPolicy: Never
"@

$tempPodYaml | kubectl apply -f -

Write-Host "Waiting for extractor pod to be ready..." -ForegroundColor Cyan
kubectl wait --for=condition=Ready pod/fl-results-extractor -n nt114-fl --timeout=300s

Write-Host "Generating plots on the server..." -ForegroundColor Cyan
kubectl exec -n nt114-fl fl-results-extractor -- sh -c "RESULTS_DIR=/results python /app/shared/plot_results.py"

Write-Host "Downloading results..." -ForegroundColor Cyan
if (-not (Test-Path -Path "./az_results")) {
    New-Item -ItemType Directory -Path "./az_results" | Out-Null
}

kubectl cp -n nt114-fl "fl-results-extractor:/results/history" ./az_results/history
kubectl cp -n nt114-fl "fl-results-extractor:/results/plots" ./az_results/plots

Write-Host "Cleaning up extractor pod..." -ForegroundColor Cyan
kubectl delete pod fl-results-extractor -n nt114-fl --ignore-not-found

Write-Host "Done! Check the ./az_results folder." -ForegroundColor Green
