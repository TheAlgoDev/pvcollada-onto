# PV-Collada Ontology (pvcollada_onto.ttl)
Welcome to the PV-Collada Ontology, an OWL 2 vocabulary designed to formalize the representation of photovoltaic (PV) system components, electrical circuit topologies, and physical 3-D layouts.

This ontology provides a standardized semantic framework for modeling everything from inverter specifications to single-axis tracker geometries, enabling highly detailed and interoperable digital representations of solar assets.

Sourcing Truth from Software Schemas
A core strength of the PV-Collada Ontology is its direct derivation from established software specifications. Rather than creating a conceptual model from scratch, this ontology sources its "ground truth" directly from the operational files used in PV design and simulation software:

XSD & Schematron Heritage: The ontology is directly derived from pvcollada_schema_2.0.xsd, pvcollada_business_2.0.sch, and pvcollada_references_2.0.sch.

Data Structure Alignment: By aligning with the PV-Collada 2.0 XML schema, the ontology ensures that data structures native to engineering software are accurately preserved and semantically enriched for knowledge graph applications.

Conditional Logic as Restrictions: Complex business rules from Schematron (e.g., ensuring a FixedTiltRack has azimuth and tilt but no tracker fields) are elegantly modeled as OWL 2 subclass restrictions, maintaining data integrity at the semantic level.

The Bigger Picture: MDS-Onto Integration
The PV-Collada Ontology does not operate in isolation. It is intentionally designed as a sub-domain (pvc:) within the broader Metadata Standards (MDS) Ontology framework (mds:).

Connecting to the MDS-Onto framework provides a massive advantage by integrating highly specific PV simulation data into a comprehensive, cross-disciplinary knowledge base:

Domain Mapping: PV-Collada operates within the mds:builtenv (Built Environment) domain, contextualizing solar installations as integrated infrastructure assets.

Class Hierarchy Bridges: Core PV-Collada classes map directly to MDS parent classes. For example, pvc:Module is a subclass of mds:PhotovoltaicModule, and pvc:Project is a subclass of mds:PhotovoltaicSite.

Semantic Equivalency: Specific technologies, such as the pvc:PERC cell architecture, are linked via exact matches (skos:exactMatch) to their MDS-Onto counterparts (mds:PassivatedEmitterRearCell).

Measurement Alignment: Data properties for technical specifications (like nominal power, short-circuit current, and temperature coefficients) utilize rdfs:seeAlso to link directly to established MDS measurement classes, ensuring consistency in how physical metrics are queried and understood across different scientific applications.

Core Architecture
The ontology is structured around three interlocking semantic layers:

Product Library (pvc:PVComponent): Typed specifications for physical balance-of-system components (e.g., Modules, Inverters, Cables, Transformers).

Circuit Topology (pvc:CircuitInstance): The instantiated electrical network describing how components are wired together (Strings, Arrays, MPPT Inputs).

Physical Layout (pvc:PhysicalAsset): The 3-D geometric reality of the installation, tracking Racks, Tables, Posts, and Terrain.

The Bridge Entity: The pvc:ModuleLayout class serves as the critical cross-domain bridge, mapping a module's electrical position in a circuit string directly to its physical row/column slot on a geometric rack.

Note on Ontology Use
This ontology is built to serve as the semantic backbone for advanced PV data science. When implementing pvcollada_onto.ttl in your data stacks, keep the following in mind:

FAIR Data Workflows: By translating rigid software schemas into OWL 2, this ontology is explicitly designed to support the development of FAIR (Findable, Accessible, Interoperable, Reusable) computational workflows. It allows disparate research and operational teams to query PV measurement and layout data using a shared, machine-readable vocabulary.

Digital Twins & Knowledge Graphs: Use the tri-layer architecture (Products, Circuits, Layouts) to construct comprehensive digital twins of solar power plants. The explicit bridging between the electrical topology and the physical 3D scene graph allows for complex querying, such as analyzing the electrical impact of localized physical shading on specific rack geometries.

Extensibility: Because it is rooted in the MDS-Onto framework, you can seamlessly extend this vocabulary by linking pvc: instances to broader environmental, meteorological, or economic ontologies without breaking the core PV definitions.

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — consistent
with MDS-Onto upstream.
# PV-Collada Ontology

OWL 2 ontology derived from the [PV-Collada 2.0](http://www.example.com/pvcollada)
XML schema, aligned with [MDS-Onto](https://cwrusdle.bitbucket.io/mds/).

Covers the three-layer PV-Collada data model:

| Layer | Description |
|-------|-------------|
| **Product library** | Typed component specifications (modules, inverters, cables, …) |
| **Circuit topology** | Electrical wiring: strings → MPPT inputs → inverters → transformers |
| **Physical layout** | 3-D rack geometry, tables, posts, terrain (COLLADA scene graph) |

## Namespace

```
https://cwrusdle.bitbucket.io/mds/builtenv/pvcollada/
```

Persistent IRI: **https://w3id.org/pvcollada** (redirects to `ontology/pvcollada_onto.ttl`)

## Repository layout

```
ontology/          OWL 2 Turtle source
sparql/            Docker Compose for local Oxigraph SPARQL endpoint
mcp/               Python MCP server (4 tools for Claude agents)
```

## Quick start

```bash
# 1 — Start the SPARQL triplestore
cd sparql/
docker compose up -d

# 2 — Install and run the MCP server
cd ../mcp/
pip install -r requirements.txt
python server.py
```

See `sparql/README.md` and `mcp/README.md` for full details.

## MDS-Onto alignment

Key class bridges:

| pvc: class | MDS-Onto parent |
|-----------|----------------|
| `pvc:Module` | `mds:PhotovoltaicModule` |
| `pvc:Inverter` | `mds:Inverter` |
| `pvc:Rack` | `mds:Racking` |
| `pvc:Project` | `mds:PhotovoltaicSite` |
