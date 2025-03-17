Write-Host "Committing and pushing deployment configuration changes" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if Git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed. Please install Git and try again." -ForegroundColor Red
    exit 1
}

# Add the modified files
Write-Host "Adding modified files to Git..." -ForegroundColor Cyan
git add backend/app.py render.yaml Procfile vercel.json frontend/.env.production

# Commit the changes
$commitMessage = "Update configuration for Render and Vercel deployment"
Write-Host "Committing changes: $commitMessage" -ForegroundColor Cyan
git commit -m $commitMessage

# Push to GitHub
Write-Host "Pushing changes to GitHub..." -ForegroundColor Cyan
git push origin main

Write-Host "Changes pushed successfully!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to Render.com and deploy your backend" -ForegroundColor Yellow
Write-Host "2. Go to Vercel.com and deploy your frontend" -ForegroundColor Yellow
Write-Host "3. Make sure to set up the environment variables on both platforms" -ForegroundColor Yellow 