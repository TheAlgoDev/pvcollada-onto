# PV-Collada Ontology (`pvcollada_onto.ttl`)

<p align="center">
  <img src="assets/logo.png" alt="PV-Collada Ontology logo" width="150" />
</p>

The PV-Collada Ontology is an OWL 2 vocabulary designed to formalize the representation of photovoltaic (PV) system components, electrical circuit topologies, and physical 3-D layouts. It provides a standardized semantic framework for modeling everything from inverter specifications to single-axis tracker geometries, enabling highly detailed and interoperable digital representations of solar assets. Derived directly from the PV-Collada 2.0 XML schema and formally aligned with [MDS-Onto](https://cwrusdle.bitbucket.io/mds/), it is designed as a FAIR-ready semantic backbone for advanced PV data science.

## Overview

- **Ontology IRI:** `https://cwrusdle.bitbucket.io/mds/builtenv/pvcollada/`
- **Persistent IRI:** [https://w3id.org/pvcollada](https://w3id.org/pvcollada)
- **License:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **OWL Profile:** OWL 2 DL (Turtle serialisation)
- **Imports / Alignment:** [MDS-Onto](https://cwrusdle.bitbucket.io/mds/) v0.3.1.31, [QUDT](http://qudt.org/), SKOS

## Repository structure

- Ontology: [ontology/pvcollada_onto.ttl](ontology/pvcollada_onto.ttl)
- Ontology documentation: [ontology/README.md](ontology/README.md)
- SHACL shape constraints: [shapes/pvcollada_shape.ttl](shapes/pvcollada_shape.ttl)
- Competency queries (SPARQL): [queries/](queries/)
- WIDOCO documentation (auto-generated): [docs/index.html](docs/index.html)
- Local SPARQL endpoint (Oxigraph): [sparql/](sparql/)
- MCP server for Claude agent integration: [mcp/](mcp/)
- w3id.org persistent namespace config: [w3id/](w3id/)

## Documentation

- **Main docs page:** [https://thealgodev.github.io/pvcollada-onto/](https://thealgodev.github.io/pvcollada-onto/)
- **WebVOWL visualization:** [https://thealgodev.github.io/pvcollada-onto/webvowl/index.html](https://thealgodev.github.io/pvcollada-onto/webvowl/index.html)
- **Provenance report:** [https://thealgodev.github.io/pvcollada-onto/provenance/provenance-en.html](https://thealgodev.github.io/pvcollada-onto/provenance/provenance-en.html)

## Architecture

The ontology mirrors the three-layer PV-Collada data model:

| Layer | Class root | Description |
|-------|-----------|-------------|
| **Product library** | `pvc:PVComponent` | Typed component specifications — modules, inverters, cables, transformers, combiners, optimizers |
| **Circuit topology** | `pvc:CircuitInstance` | Instantiated electrical network — strings, arrays, MPPT inputs, inverter/combiner instances, cable connections |
| **Physical layout** | `pvc:PhysicalAsset` | 3-D geometric installation — racks, tables, posts, gaps, terrain mesh (COLLADA scene graph) |

`pvc:ModuleLayout` is the **cross-domain bridge**: it maps a module's electrical position in a circuit string directly to its physical row/column slot on a geometric rack, enabling combined electrical and spatial queries — for example, tracing the electrical impact of localized shading on a specific rack geometry.

## Schema heritage

The ontology's ground truth is sourced directly from operational PV design software schemas rather than constructed from scratch:

- **`pvcollada_schema_2.0.xsd`** — primary schema; drives all classes, data properties, and enumerations
- **`pvcollada_business_2.0.sch`** — conditional field rules (e.g. `FixedTiltRack` must carry `azimuth` + `tilt`; `TrackerRack` must not) re-expressed as OWL 2 subclass restrictions and SHACL shapes
- **`pvcollada_references_2.0.sch`** — reference-integrity rules for circuit-to-component IDREF links

XSD `simpleType` enumerations (cell technology, rack type, inverter type, etc.) are modelled as `owl:Class` + `owl:oneOf` named individuals so that each member can carry its own alignment and annotation links.

## MDS-Onto alignment

The ontology is a sub-domain module of MDS-Onto (`mds:builtenv`). Alignment with MDS-Onto v0.3.1.31 contextualises PV-Collada data within a broader cross-disciplinary knowledge base, connecting solar simulation data to materials science, built environment, and environmental measurement ontologies.

| `pvc:` term | Relation | `mds:` term |
|-------------|----------|-------------|
| `pvc:Module` | `rdfs:subClassOf` | `mds:PhotovoltaicModule` |
| `pvc:Inverter` | `rdfs:subClassOf` | `mds:Inverter` |
| `pvc:Rack` | `rdfs:subClassOf` | `mds:Racking` |
| `pvc:Project` | `rdfs:subClassOf` | `mds:PhotovoltaicSite` |
| `pvc:PERC` | `skos:exactMatch` | `mds:PassivatedEmitterRearCell` |
| `pvc:CellArchitecture` | `skos:closeMatch` | `mds:CellTechnology`, `mds:CellTechnologyType` |
| `pvc:nomPower` … `pvc:manufacturer` | `rdfs:seeAlso` | corresponding `mds:` measurement classes |

See [queries/cq07_mds_alignment.rq](queries/cq07_mds_alignment.rq) for a SPARQL query that returns all alignment triples.

## Competency queries

The [queries/](queries/) folder contains 10 SPARQL competency queries (CQ01–CQ10) covering class listing, STC electrical parameters, MPPT voltage windows, full circuit topology traversal, physical rack layout, the circuit↔physical cross-domain bridge, MDS-Onto alignment, bifacial modules, temperature coefficients, and project capacity summary. See [queries/README.md](queries/README.md) for usage examples with both Oxigraph and RDFLib.

## Quick start

```bash
# 1 — Start the local SPARQL triplestore
cd sparql/
docker compose up -d          # loads ontology into Oxigraph at localhost:7878

# 2 — Install and run the MCP server (for Claude agent integration)
cd ../mcp/
pip install -r requirements.txt
python server.py
```

See [sparql/README.md](sparql/README.md) and [mcp/README.md](mcp/README.md) for full details.

## Using this ontology

**FAIR data workflows.** By translating rigid software schemas into OWL 2, the ontology is explicitly designed to support FAIR (Findable, Accessible, Interoperable, Reusable) computational workflows, allowing disparate research and operational teams to query PV measurement and layout data using a shared, machine-readable vocabulary.

**Digital twins and knowledge graphs.** The tri-layer architecture (Products → Circuits → Layouts) and the `pvc:ModuleLayout` bridge support the construction of comprehensive digital twins of solar power plants, enabling complex cross-layer queries that combine electrical simulation data with 3-D spatial analysis.

**Extensibility.** Because the ontology is rooted in MDS-Onto, `pvc:` instances can be seamlessly linked to broader environmental, meteorological, or economic ontologies without modifying core PV definitions.

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — consistent with MDS-Onto upstream.
