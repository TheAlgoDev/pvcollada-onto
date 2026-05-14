Set-Location "C:\Users\brent\dev\pv_onto\pv ontology\pvcollada-onto"
git config user.name "TheAlgoDev"
git config user.email "thompsonsolutionscompany@gmail.com"

$s = "C:\Users\brent\dev\pv_onto\pv ontology"
$d = "C:\Users\brent\dev\pv_onto\pv ontology\pvcollada-onto"

New-Item -ItemType Directory -Force "$d\ontology" | Out-Null
New-Item -ItemType Directory -Force "$d\sparql" | Out-Null
New-Item -ItemType Directory -Force "$d\mcp" | Out-Null
New-Item -ItemType Directory -Force "$d\shapes" | Out-Null
New-Item -ItemType Directory -Force "$d\queries" | Out-Null
New-Item -ItemType Directory -Force "$d\widoco-sections" | Out-Null
New-Item -ItemType Directory -Force "$d\.github\workflows" | Out-Null
New-Item -ItemType Directory -Force "$d\docs" | Out-Null
New-Item -ItemType Directory -Force "$d\w3id" | Out-Null

Copy-Item -Force "$s\README.md"                                   "$d\README.md"
Copy-Item -Force "$s\ontology\pvcollada_onto.ttl"                 "$d\ontology\pvcollada_onto.ttl"
Copy-Item -Force "$s\ontology\README.md"                          "$d\ontology\README.md"
Copy-Item -Force "$s\sparql\docker-compose.yml"                   "$d\sparql\docker-compose.yml"
Copy-Item -Force "$s\sparql\README.md"                            "$d\sparql\README.md"
Copy-Item -Force "$s\mcp\server.py"                               "$d\mcp\server.py"
Copy-Item -Force "$s\mcp\requirements.txt"                        "$d\mcp\requirements.txt"
Copy-Item -Force "$s\mcp\claude_desktop_config.json"              "$d\mcp\claude_desktop_config.json"
Copy-Item -Force "$s\mcp\README.md"                               "$d\mcp\README.md"
Copy-Item -Force "$s\shapes\pvcollada_shape.ttl"                  "$d\shapes\pvcollada_shape.ttl"
Copy-Item -Force "$s\queries\README.md"                           "$d\queries\README.md"
Copy-Item -Force "$s\queries\cq01_list_all_classes.rq"            "$d\queries\cq01_list_all_classes.rq"
Copy-Item -Force "$s\queries\cq02_module_electrical_params.rq"    "$d\queries\cq02_module_electrical_params.rq"
Copy-Item -Force "$s\queries\cq03_inverter_mppt_window.rq"        "$d\queries\cq03_inverter_mppt_window.rq"
Copy-Item -Force "$s\queries\cq04_circuit_topology.rq"            "$d\queries\cq04_circuit_topology.rq"
Copy-Item -Force "$s\queries\cq05_physical_layout_racks.rq"       "$d\queries\cq05_physical_layout_racks.rq"
Copy-Item -Force "$s\queries\cq06_cross_domain_bridge.rq"         "$d\queries\cq06_cross_domain_bridge.rq"
Copy-Item -Force "$s\queries\cq07_mds_alignment.rq"               "$d\queries\cq07_mds_alignment.rq"
Copy-Item -Force "$s\queries\cq08_bifacial_modules.rq"            "$d\queries\cq08_bifacial_modules.rq"
Copy-Item -Force "$s\queries\cq09_temperature_coefficients.rq"    "$d\queries\cq09_temperature_coefficients.rq"
Copy-Item -Force "$s\queries\cq10_project_capacity_summary.rq"    "$d\queries\cq10_project_capacity_summary.rq"
Copy-Item -Force "$s\widoco-sections\abstract-en.html"            "$d\widoco-sections\abstract-en.html"
Copy-Item -Force "$s\widoco-sections\introduction-en.html"        "$d\widoco-sections\introduction-en.html"
Copy-Item -Force "$s\widoco-sections\description-en.html"         "$d\widoco-sections\description-en.html"
Copy-Item -Force "$s\widoco-sections\references-en.html"          "$d\widoco-sections\references-en.html"
Copy-Item -Force "$s\.github\workflows\build-widoco-docs.yml"     "$d\.github\workflows\build-widoco-docs.yml"
Copy-Item -Force "$s\docs\index.html"                             "$d\docs\index.html"
Copy-Item -Force "$s\w3id\.htaccess"                              "$d\w3id\.htaccess"
Copy-Item -Force "$s\w3id\METADATA.md"                            "$d\w3id\METADATA.md"

New-Item -ItemType File -Force "$d\docs\.nojekyll" | Out-Null

Write-Host "Files copied. Staging..." -ForegroundColor Cyan
git add .
git status
git commit -m "feat: add complete project structure"
git push origin main
Write-Host "Done." -ForegroundColor Green
