# 4_destroy_rg.ps1
# Deletes the Azure Resource Group to stop billing.
Write-Host "Destroying Azure Resource Group FL-ZKP-RG..." -ForegroundColor Red
az group delete --name FL-ZKP-RG --yes --no-wait
Write-Host "Deletion triggered. The resources will be removed in the background." -ForegroundColor Green
