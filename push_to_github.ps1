# Push to GitHub Script
# Repository: https://github.com/danyalkhalid764-wq/myaistudio.git
# Email: danyalkhalid764@gmail.com

Write-Host "=== Pushing MyAIStudio to GitHub ===" -ForegroundColor Green
Write-Host "Repository: https://github.com/danyalkhalid764-wq/myaistudio.git" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version 2>&1
    Write-Host "Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git first:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "2. Run the installer with default settings" -ForegroundColor White
    Write-Host "3. RESTART PowerShell after installation" -ForegroundColor White
    Write-Host "4. Run this script again" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "Configuring Git..." -ForegroundColor Cyan
git config --global user.email "danyalkhalid764@gmail.com"

# Get user name if not set
$currentName = git config --global user.name
if (-not $currentName) {
    Write-Host "Please enter your name for Git commits: " -ForegroundColor Cyan -NoNewline
    $userName = Read-Host
    if ($userName) {
        git config --global user.name "$userName"
        Write-Host "Git configured with name: $userName" -ForegroundColor Green
    }
} else {
    Write-Host "Git already configured with name: $currentName" -ForegroundColor Green
}

Write-Host ""
Write-Host "Initializing Git repository..." -ForegroundColor Cyan
if (Test-Path .git) {
    Write-Host "Git repository already initialized" -ForegroundColor Yellow
} else {
    git init
    Write-Host "Git repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "Adding all files to Git..." -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "Checking for changes..." -ForegroundColor Cyan
$status = git status --porcelain
if ($status) {
    Write-Host "Creating initial commit..." -ForegroundColor Cyan
    git commit -m "Initial commit: MyAIStudio project with Railway deployment setup"
    Write-Host "Commit created successfully!" -ForegroundColor Green
} else {
    Write-Host "No changes to commit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setting up remote repository..." -ForegroundColor Cyan
$remoteUrl = "https://github.com/danyalkhalid764-wq/myaistudio.git"

# Check if remote already exists
$existingRemote = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote 'origin' already exists: $existingRemote" -ForegroundColor Yellow
    Write-Host "Updating remote URL..." -ForegroundColor Cyan
    git remote set-url origin $remoteUrl
} else {
    git remote add origin $remoteUrl
    Write-Host "Remote 'origin' added: $remoteUrl" -ForegroundColor Green
}

Write-Host ""
Write-Host "Setting branch to 'main'..." -ForegroundColor Cyan
git branch -M main

Write-Host ""
Write-Host "=== Ready to Push ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "Now pushing to GitHub..." -ForegroundColor Cyan
Write-Host "Note: You may be prompted for authentication" -ForegroundColor Yellow
Write-Host ""
Write-Host "If prompted for credentials:" -ForegroundColor Yellow
Write-Host "  Username: danyalkhalid764-wq" -ForegroundColor White
Write-Host "  Password: Use a Personal Access Token (NOT your GitHub password)" -ForegroundColor White
Write-Host ""
Write-Host "To create a Personal Access Token:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "  2. Generate new token (classic)" -ForegroundColor White
Write-Host "  3. Select 'repo' permissions" -ForegroundColor White
Write-Host "  4. Copy the token and use it as your password" -ForegroundColor White
Write-Host ""

# Try to push
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== SUCCESS! ===" -ForegroundColor Green
    Write-Host "Your code has been pushed to GitHub!" -ForegroundColor Green
    Write-Host "Repository: https://github.com/danyalkhalid764-wq/myaistudio" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Go to Railway.app and connect your GitHub repository" -ForegroundColor White
    Write-Host "2. Deploy the backend to Railway" -ForegroundColor White
    Write-Host "3. See RAILWAY_DEPLOYMENT.md for detailed instructions" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "=== Push Failed ===" -ForegroundColor Red
    Write-Host "Please check the error message above" -ForegroundColor Yellow
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  - Authentication failed: Use Personal Access Token" -ForegroundColor White
    Write-Host "  - Network issues: Check your internet connection" -ForegroundColor White
    Write-Host "  - Repository permissions: Make sure you have write access" -ForegroundColor White
}




