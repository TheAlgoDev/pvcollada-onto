# PV-Collada Ontology (`pvcollada_onto.ttl`)

<p align="center">
  <a href="https://thealgodev.github.io/pvcollada-onto/webvowl/index.html">
    <img src="https://img.shields.io/badge/Visualize-WebVOWL-blue?style=flat-square" alt="WebVOWL" />
  </a>
  <a href="https://thealgodev.github.io/pvcollada-onto/">
    <img src="https://img.shields.io/badge/Docs-WIDOCO-green?style=flat-square" alt="WIDOCO Docs" />
  </a>
  <a href="https://creativecommons.org/licenses/by-sa/4.0/">
    <img src="https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey?style=flat-square" alt="License" />
  </a>
  <a href="https://www.w3.org/TR/owl2-overview/">
    <img src="https://img.shields.io/badge/OWL-2%20DL-orange?style=flat-square" alt="OWL 2 DL" />
  </a>
</p>

The PV-Collada Ontology is an OWL 2 vocabulary designed to formalize the representation of photovoltaic (PV) system components, electrical circuit topologies, and physical 3-D layouts. It provides a standardized semantic framework for modeling everything from inverter specifications to single-axis tracker geometries, enabling highly detailed and interoperable digital representations of solar assets. Derived directly from the PV-Collada 2.0 XML schema and formally aligned with [MDS-Onto](https://cwrusdle.bitbucket.io/mds/), it is designed as a FAIR-ready semantic backbone for advanced PV data science.

## Overview

| Field | Value |
|---|---|
| **Ontology IRI** | `https://w3id.org/pvcollada/` |
| **Persistent IRI** | [https://w3id.org/pvcollada](https://w3id.org/pvcollada) |
| **License** | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| **OWL Profile** | OWL 2 DL (Turtle serialisation) |
| **Alignment** | [MDS-Onto](https://cwrusdle.bitbucket.io/mds/) v0.3.1.31, [QUDT](http://qudt.org/), SKOS |
| **Triples** | ~1,367 |

## Documentation & Visualization

| Resource | Link |
|---|---|
| **Interactive graph (WebVOWL)** | [View ontology diagram](https://thealgodev.github.io/pvcollada-onto/webvowl/index.html) |
| **Full HTML documentation** | [WIDOCO docs](https://thealgodev.github.io/pvcollada-onto/) |
| **Provenance** | [provenance-en.html](https://thealgodev.github.io/pvcollada-onto/provenance/provenance-en.html) |
| **OOPS! evaluation** | [oopsEval.html](https://thealgodev.github.io/pvcollada-onto/OOPSevaluation/oopsEval.html) |
| **Persistent IRI** | [https://w3id.org/pvcollada](https://w3id.org/pvcollada) |

## Repository Structure

```
pvcollada-onto/
├── ontology/
│   ├── pvcollada_onto.ttl      # OWL 2 DL ontology (Turtle)
│   └── README.md               # Class / property reference
├── shapes/
│   └── pvcollada_shape.ttl     # SHACL NodeShapes for validation
├── queries/
│   └── cq01–cq10.rq            # Competency SPARQL queries
├── mcp/
│   ├── server.py               # Python MCP server (4 tools)
│   ├── requirements.txt
│   └── claude_desktop_config.json
├── sparql/
│   └── docker-compose.yml      # Oxigraph SPARQL endpoint
├── widoco-sections/            # Custom HTML sections injected into WIDOCO
├── docs/                       # Auto-generated WIDOCO documentation
├── w3id/
│   └── .htaccess               # Content-negotiation rules for w3id.org
└── .github/workflows/
    └── build-widoco-docs.yml   # CI: WIDOCO + WebVOWL + GitHub Pages
```

## Architecture

The ontology covers three interlocking layers:

| Layer | Root Classes | Description |
|---|---|---|
| **Product library** | `Module`, `Inverter`, `MPPTUnit`, `Cable`, `Combiner` | Typed component specs with STC parameters |
| **Circuit topology** | `String`, `InverterInstance`, `CircuitPosition` | Wiring relationships between components |
| **Physical layout** | `FixedTiltRack`, `TrackerRack`, `ModuleLayout` | 3-D geometry and georeferenced placement |

`ModuleLayout` is the cross-domain bridge that links a `CircuitPosition` (circuit layer) to a `Rack` (physical layer).

## MDS-Onto Alignment

| PV-Collada | Relation | MDS-Onto |
|---|---|---|
| `pvc:Module` | `rdfs:subClassOf` | `mds:PhotovoltaicModule` |
| `pvc:Inverter` | `rdfs:subClassOf` | `mds:Inverter` |
| `pvc:Rack` | `rdfs:subClassOf` | `mds:Racking` |
| `pvc:Project` | `rdfs:subClassOf` | `mds:PhotovoltaicSite` |
| `pvc:CellArchitecture` | `skos:closeMatch` | `mds:CellTechnology` |
| `pvc:RackType` | `skos:closeMatch` | `mds:RackingType` |
| `pvc:PERC` | `skos:exactMatch` | `mds:PassivatedEmitterRearCell` |

## Competency Queries

| Query | Description |
|---|---|
| [cq01](queries/cq01_list_all_classes.rq) | List all OWL classes with labels |
| [cq02](queries/cq02_module_electrical_params.rq) | Module STC electrical parameters |
| [cq03](queries/cq03_inverter_mppt_window.rq) | Inverter MPPT voltage windows |
| [cq04](queries/cq04_circuit_topology.rq) | Circuit topology (strings → inverters) |
| [cq05](queries/cq05_physical_layout_racks.rq) | Physical layout and rack geometry |
| [cq06](queries/cq06_cross_domain_bridge.rq) | Cross-domain bridge via ModuleLayout |
| [cq07](queries/cq07_mds_alignment.rq) | MDS-Onto aligned classes |
| [cq08](queries/cq08_bifacial_modules.rq) | Bifacial module configurations |
| [cq09](queries/cq09_temperature_coefficients.rq) | Temperature coefficient properties |
| [cq10](queries/cq10_project_capacity_summary.rq) | Project capacity summary |

## Quick Start

### Load into local SPARQL endpoint

```bash
cd sparql
docker compose up -d
# Load the ontology
curl -X POST http://localhost:7878/store \
  -H "Content-Type: text/turtle" \
  --data-binary @../ontology/pvcollada_onto.ttl
```

### Validate instance data

```bash
pip install pyshacl
pyshacl -s shapes/pvcollada_shape.ttl -o results.ttl your_data.ttl
```

### Use the MCP server with Claude

```bash
cd mcp
pip install -r requirements.txt
python server.py
```

Add `mcp/claude_desktop_config.json` to your Claude Desktop config to enable semantic search over the ontology.

## Using This Ontology

**FAIR data workflows** — the persistent `https://w3id.org/pvcollada/` IRI and content-negotiated `.htaccess` make every term dereferenceable and resolvable by RDF clients.

**Digital twins** — combine the circuit topology and physical layout layers to build georeferenced digital twins of operating PV plants.

**Interoperability** — the MDS-Onto alignment means PV-Collada data can be queried and reasoned over alongside materials science datasets in the broader MDS ecosystem.

**Extensibility** — add new component types by subclassing existing roots; SHACL shapes validate conformance automatically.
