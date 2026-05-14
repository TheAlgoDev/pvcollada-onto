# Push updated workflow only
# Run from pvcollada-onto\: .\push_workflow_fix.ps1

$ErrorActionPreference = "Stop"
$repoDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceDir = Split-Path -Parent $repoDir

Set-Location $repoDir
git config user.name  "TheAlgoDev"
git config user.email "thompsonsolutionscompany@gmail.com"

# Copy updated workflow from parent workspace
$src = Join-Path $sourceDir ".github\workflows\build-widoco-docs.yml"
$dst = Join-Path $repoDir   ".github\workflows\build-widoco-docs.yml"
New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
Copy-Item -Force $src $dst
Write-Host "Copied workflow" -ForegroundColor DarkGray

git add .github/workflows/build-widoco-docs.yml
git status

$msg = @'
fix: switch Pages to GitHub Actions deployment; add deploy-pages job

Changes:
- Pages source is now GitHub Actions (no more Jekyll auto-build errors)
- Added upload-pages-artifact + deploy-pages steps after WIDOCO build
- Added pages/id-token permissions required for Pages deployment
- Added concurrency group to prevent overlapping deployments
- FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 suppresses Node 20 deprecation warning
- Simplified section injection loop
'@

git commit -m $msg
git push origin main

Write-Host ""
Write-Host "Done. Go to Actions and run the workflow manually to trigger first build:" -ForegroundColor Green
Write-Host "https://github.com/TheAlgoDev/pvcollada-onto/actions" -ForegroundColor Cyan
