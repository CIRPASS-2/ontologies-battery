# Ontology Development Resources for the Battery Sector

This repository includes development resources contributing to ontology development for the battery sector within the CIRPASS-2 project.

**Important disclaimer:**

* The ontologies for the battery sector stored in this repository and generated within the CIRPASS-2 project do not represent an official ontology for the battery Digital Product Passport.
* This project is under active development. Information may be incomplete and is subject to change.

## Overview

This repository contains the **EU DPP Battery Ontology** (version 0.1.0 DRAFT): a sectoral ontology for battery Digital Product Passports under Regulation (EU) 2023/1542. It extends the CIRPASS-2 cross-sectoral CORE ontology (EU DPP CO) by direct reference and is organised as an umbrella module plus three thematic modules:

| File | Module | Prefix | Namespace |
|------|--------|--------|-----------|
| `battery ontology.ttl` | **Umbrella** — declares `bat:Battery` as a subclass of the cross-sectoral `dpp:Product` | `bat` | `https://w3id.org/eudpp/battery#` |
| `battery performance.ttl` | **Performance** — electrochemical performance, durability and in-use state (BatteryPass-Ready category "Performance and durability", attributes 59–100) | `batperf` | `https://w3id.org/eudpp/battery-performance#` |
| `battery materials.ttl` | **Materials** — battery chemistry and internal material location, extending the CORE MAT module | `batmat` | `https://w3id.org/eudpp/battery-materials#` |
| `battery labeling.ttl` | **Labeling** — labels and symbols (BatteryPass-Ready category "Symbols, labels and documentation of conformity", attributes 21–24) | `batlab` | `https://w3id.org/eudpp/battery-labeling#` |

## Modelling conventions

* Each module is a self-contained `owl:Ontology` file with its own IRI, `owl:versionIRI`, namespace, prefix and metadata.
* CORE concepts are referenced directly by IRI — no `owl:imports`, no copied axioms (same approach as the Textile sector modules). To obtain a connected graph, load these modules together with the EU DPP CO modules.
* The modules are developed against CIRPASS-2 CORE ontology v2.0 (P_DPP v2.0.0, MAT v1.0.2; update of 30 April 2026); external references are pinned to these versions.


## Reference sources

* Regulation (EU) 2023/1542 (Batteries Regulation), notably Annex XIII
* BatteryPass-Ready Data Attribute Long List v1.3
* Spherity Battery Pass ontology v0.1

---

© CIRPASS-2 Consortium, 2024-2027

The CIRPASS-2 project receives funding under the European Union's DIGITAL EUROPE PROGRAMME under the GA No 101158775.

## License


See the License for the specific language governing permissions and
limitations under the License.
```
