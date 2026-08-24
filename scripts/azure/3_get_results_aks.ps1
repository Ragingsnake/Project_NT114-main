Continue = 'Stop'

Write-Host "Finding FL Server Pod..." -ForegroundColor Cyan
 = kubectl get pods -l app=fl-server -o jsonpath='{.items[0].metadata.name}'

if (-not ) {
    Write-Host "Server pod not found. Is the cluster running?" -ForegroundColor Red
    exit
}

Write-Host "Generating plots on the server..." -ForegroundColor Cyan
# Because Helm mapped results to /results, the history and plots are inside /results!
kubectl exec  -- python /app/shared/plot_results.py

Write-Host "Downloading results..." -ForegroundColor Cyan
if (-not (Test-Path -Path "./az_results")) {
    New-Item -ItemType Directory -Path "./az_results" | Out-Null
}

kubectl cp ":/results/history" ./az_results/history
kubectl cp ":/results/plots" ./az_results/plots

Write-Host "Done! Check the ./az_results folder." -ForegroundColor Green
