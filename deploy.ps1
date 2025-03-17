Write-Host "Sentiment Analysis Deployment Script" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if Git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed. Please install Git and try again." -ForegroundColor Red
    exit 1
}

# Check if Git LFS is installed
$gitLfsCheck = git lfs install 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Git LFS is not installed. Please install Git LFS and try again." -ForegroundColor Red
    Write-Host "You can download it from: https://git-lfs.github.com/" -ForegroundColor Yellow
    exit 1
}

# Initialize Git LFS
Write-Host "Initializing Git LFS..." -ForegroundColor Cyan
git lfs install

# Initialize Git repository if not already initialized
if (!(Test-Path .git)) {
    Write-Host "Initializing Git repository..." -ForegroundColor Cyan
    git init
}

# Track large files with Git LFS
Write-Host "Tracking large model files with Git LFS..." -ForegroundColor Cyan
git lfs track "*.bin"
git lfs track "*.safetensors"
git lfs track "model/fine_tuned_model/model.safetensors"

# Add all files to Git
Write-Host "Adding files to Git..." -ForegroundColor Cyan
git add .

# Commit changes
$commitMessage = Read-Host "Enter commit message (default: 'Prepare for deployment')"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Prepare for deployment"
}
git commit -m $commitMessage

# Ask for GitHub repository URL
$repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git)"
if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "GitHub repository URL is required." -ForegroundColor Red
    exit 1
}

# Add remote and push
Write-Host "Adding remote repository..." -ForegroundColor Cyan
git remote add origin $repoUrl
Write-Host "Pushing to GitHub (this may take a while due to large model files)..." -ForegroundColor Cyan
git push -u origin main

Write-Host "GitHub repository setup complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to Render.com and connect your GitHub repository" -ForegroundColor Yellow
Write-Host "2. Create a new Web Service with the settings from the README.md" -ForegroundColor Yellow
Write-Host "3. Go to Vercel.com and connect your GitHub repository" -ForegroundColor Yellow
Write-Host "4. Configure the Vercel project with the settings from the README.md" -ForegroundColor Yellow
Write-Host "5. Once both deployments are complete, update the frontend environment variable VITE_API_URL with your Render backend URL" -ForegroundColor Yellow 