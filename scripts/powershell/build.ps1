# Ensure we run from the project root (one level up from scripts/powershell)
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location -Path $ProjectRoot

# Set Corporate Proxy (Required for pip/apt during build)
$ProxyUrl = "http://host.docker.internal:3128"
$ProxyArgs = @("--build-arg", "HTTP_PROXY=$ProxyUrl", "--build-arg", "HTTPS_PROXY=$ProxyUrl", "--build-arg", "http_proxy=$ProxyUrl", "--build-arg", "https_proxy=$ProxyUrl")

Write-Host "--- Building fl-zkp-node ---" -ForegroundColor Cyan
docker build -f docker/Dockerfile.zkp_node -t ragingsnake/fl-zkp-node:latest $ProxyArgs .
if ($LASTEXITCODE -ne 0) { throw "Build failed for fl-zkp-node" }

Write-Host "--- Building fl-blockchain ---" -ForegroundColor Cyan
docker build -f docker/Dockerfile.blockchain -t ragingsnake/fl-blockchain:latest $ProxyArgs .
if ($LASTEXITCODE -ne 0) { throw "Build failed for fl-blockchain" }

Write-Host "--- Building fl-server (Optimized Size) ---" -ForegroundColor Cyan
docker build -f docker/Dockerfile.server -t ragingsnake/fl-server:latest $ProxyArgs .
if ($LASTEXITCODE -ne 0) { throw "Build failed for fl-server" }

Write-Host "--- Building fl-client (Optimized Size) ---" -ForegroundColor Cyan
docker build -f docker/Dockerfile.client -t ragingsnake/fl-client:latest $ProxyArgs .
if ($LASTEXITCODE -ne 0) { throw "Build failed for fl-client" }

Write-Host "=== All optimized images built successfully! ===" -ForegroundColor Green
docker images | Select-String "ragingsnake"
