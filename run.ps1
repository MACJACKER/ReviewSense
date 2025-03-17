# Run both backend and frontend for the Sentiment Analysis Application

Write-Host "Starting Sentiment Analysis Application" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Start backend server
$backendJob = Start-Job -ScriptBlock {
    Set-Location "$env:USERPROFILE\OneDrive\Desktop\Sentiment Analysis\backend"
    Write-Host "Starting backend server..." -ForegroundColor Cyan
    uvicorn main:app --reload
}

Write-Host "Backend server starting..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Start frontend server
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "$env:USERPROFILE\OneDrive\Desktop\Sentiment Analysis\frontend"
    Write-Host "Starting frontend server..." -ForegroundColor Cyan
    npm run dev
}

Write-Host "Frontend server starting..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

Write-Host "`nBoth servers are now running!" -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop both servers" -ForegroundColor Yellow

try {
    # Keep the script running until Ctrl+C is pressed
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    # Clean up when script is interrupted
    Write-Host "`nStopping servers..." -ForegroundColor Yellow
    
    Stop-Job -Job $backendJob
    Remove-Job -Job $backendJob
    
    Stop-Job -Job $frontendJob
    Remove-Job -Job $frontendJob
    
    Write-Host "Servers stopped." -ForegroundColor Green
} 