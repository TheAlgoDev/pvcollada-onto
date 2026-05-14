"""
PV-Collada MCP Server
=====================
Exposes the pvcollada_onto.ttl ontology as four Claude-callable tools
via an Oxigraph SPARQL endpoint (default: http://localhost:7878).

Tools
-----
lookup_term            – find a class or property by label / partial label
get_class_hierarchy    – walk rdfs:subClassOf chain for a given IRI
get_properties_for_class – list all data/object properties scoped to a class
get_mds_alignment      – return MDS-Onto links (subClassOf / closeMatch / seeAlso)

Usage (stdio transport for Claude Desktop)
------------------------------------------
  python server.py

Claude Desktop claude_desktop_config.json entry:
  {
    "pvcollada": {
      "command": "python",
      "args": ["/path/to/mcp/server.py"],
      "env": { "OXIGRAPH_URL": "http://localhost:7878" }
    }
  }
"""

import os
import json
import urllib.parse
import urllib.request
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OXIGRAPH_URL = os.getenv("OXIGRAPH_URL", "http://localhost:7878")
SPARQL_ENDPOINT = f"{OXIGRAPH_URL}/query"

PVC = "https://cwrusdle.bitbucket.io/mds/builtenv/pvcollada/"
MDS = "https://cwrusdle.bitbucket.io/mds/"

PREFIXES = f"""
PREFIX pvc:  <{PVC}>
PREFIX mds:  <{MDS}>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
"""

# ---------------------------------------------------------------------------
# SPARQL helper
# ---------------------------------------------------------------------------

def sparql(query: str) -> list[dict]:
    """Run a SPARQL SELECT against Oxigraph; return list of binding dicts."""
    full_query = PREFIXES + query
    data = urllib.parse.urlencode({"query": full_query}).encode()
    req = urllib.request.Request(
        SPARQL_ENDPOINT,
        data=data,
        headers={"Accept": "application/sparql-results+json",
                 "Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
        return [
            {k: v["value"] for k, v in row.items()}
            for row in result["results"]["bindings"]
        ]
    except Exception as exc:
        raise RuntimeError(
            f"SPARQL error — is Oxigraph running at {OXIGRAPH_URL}?\n{exc}"
        ) from exc


def shorten(iri: str) -> str:
    """Replace known namespace prefixes for compact display."""
    return (iri
            .replace(PVC, "pvc:")
            .replace(MDS, "mds:")
            .replace("http://www.w3.org/2002/07/owl#", "owl:")
            .replace("http://www.w3.org/2000/01/rdf-schema#", "rdfs:")
            .replace("http://www.w3.org/2004/02/skos/core#", "skos:"))


# ---------------------------------------------------------------------------
# MCP server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "pvcollada-onto",
    instructions=(
        "Provides vocabulary lookup and hierarchy navigation for the "
        "PV-Collada OWL 2 ontology (pvcollada_onto.ttl). "
        "Use these tools to ground extraction results against the ontology "
        "and to discover MDS-Onto alignment for any pvc: term."
    ),
)


@mcp.tool()
def lookup_term(label: str) -> str:
    """
    Find ontology classes and properties whose rdfs:label contains the given
    string (case-insensitive). Returns IRI, type (Class / DatatypeProperty /
    ObjectProperty), label, and skos:definition for each match.

    Args:
        label: Partial or full label to search for, e.g. "module", "voltage"
    """
    rows = sparql(f"""
    SELECT DISTINCT ?iri ?type ?lbl ?def WHERE {{
      VALUES ?rdftype {{ owl:Class owl:DatatypeProperty owl:ObjectProperty
                         owl:NamedIndividual }}
      ?iri a ?rdftype ;
           rdfs:label ?lbl .
      OPTIONAL {{ ?iri skos:definition ?def }}
      FILTER(CONTAINS(LCASE(STR(?lbl)), LCASE("{label}")))
    }}
    ORDER BY ?lbl
    """)

    if not rows:
        return f"No terms found matching '{label}'."

    lines = [f"Found {len(rows)} term(s) matching '{label}':\n"]
    for r in rows:
        iri_short = shorten(r["iri"])
        rtype = shorten(r.get("type", ""))
        defn = r.get("def", "(no definition)")
        lines.append(f"  {iri_short}  [{rtype}]")
        lines.append(f"    label: {r['lbl']}")
        lines.append(f"    definition: {defn}")
    return "\n".join(lines)


@mcp.tool()
def get_class_hierarchy(class_iri: str) -> str:
    """
    Walk the rdfs:subClassOf chain upward from the given class IRI,
    returning the full ancestor path to owl:Thing. Also returns immediate
    subclasses (one level down).

    Args:
        class_iri: Full IRI or pvc:-prefixed short form, e.g.
                   "https://cwrusdle.bitbucket.io/mds/builtenv/pvcollada/Module"
                   or "pvc:Module"
    """
    # Expand pvc: shorthand
    if class_iri.startswith("pvc:"):
        class_iri = PVC + class_iri[4:]
    if class_iri.startswith("mds:"):
        class_iri = MDS + class_iri[4:]

    # Ancestors (transitive)
    ancestors = sparql(f"""
    SELECT ?ancestor ?lbl WHERE {{
      <{class_iri}> rdfs:subClassOf+ ?ancestor .
      OPTIONAL {{ ?ancestor rdfs:label ?lbl }}
      FILTER(?ancestor != owl:Thing)
    }}
    """)

    # Direct subclasses
    children = sparql(f"""
    SELECT ?child ?lbl WHERE {{
      ?child rdfs:subClassOf <{class_iri}> ;
             rdfs:label ?lbl .
    }}
    ORDER BY ?lbl
    """)

    # Own label
    own = sparql(f"""
    SELECT ?lbl ?def WHERE {{
      <{class_iri}> rdfs:label ?lbl .
      OPTIONAL {{ <{class_iri}> skos:definition ?def }}
    }}
    """)

    short = shorten(class_iri)
    lines = [f"Class: {short}"]
    if own:
        lines.append(f"  label: {own[0].get('lbl', '—')}")
        lines.append(f"  definition: {own[0].get('def', '—')}")

    if ancestors:
        chain = " → ".join(shorten(r["ancestor"]) for r in ancestors)
        lines.append(f"\nAncestor chain:\n  {short} → {chain} → owl:Thing")
    else:
        lines.append(f"\nAncestor chain:\n  {short} → owl:Thing")

    if children:
        lines.append("\nDirect subclasses:")
        for c in children:
            lines.append(f"  {shorten(c['child'])}  \"{c.get('lbl', '')}\"")
    else:
        lines.append("\nNo declared subclasses.")

    return "\n".join(lines)


@mcp.tool()
def get_properties_for_class(class_iri: str) -> str:
    """
    List all OWL data properties and object properties whose rdfs:domain
    is (or includes) the given class. Returns IRI, range, label, unit, and
    definition for each property.

    Args:
        class_iri: Full IRI or pvc:-prefixed short form, e.g. "pvc:Module"
    """
    if class_iri.startswith("pvc:"):
        class_iri = PVC + class_iri[4:]
    if class_iri.startswith("mds:"):
        class_iri = MDS + class_iri[4:]

    rows = sparql(f"""
    SELECT ?prop ?ptype ?range ?lbl ?unit ?def WHERE {{
      VALUES ?ptype {{ owl:DatatypeProperty owl:ObjectProperty }}
      ?prop a ?ptype ;
            rdfs:domain <{class_iri}> ;
            rdfs:label  ?lbl .
      OPTIONAL {{ ?prop rdfs:range ?range }}
      OPTIONAL {{ ?prop <http://qudt.org/schema/qudt/applicableUnit> ?unit }}
      OPTIONAL {{ ?prop skos:definition ?def }}
    }}
    ORDER BY ?lbl
    """)

    if not rows:
        return f"No domain-scoped properties found for {shorten(class_iri)}."

    lines = [f"{len(rows)} properties scoped to {shorten(class_iri)}:\n"]
    for r in rows:
        pshort = shorten(r["prop"])
        rng = shorten(r.get("range", "—"))
        unit = shorten(r.get("unit", ""))
        defn = r.get("def", "—")
        ptype = "DataProp" if "Datatype" in r.get("ptype", "") else "ObjProp"
        lines.append(f"  {pshort}  [{ptype}]  range: {rng}"
                     + (f"  unit: {unit}" if unit else ""))
        lines.append(f"    {defn}")
    return "\n".join(lines)


@mcp.tool()
def get_mds_alignment(term_iri: str) -> str:
    """
    Return all MDS-Onto alignment annotations for a pvc: class, property,
    or named individual. Covers rdfs:subClassOf to mds: classes,
    skos:closeMatch, skos:exactMatch, and rdfs:seeAlso links.

    Args:
        term_iri: Full IRI or pvc:-prefixed short form, e.g. "pvc:Module"
    """
    if term_iri.startswith("pvc:"):
        term_iri = PVC + term_iri[4:]

    rows = sparql(f"""
    SELECT ?relation ?target ?targetLabel WHERE {{
      VALUES ?relation {{
        rdfs:subClassOf
        skos:closeMatch
        skos:exactMatch
        skos:relatedMatch
        rdfs:seeAlso
      }}
      <{term_iri}> ?relation ?target .
      FILTER(STRSTARTS(STR(?target), "{MDS}"))
      OPTIONAL {{ ?target rdfs:label ?targetLabel }}
    }}
    ORDER BY ?relation ?target
    """)

    short = shorten(term_iri)
    if not rows:
        return f"No MDS-Onto alignment found for {short}."

    lines = [f"MDS-Onto alignment for {short}:\n"]
    for r in rows:
        rel = shorten(r["relation"])
        tgt = shorten(r["target"])
        lbl = r.get("targetLabel", "")
        lines.append(f"  {rel}  {tgt}" + (f'  "{lbl}"' if lbl else ""))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
