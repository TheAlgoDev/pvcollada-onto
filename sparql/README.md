# PV-Collada SPARQL Endpoint (Local)

Runs [Oxigraph](https://github.com/oxigraph/oxigraph) locally via Docker Compose,
serving `pvcollada_onto.ttl` as a SPARQL 1.1 endpoint.

## Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin)

## Start

```bash
cd sparql/
docker compose up -d
```

The SPARQL endpoint is available at **http://localhost:7878**

| Path | Description |
|------|-------------|
| `GET /query?query=...` | SPARQL SELECT / ASK / CONSTRUCT |
| `POST /query` | SPARQL query (body: `application/sparql-query`) |
| `GET /` | Oxigraph web UI |

## Reload ontology after edits

```bash
docker compose restart loader
```

Or manually:

```bash
curl -X POST http://localhost:7878/store?graph=https://w3id.org/pvcollada/ \
  -H "Content-Type: text/turtle" \
  --data-binary @../ontology/pvcollada_onto.ttl
```

## Stop

```bash
docker compose down          # keep data volume
docker compose down -v       # also wipe data (forces full reload on next start)
```

## Example query

```sparql
PREFIX pvc: <https://w3id.org/pvcollada/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?class ?label WHERE {
  ?class a owl:Class ;
         rdfs:label ?label .
}
ORDER BY ?label
```
