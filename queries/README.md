# Competency Queries

SPARQL 1.1 queries that test the competency of `pvcollada_onto.ttl`.
Each query is named `cqNN_description.rq`.

| File | Competency Question |
|------|---------------------|
| `cq01_list_all_classes.rq` | What classes does the ontology define? |
| `cq02_module_electrical_params.rq` | What are the STC electrical parameters of all module types? |
| `cq03_inverter_mppt_window.rq` | For each inverter, what is the MPPT voltage window per channel? |
| `cq04_circuit_topology.rq` | What is the full circuit topology (inverter → MPPT → string → array)? |
| `cq05_physical_layout_racks.rq` | What racks exist and what are their geometry parameters? |
| `cq06_cross_domain_bridge.rq` | Which modules occupy which rack slots? (circuit ↔ physical bridge) |
| `cq07_mds_alignment.rq` | How are pvc: terms aligned to MDS-Onto? |
| `cq08_bifacial_modules.rq` | Which modules are bifacial and what is their bifacial factor? |
| `cq09_temperature_coefficients.rq` | What temperature coefficients are defined for each module? |
| `cq10_project_capacity_summary.rq` | What is the system capacity and module count per project? |

## Running queries

**Local Oxigraph** (after `docker compose up -d` in `sparql/`):

```bash
curl -X POST http://localhost:7878/query \
     -H "Content-Type: application/sparql-query" \
     -H "Accept: application/sparql-results+json" \
     --data-binary @queries/cq07_mds_alignment.rq | python -m json.tool
```

**RDFLib** (no server needed):

```python
import rdflib, json

g = rdflib.Graph()
g.parse("ontology/pvcollada_onto.ttl", format="turtle")

with open("queries/cq07_mds_alignment.rq") as f:
    q = f.read()

for row in g.query(q):
    print(row)
```
