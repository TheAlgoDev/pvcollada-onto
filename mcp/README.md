# PV-Collada MCP Server

An [MCP](https://modelcontextprotocol.io) server that exposes the
`pvcollada_onto.ttl` ontology as four Claude-callable tools, backed by a
local Oxigraph SPARQL endpoint.

## Tools

| Tool | Description |
|------|-------------|
| `lookup_term(label)` | Find classes/properties by partial label |
| `get_class_hierarchy(class_iri)` | Walk subClassOf chain + list subclasses |
| `get_properties_for_class(class_iri)` | All domain-scoped properties with units |
| `get_mds_alignment(term_iri)` | MDS-Onto subClassOf / closeMatch / seeAlso links |

## Prerequisites

1. Oxigraph running locally — see `../sparql/README.md`
2. Python 3.10+

## Install

```bash
cd mcp/
pip install -r requirements.txt
```

## Run (standalone test)

```bash
python server.py
```

## Connect to Claude Desktop

1. Open `claude_desktop_config.json` in this folder.
2. Copy the `"pvcollada"` block into your Claude Desktop config file:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
3. Update `PATH_TO_REPO` to the absolute path of this repository.
4. Restart Claude Desktop.

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OXIGRAPH_URL` | `http://localhost:7878` | Base URL of the Oxigraph instance |

## Example usage in Claude

```
Look up the term "rack" in the pvcollada ontology.
Show me the class hierarchy for pvc:Module.
What properties are scoped to pvc:Inverter?
What MDS-Onto classes does pvc:Module align with?
```
