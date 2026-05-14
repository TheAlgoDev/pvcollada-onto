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

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — consistent
with MDS-Onto upstream.
