# Copy all built files from parent workspace into this git repo, then push.
# Run from this folder: .\push_everything.ps1

$ErrorActionPreference = "Stop"

$repoDir   = Split-Path -Parent $MyInvocation.MyCommand.Path   # …/pvcollada-onto
$sourceDir = Split-Path -Parent $repoDir                        # …/pv ontology

Write-Host "Repo  : $repoDir"   -ForegroundColor Cyan
Write-Host "Source: $sourceDir" -ForegroundColor Cyan

Set-Location $repoDir

git config user.name  "TheAlgoDev"
git config user.email "thompsonsolutionscompany@gmail.com"

# ── Copy files from parent workspace into this repo ───────────────────────────

function CopyIn($rel) {
    $src = Join-Path $sourceDir $rel
    $dst = Join-Path $repoDir   $rel
    if (-not (Test-Path $src)) { Write-Host "SKIP (not found): $rel" -ForegroundColor DarkGray; return }
    $dstDir = Split-Path $dst -Parent
    if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Force $dstDir | Out-Null }
    Copy-Item -Force $src $dst
    Write-Host "  copied: $rel" -ForegroundColor DarkGray
}

function CopyDirIn($rel) {
    $src = Join-Path $sourceDir $rel
    $dst = Join-Path $repoDir   $rel
    if (-not (Test-Path $src)) { Write-Host "SKIP dir (not found): $rel" -ForegroundColor DarkGray; return }
    if (-not (Test-Path $dst)) { New-Item -ItemType Directory -Force $dst | Out-Null }
    Copy-Item -Recurse -Force "$src\*" $dst
    Write-Host "  copied dir: $rel" -ForegroundColor DarkGray
}

Write-Host "Copying files..." -ForegroundColor Cyan

CopyIn  "README.md"
CopyIn  "ontology\pvcollada_onto.ttl"
CopyIn  "ontology\README.md"
CopyIn  "sparql\docker-compose.yml"
CopyIn  "sparql\README.md"
CopyIn  "mcp\server.py"
CopyIn  "mcp\requirements.txt"
CopyIn  "mcp\claude_desktop_config.json"
CopyIn  "mcp\README.md"
CopyIn  "shapes\pvcollada_shape.ttl"
CopyDirIn "queries"
CopyDirIn "widoco-sections"
CopyIn  ".github\workflows\build-widoco-docs.yml"
CopyIn  "docs\.nojekyll"
CopyIn  "docs\index.html"
CopyIn  "w3id\.htaccess"
CopyIn  "w3id\METADATA.md"

# ── Stage and commit ──────────────────────────────────────────────────────────

Write-Host "Staging..." -ForegroundColor Cyan
git add .

git status

$staged = git diff --cached --name-only
if (-not $staged) {
    Write-Host "Nothing new to commit — already up to date." -ForegroundColor Yellow
    exit 0
}

$msg = @'
feat: add complete project structure

ontology/pvcollada_onto.ttl  OWL 2 DL, 1367 triples, MDS-Onto aligned
ontology/README.md           full class/property/enumeration reference
sparql/                      Oxigraph Docker Compose endpoint
mcp/                         Python MCP server, 4 SPARQL-backed tools
shapes/pvcollada_shape.ttl   SHACL NodeShapes for all key classes
queries/cq01-cq10            10 SPARQL competency queries
widoco-sections/             custom abstract, intro, description, references
.github/workflows/           WIDOCO CI with OOPS, WebVOWL, auto-commit
docs/.nojekyll               static Pages placeholder, no Jekyll
w3id/                        content-negotiation redirect config
README.md                    FAIR-O style with WebVOWL and provenance links
'@
git commit -m $msg

# ── Push ─────────────────────────────────────────────────────────────────────

Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push origin main

Write-Host ""
Write-Host "Done! Repo is live at:" -ForegroundColor Green
Write-Host "https://github.com/TheAlgoDev/pvcollada-onto" -ForegroundColor Cyan
Write-Host ""
Write-Host "Trigger the WIDOCO build at:" -ForegroundColor Yellow
Write-Host "https://github.com/TheAlgoDev/pvcollada-onto/actions" -ForegroundColor Cyan
