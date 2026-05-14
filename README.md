# PV-Collada Ontology (`pvcollada_onto.ttl`)

<p align="center">
  <img src="assets/logo.png" alt="PV-Collada Ontology logo" width="150" />
</p>

The PV-Collada Ontology is an OWL 2 vocabulary designed to formalize the representation of photovoltaic (PV) system components, electrical circuit topologies, and physical 3-D layouts. It provides a standardized semantic framework for modeling everything from inverter specifications to single-axis tracker geometries, enabling highly detailed and interoperable digital representations of solar assets. Derived directly from the PV-Collada 2.0 XML schema and formally aligned with [MDS-Onto](https://cwrusdle.bitbucket.io/mds/), it is designed as a FAIR-ready semantic backbone for advanced PV data science.

## Overview

- **Ontology IRI:** `https://w3id.org/pvcollada/`
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
- Local SPARQL endpoint 