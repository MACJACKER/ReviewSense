# Test All Components of the Sentiment Analysis Application
# This script runs all tests for the backend, frontend, and model

Write-Host "Starting comprehensive testing of the Sentiment Analysis Application" -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Green

# Check if backend server is running
$backendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -Method GET -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        $backendRunning = $true
        Write-Host "✅ Backend server is running" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend server is not running" -ForegroundColor Red
    Write-Host "Starting backend server..." -ForegroundColor Yellow
}

# Check if frontend server is running
$frontendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        $frontendRunning = $true
        Write-Host "✅ Frontend server is running" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend server is not running" -ForegroundColor Red
    Write-Host "Starting frontend server..." -ForegroundColor Yellow
}

# Start servers if needed
$startedBackend = $false
$startedFrontend = $false

if (-not $backendRunning) {
    $backendJob = Start-Job -ScriptBlock {
        Set-Location "$env:USERPROFILE\OneDrive\Desktop\Sentiment Analysis\backend"
        uvicorn main:app --reload
    }
    $startedBackend = $true
    Write-Host "Backend server starting..." -ForegroundColor Yellow
    # Wait for backend to start
    Start-Sleep -Seconds 5
}

if (-not $frontendRunning) {
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location "$env:USERPROFILE\OneDrive\Desktop\Sentiment Analysis\frontend"
        npm run dev
    }
    $startedFrontend = $true
    Write-Host "Frontend server starting..." -ForegroundColor Yellow
    # Wait for frontend to start
    Start-Sleep -Seconds 5
}

# Run backend API tests
Write-Host "`nRunning Backend API Tests" -ForegroundColor Cyan
Write-Host "------------------------" -ForegroundColor Cyan
Set-Location "$env:USERPROFILE\OneDrive\Desktop\Sentiment Analysis\backend"
python test_api.py

# Check model metrics
Write-Host "`nChecking Model Metrics" -ForegroundColor Cyan
Write-Host "------------------------" -ForegroundColor Cyan
Set-Location "$env:USERPROFILE\OneDrive\Desktop\Sentiment Analysis"
python model/check_metrics.py

# Run frontend tests
Write-Host "`nRunning Frontend Tests" -ForegroundColor Cyan
Write-Host "------------------------" -ForegroundColor Cyan
Set-Location "$env:USERPROFILE\OneDrive\Desktop\Sentiment Analysis\frontend"
npm test

# Clean up jobs if we started them
if ($startedBackend) {
    Stop-Job -Job $backendJob
    Remove-Job -Job $backendJob
    Write-Host "Stopped backend server" -ForegroundColor Yellow
}

if ($startedFrontend) {
    Stop-Job -Job $frontendJob
    Remove-Job -Job $frontendJob
    Write-Host "Stopped frontend server" -ForegroundColor Yellow
}

Write-Host "`nTesting completed!" -ForegroundColor Green
Write-Host "To run the application, use the run.ps1 script" -ForegroundColor Green 