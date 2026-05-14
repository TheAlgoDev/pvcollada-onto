# PV-Collada Ontology (`pvcollada_onto.ttl`)

An OWL 2 ontology for describing photovoltaic (PV) systems at the level of
circuit topology, physical layout, and component product data.
Derived from the [PV-Collada 2.0 XML Schema](http://www.example.com/pvcollada)
and formally aligned with [MDS-Onto](https://cwrusdle.bitbucket.io/mds/)
(Materials Data Science Ontology).

---

## Namespace and IRI

| Item | Value |
|------|-------|
| Ontology IRI | `https://w3id.org/pvcollada/` |
| Persistent IRI | `https://w3id.org/pvcollada` (pending merge of w3id PR #6066) |
| Prefix | `pvc:` |
| OWL profile | OWL 2 DL |
| Serialisation | Turtle (`.ttl`) |
| Version | 0.1.0 |
| MDS-Onto domain | `builtenv` |
| MDS-Onto subdomain | `pvcollada` |

---

## Three-Layer Model

PV-Collada describes a PV system across three interlocking layers.
The ontology mirrors this structure through three abstract parent classes:

```
pvc:PVColladaEntity
├── pvc:PVComponent        (Layer 1 — product library)
├── pvc:CircuitInstance    (Layer 2 — electrical circuit topology)
└── pvc:PhysicalAsset      (Layer 3 — 3-D physical layout)
```

`pvc:ModuleLayout` is the **cross-domain bridge**: it links a module's
position in the circuit (Layer 2) to its physical slot on a rack (Layer 3).

---

## Class Reference

### Layer 1 — Product Library (`pvc:PVComponent`)

These classes represent typed component specifications, analogous to
entries in a manufacturer datasheet library.

| Class | XSD source | Description |
|-------|-----------|-------------|
| `pvc:Module` | `module_type_object` | PV module: dimensions, STC electrical parameters, cell technology |
| `pvc:Inverter` | `inverter_type_object` | DC→AC inverter: power ratings, MPPT window, efficiency |
| `pvc:MPPTUnit` | `mppt_type_object` | One MPPT channel specification on an inverter |
| `pvc:Transformer` | `transformer_type_object` | AC step-up/isolation transformer |
| `pvc:Cable` | `cable_type_object` | Cable: cross-section, material, resistance |
| `pvc:DCCombiner` | `combiner_dc_type_object` | DC string combiner box |
| `pvc:ACCombiner` | `combiner_ac_type_object` | AC inverter combiner panel |
| `pvc:Optimizer` | `optimizer_type_object` | Module-level power optimizer |

### Layer 2 — Circuit Topology (`pvc:CircuitInstance`)

These classes represent instantiated elements in the wired electrical circuit.

| Class | Description |
|-------|-------------|
| `pvc:Circuit` | Root of the electrical circuit; starts at a transformer, AC combiner, or inverter |
| `pvc:InverterInstance` | An inverter in the circuit, containing MPPT inputs |
| `pvc:TransformerInstance` | A transformer instance in the circuit |
| `pvc:ACCombinerInstance` | An AC combiner instance |
| `pvc:DCCombinerInstance` | A DC combiner instance |
| `pvc:MPPTInput` | One MPPT channel instance within an inverter instance |
| `pvc:String` | A series-connected string of modules |
| `pvc:ModuleArray` | Ordered collection of modules within a string |
| `pvc:OptimizerArray` | Ordered collection of optimizers within a string |
| `pvc:OptimizerInstance` | A single optimizer in the circuit |
| `pvc:ModuleLayout` | **Cross-domain bridge** — maps circuit position to physical rack slot |
| `pvc:CableTo` | A directed cable connection from a circuit element to its parent |

### Layer 3 — Physical Layout (`pvc:PhysicalAsset`)

| Class | Description |
|-------|-------------|
| `pvc:Project` | Top-level project metadata (capacity, counts, projection, boundary) |
| `pvc:Rack` | Co-planar module group; COLLADA geometry rectangle |
| `pvc:FixedTiltRack` | Rack subclass for fixed-tilt mounting (requires `azimuth`, `tilt`) |
| `pvc:TrackerRack` | Rack subclass for tracker mounting (requires `trackerAzimuth`) |
| `pvc:Table` | Group of mechanically linked racks in one row |
| `pvc:Post` | Structural post (rack, tracker, or fence) |
| `pvc:Gap` | Space between racks on a tracker torque tube (motor or joint) |
| `pvc:Terrain` | Triangulated 3-D terrain surface mesh |

---

## Enumeration Classes

XSD `simpleType` enumerations are modelled as `owl:Class` + `owl:oneOf`
named individuals.

| Class | Members |
|-------|---------|
| `pvc:CellMaterial` | `MonoSi` · `PolySi` · `ASi` · `CdTe` |
| `pvc:CellArchitecture` | `SingleJunction` · `Heterojunction` · `IBC` · `PERC` · `TOPcon` · `TandemPerovskite` |
| `pvc:ModuleType` | `Monofacial` · `Bifacial` · `CPV` · `Shingle` |
| `pvc:InverterType` | `CentralInverter` · `StringInverter` · `Microinverter` |
| `pvc:RackType` | `FixedTilt` · `TrackerRackType` |
| `pvc:TableType` | `FixedTable` · `TrackerTable` |
| `pvc:TrackerType` | `SingleAxisTracker` · `DualAxisTracker` |
| `pvc:TorqueTubeShape` | `CircularTube` · `RectangularTube` · `OctagonalTube` |
| `pvc:DriveType` | `IndependentDrive` · `LinkedDrive` |
| `pvc:PostType` | `RackPost` · `TrackerPost` · `FencePost` |
| `pvc:PostShape` | `RectangularPost` · `CircularPost` · `HShapePost` |
| `pvc:PostInclination` | `VerticalPost` · `PerpendicularPost` |
| `pvc:GapType` | `MotorGap` · `JointGap` |
| `pvc:ModuleOrientation` | `Portrait` · `Landscape` |
| `pvc:ConductorMaterial` | `CopperConductor` · `AluminumConductor` |
| `pvc:PowerType` | `ACPower` · `DCPower` |
| `pvc:EfficiencyStandardType` | `CECEfficiency` · `EUEfficiency` |

---

## Key Data Properties (Module)

| Property | Range | Unit | MDS-Onto link |
|----------|-------|------|---------------|
| `pvc:nomPower` | `xsd:float` | W | `mds:NameplateMaximumPower` |
| `pvc:vOc` | `xsd:float` | V | `mds:OpenCircuitVoltage` |
| `pvc:iSc` | `xsd:float` | A | `mds:ShortCircuitCurrent` |
| `pvc:vMpp` | `xsd:float` | V | `mds:VoltageAtMaximumPower` |
| `pvc:iMpp` | `xsd:float` | A | `mds:CurrentAtMaximumPower` |
| `pvc:tCoefPower` | `xsd:float` | %/°C | `mds:ModuleTemperatureCoefficientPower` |
| `pvc:tCoefVoc` | `xsd:float` | V/°C | `mds:ModuleTemperatureCoefficientVoltage` |
| `pvc:tCoefIsc` | `xsd:float` | A/°C | `mds:ModuleTemperatureCoefficientCurrent` |
| `pvc:numCells` | `xsd:positiveInteger` | — | `mds:CellNumber` |
| `pvc:numCellsSeries` | `xsd:positiveInteger` | — | `mds:CellNumberPerString` |
| `pvc:numStrings` | `xsd:positiveInteger` | — | `mds:ModuleParallelStringsNumber` |
| `pvc:bifacialFactor` | `xsd:float` | — | — |
| `pvc:moduleLength` / `Width` / `Depth` | `xsd:float` | mm | — |

Units for all quantitative properties are recorded via `qudt:applicableUnit`
annotations; QUDT unit IRIs from `http://qudt.org/vocab/unit/`.

---

## MDS-Onto Alignment

This ontology is a subdomain module of MDS-Onto (`mds:builtenv`).
The table below summarises the formal alignment with MDS-Onto v0.3.1.31.

| pvc: term | Relation | mds: term |
|-----------|----------|-----------|
| `pvc:Module` | `rdfs:subClassOf` | `mds:PhotovoltaicModule` |
| `pvc:Inverter` | `rdfs:subClassOf` | `mds:Inverter` |
| `pvc:Rack` | `rdfs:subClassOf` | `mds:Racking` |
| `pvc:Project` | `rdfs:subClassOf` | `mds:PhotovoltaicSite` |
| `pvc:CellArchitecture` | `skos:closeMatch` | `mds:CellTechnology`, `mds:CellTechnologyType` |
| `pvc:RackType` | `skos:closeMatch` | `mds:RackingType` |
| `pvc:PERC` | `skos:exactMatch` | `mds:PassivatedEmitterRearCell` |
| `pvc:nomPower` … `pvc:manufacturer` | `rdfs:seeAlso` | corresponding mds: measurement classes |

All pvc: classes carry `mds:hasDomain`, `mds:hasSubDomain`, and
`mds:hasStudyStage` annotation properties as required by MDS-Onto conventions.

---

## Business Rules (Schematron → OWL 2)

Two Schematron patterns from `pvcollada_business_2.0.sch` are encoded as
OWL 2 subclass restrictions:

**Fixed-tilt rack** (`pvc:FixedTiltRack`) must have `pvc:azimuth` and
`pvc:tilt` (minCardinality 1), and must not carry tracker geometry fields.

**Tracker rack** (`pvc:TrackerRack`) must have `pvc:trackerAzimuth`
(minCardinality 1), and must not carry fixed-tilt fields.

`pvc:FixedTiltRack` and `pvc:TrackerRack` are declared `owl:AllDisjointClasses`.

> The MPPT URL uniqueness rule (Schematron) cannot be expressed in OWL 2 DL;
> it requires SPARQL/SWRL and is documented in comments in the TTL file.

---

## Loading and Querying

**Protégé** — open `pvcollada_onto.ttl` directly; the `owl:imports` header
references the MDS-Onto IRI, which Protégé will attempt to resolve.

**RDFLib (Python)**
```python
import rdflib
g = rdflib.Graph()
g.parse("pvcollada_onto.ttl", format="turtle")
print(len(g), "triples")          # 1367
```

**Local SPARQL endpoint** — see `../sparql/README.md` for Oxigraph Docker
Compose setup. Once running at `localhost:7878`:
```sparql
PREFIX pvc: <https://w3id.org/pvcollada/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?class ?label WHERE {
  ?class a owl:Class ; rdfs:label ?label .
} ORDER BY ?label
```

---

## Sources

| Source file | Role |
|-------------|------|
| `pvcollada_schema_2.0.xsd` | Primary schema — classes, properties, enumerations |
| `pvcollada_business_2.0.sch` | Business rules — rack type conditional fields |
| `pvcollada_references_2.0.sch` | Reference integrity — circuit-to-component IDREF rules |
| `MDS_Onto-v0.3.1.31.owl` | Upstream ontology for alignment and subclass declarations |

---

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) —
consistent with MDS-Onto upstream.
