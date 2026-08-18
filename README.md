# Ontology Development Resources for the Battery Sector

This repository includes development resources contributing to ontology development for the battery sector within the CIRPASS-2 project.

**Important disclaimer:**

* The ontologies for the battery sector stored in this repository and generated within the CIRPASS-2 project do not represent an official ontology for the battery Digital Product Passport.
* This project is under active development. Information may be incomplete and is subject to change.

## Overview

This repository contains the **EU DPP Battery Ontology** (umbrella version 0.2.0 DRAFT): a sectoral ontology for battery Digital Product Passports under Regulation (EU) 2023/1542. It extends the CIRPASS-2 cross-sectoral CORE ontology (EU DPP CO) by direct reference and is organised as an umbrella module plus four thematic modules:

| File | Module | Prefix | Namespace |
|------|--------|--------|-----------|
| `battery ontology.ttl` | **Umbrella** — declares `bat:Battery` as a subclass of the cross-sectoral `dpp:Product` | `bat` | `https://w3id.org/eudpp/battery#` |
| `battery performance.ttl` | **Performance** — electrochemical performance, durability and in-use state (BatteryPass-Ready category "Performance and durability", attributes 59–100) | `batperf` | `https://w3id.org/eudpp/battery-performance#` |
| `battery materials.ttl` | **Materials** — battery chemistry and internal material location, extending the CORE MAT module | `batmat` | `https://w3id.org/eudpp/battery-materials#` |
| `battery labeling.ttl` | **Labeling** — labels and symbols (BatteryPass-Ready category "Symbols, labels and documentation of conformity", attributes 21–24) | `batlab` | `https://w3id.org/eudpp/battery-labeling#` |
| `battery-categories.ttl` | **Categories** — controlled vocabulary of the five battery categories of Art. 3(1), as individuals of the CORE class `dpp:ClassificationCode` | `batcat` | `https://w3id.org/eudpp/battery-categories#` |

### Battery category

The category is not a battery term. It is carried by the CORE property `dpp:hasProductGroup` (`dpp:Product` → `dpp:ClassificationCode`, declared in P_DPP v2.0.0):

```turtle
:battery-12345
    a                    bat:Battery ;
    dpp:hasProductGroup  batcat:ElectricVehicleBattery .
```

The five categories are defined in **Article 3(1)** of Regulation (EU) 2023/1542 — not Article 2, which is "Objectives".

| Category | `codeValue` | Art. 3(1) | Passport |
|---|---|---|---|
| Electric vehicle battery | `EV` | (14) | Yes |
| Light means of transport battery | `LMT` | (11) | Yes |
| Industrial battery | `industrial` | (13) | Yes, above 2 kWh |
| Portable battery | `portable` | (9) | No |
| Starting, lighting and ignition battery | `SLI` | (12) | No |

Passport scope is a conformance rule (Art. 77), expressed in SHACL, not in OWL.

## Modelling conventions

* Each module is a self-contained `owl:Ontology` file with its own IRI, `owl:versionIRI`, namespace, prefix and metadata.
* CORE concepts are referenced directly by IRI — no `owl:imports`, no copied axioms (same approach as the Textile sector modules). To obtain a connected graph, load these modules together with the EU DPP CO modules.
* The modules are developed against CIRPASS-2 CORE ontology v2.0 (P_DPP v2.0.0, MAT v1.0.2; update of 30 April 2026); external references are pinned to these versions.
* No cardinality restrictions in OWL: the mandatory/optional constraints of Regulation (EU) 2023/1542 are to be expressed in separate SHACL shapes.
* Alignments to BatteryPass-Ready and to the Spherity Battery Pass ontology are to be maintained in a dedicated SSSOM mappings file, not in the ontology itself.
* Controlled vocabularies are declared in their own module rather than inside the T-Box modules, so that they can be versioned independently.
* CORE reuse before local declaration: where the CORE already provides a class or property, it is reused rather than mirrored in the battery namespace.

## Changelog

### Umbrella 0.2.0 — 18 August 2026

* New module `battery-categories.ttl`: one `skos:ConceptScheme` and the five categories as individuals of `dpp:ClassificationCode` + `skos:Concept`, with the Art. 3(1) definitions quoted verbatim. Closes [#2](https://github.com/CIRPASS-2/ontologies-battery/issues/2).
* `eudpp:ClassificationCode` reused as-is; the fallback `bat:batteryCategory` is **not** created.
* Corrected the legal reference: the definitions are in **Art. 3(1)**, not Art. 2. `bat:Battery` updated accordingly.
* Umbrella: `battery-categories` added to `rdfs:seeAlso` and to the description.
* Added `bat:dueDiligenceReport` and `bat:dueDiligenceAudit` (`xsd:anyURI` on `bat:Battery`), Art. 52 / Annex X. Closes [#4](https://github.com/CIRPASS-2/ontologies-battery/issues/4). Kept in the battery namespace, as the issue proposes; `xsd:anyURI` rather than the CORE `Source` pattern, which lives in the not-yet-integrated LCA module.

## Reference sources

* Regulation (EU) 2023/1542 (Batteries Regulation), notably Annex XIII
* BatteryPass-Ready Data Attribute Long List v1.3
* Spherity Battery Pass ontology v0.1

---

© CIRPASS-2 Consortium, 2024-2027

The CIRPASS-2 project receives funding under the European Union's DIGITAL EUROPE PROGRAMME under the GA No 101158775.

**Important disclaimer:** All software and artifacts produced by the CIRPASS-2 consortium are designed for exploration and are provided for information purposes only. They should not be interpreted as being either complete, exhaustive, or normative. The CIRPASS-2 consortium partners are not liable for any damage that could result from making use of this information. Technical interpretations of the European Digital Product Passport system expressed in these artifacts are those of the author(s) only and do not necessarily reflect those of the European Union, European Commission, or the European Health and Digital Executive Agency (HADEA). Neither the European Union, the European Commission nor the granting authority can be held responsible for them. Technical interpretations of the European Digital Product Passport system expressed in these artifacts are those of the author(s) only and should not be interpreted as reflecting those of CEN-CENELEC JTC 24.

## License

This project is licensed under the Apache License 2.0.

```
Copyright 2024-2027 CIRPASS-2

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
