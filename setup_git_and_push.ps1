# Git Setup and Push Script
# Run this script after installing Git

Write-Host "=== Git Setup and Push Script ===" -ForegroundColor Green
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "After installation, restart PowerShell and run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Configuring Git with your email..." -ForegroundColor Cyan
git config --global user.email "danyalkhalid764@gmail.com"

Write-Host "Please enter your name for Git commits: " -ForegroundColor Cyan -NoNewline
$userName = Read-Host
if ($userName) {
    git config --global user.name "$userName"
    Write-Host "Git configured with name: $userName" -ForegroundColor Green
}

Write-Host ""
Write-Host "Initializing Git repository..." -ForegroundColor Cyan
git init

Write-Host ""
Write-Host "Adding all files to Git..." -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "Creating initial commit..." -ForegroundColor Cyan
git commit -m "Initial commit: MyAIStudio project with Railway deployment setup"

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com and create a new repository" -ForegroundColor White
Write-Host "2. Copy the repository URL (e.g., https://github.com/username/repo-name.git)" -ForegroundColor White
Write-Host "3. Run the following commands:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin YOUR_REPOSITORY_URL" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Or provide your GitHub repository URL and I can help you push!" -ForegroundColor Green

