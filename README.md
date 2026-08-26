# Ontology Development Resources for the Battery Sector

This repository includes development resources contributing to ontology development for the battery sector within the CIRPASS-2 project.

**Important disclaimer:**

* The ontologies for the battery sector stored in this repository and generated within the CIRPASS-2 project do not represent an official ontology for the battery Digital Product Passport.
* This project is under active development. Information may be incomplete and is subject to change.

See [DISCLAIMER.md](DISCLAIMER.md) for the full disclaimer.

## Overview

This repository contains the **EU DPP Battery Ontology** (umbrella version 0.4.0 DRAFT): a sectoral ontology for battery Digital Product Passports under Regulation (EU) 2023/1542. It extends the CIRPASS-2 cross-sectoral CORE ontology (EU DPP CO) by direct reference and is organised as an umbrella module plus eight thematic modules:

| File | Module | Prefix | Namespace |
|------|--------|--------|-----------|
| `battery ontology.ttl` | **Umbrella** — declares `bat:Battery` as a subclass of the cross-sectoral `dpp:Product` | `bat` | `https://w3id.org/eudpp/battery#` |
| `battery performance.ttl` | **Performance** — electrochemical performance, durability and in-use state (BatteryPass-Ready category "Performance and durability", attributes 59–100) | `batperf` | `https://w3id.org/eudpp/battery-performance#` |
| `battery materials.ttl` | **Materials** — battery chemistry and internal material location, extending the CORE MAT module | `batmat` | `https://w3id.org/eudpp/battery-materials#` |
| `battery-locations.ttl` | **Locations** — the three internal locations named by Annex XIII 2(a) — cathode, anode, electrolyte — as individuals of `batmat:BatteryLocation`, value set of `batmat:hasBatteryLocation` | `batloc` | `https://w3id.org/eudpp/battery-locations#` |
| `battery-chemistries.ttl` | **Chemistries** — the ten chemistry terms of the draft labelling Implementing Act, as individuals of the CORE class `dpp:MaterialType` | `batchem` | `https://w3id.org/eudpp/battery-chemistries#` |
| `battery labeling.ttl` | **Labeling** — labels and symbols (BatteryPass-Ready category "Symbols, labels and documentation of conformity", attributes 21–24) | `batlab` | `https://w3id.org/eudpp/battery-labeling#` |
| `battery-extinguisher-classes.ttl` | **Extinguisher classes** — controlled vocabulary of the five extinguisher classes, value set of `batlab:extinguishingAgent` | `batext` | `https://w3id.org/eudpp/battery-extinguisher-classes#` |
| `battery-categories.ttl` | **Categories** — controlled vocabulary of the five battery categories of Art. 3(1), as individuals of the CORE class `dpp:ClassificationCode` | `batcat` | `https://w3id.org/eudpp/battery-categories#` |
| `battery-statuses.ttl` | **Statuses** — controlled vocabulary of the five battery lifecycle statuses of Annex XIII 4(c), value set of `bat:hasBatteryStatus` | `batstat` | `https://w3id.org/eudpp/battery-statuses#` |
| `battery-cf-shapes.ttl` | **Carbon footprint shapes** — SHACL profile binding the battery carbon footprint to the CORE; declares no term | `batcf` | `https://w3id.org/eudpp/battery-cf-shapes#` |

### Battery status vs passport status

Two different things, deliberately kept apart.

The **battery status** is the state of the physical item — `original`, `repurposed`, `re-used`, `remanufactured`, `waste` (Annex XIII 4(c)). It is a battery term, carried by `bat:hasBatteryStatus`:

```turtle
:battery-12345
    a                     bat:Battery ;
    bat:hasBatteryStatus  batstat:Repurposed .
```

The **passport status** is the state of the digital resource — `Active`, `Archived`, `Inactive`, `Invalid`. It is cross-sectoral and already in the CORE, on `dpp:DPP` through `dpp:dppStatus`. It is not restated in the battery namespace.

The OWL range of `bat:hasBatteryStatus` is `skos:Concept`, deliberately loose. Closing the list is a conformance rule: the [#10](https://github.com/CIRPASS-2/ontologies-battery/issues/10) shape set carries an `sh:in` over the five concepts of `batstat:BatteryStatusScheme`.

When a battery is remanufactured, repurposed or prepared for re-use and placed on the market again, a new passport is issued and linked back to the previous one through the CORE property `dpp:linkToPreviousDPP` (ESPR Art. 11(d)). Status-change events belong to the CORE event module.

Two gaps on that CORE side were raised rather than patched here: [ontologies-core#56](https://github.com/CIRPASS-2/ontologies-core/issues/56) — `linkToPreviousDPP` is one-directional and typed `xsd:anyURI` rather than pointing at `dpp:DPP` — and [ontologies-core#57](https://github.com/CIRPASS-2/ontologies-core/issues/57) — `dppStatus` enumerates `Invalid` where prEN 18223 says `Marked-for-deletion`.

`bat:hasBatteryStatus` is the one place where the battery module declares a term the CORE could have provided. There is no generic product status in the CORE — `dpp:hasProductGroup` carries the product group, not the state of the item — so the property is local by necessity, not by choice. It is a stopgap: [ontologies-core#35](https://github.com/CIRPASS-2/ontologies-core/issues/35) requests a cross-sectoral `eudpp:productStatus` on `eudpp:Product`, and is still open. When it lands, `bat:hasBatteryStatus` is to be deprecated in favour of it.

### Carbon footprint binding

No carbon-footprint term is declared in the battery namespace. The footprint is the
cross-sectoral `dpp:CarbonFootprint` of P_DPP, reached through `dpp:hasProperty`, and
`battery-cf-shapes.ttl` only constrains how a battery uses it:

```turtle
:battery-12345
    a                 bat:Battery ;
    dpp:hasProductGroup  batcat:ElectricVehicleBattery ;
    dpp:hasProperty   [ a dpp:CarbonFootprint ;
                        dpp:numericalValue      "52.4"^^xsd:decimal ;
                        dpp:hasMeasurementUnit  si:kilogram ] .
```

Two shapes are active today. `CarbonFootprintRequiredShape` requires a footprint on
batteries in the electric-vehicle, industrial and LMT categories, and leaves portable and
SLI batteries unconstrained. `CarbonFootprintValueShape` requires exactly one non-negative
decimal value and exactly one measurement unit.

The rest of the binding requested in
[ontologies-battery#1](https://github.com/CIRPASS-2/ontologies-battery/issues/1) — LCA
study, per-stage breakdown, functional unit, verification, background datasets,
manufacturing plant, declaration of conformity, public study link, performance class — is
written in the same file but carries `sh:deactivated true`, and becomes active by removing
one boolean. Each deactivated shape states why it is off, and the three reasons are not
the same thing: **PENDING** — the term is to be created by a CORE issue that #1 itself
cites; **MISSING** — #1 treats the term as available and it is absent from a module file
that is complete; **UNKNOWN** — the term belongs to the LCA module, which is not in the
folder and not imported by `core.owl`, so nothing can be concluded either way.

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

The industrial row is a **two-part test**: the category *and* a capacity above 2 kWh. The [#10](https://github.com/CIRPASS-2/ontologies-battery/issues/10) shape therefore needs a rated energy value in kWh next to `dpp:hasProductGroup`. **No term carries one today**: `batperf:ratedCapacity` is in ampere-hours, and `batperf:certifiedUsableBatteryEnergy` is the UN GTR No 22 value certified for a vehicle, which does not apply to an industrial battery. Open point on [#2](https://github.com/CIRPASS-2/ontologies-battery/issues/2).

## Modelling conventions

* Each module is a self-contained `owl:Ontology` file with its own IRI, `owl:versionIRI`, namespace, prefix and metadata.
* CORE concepts are referenced directly by IRI — no `owl:imports`, no copied axioms (same approach as the Textile sector modules). To obtain a connected graph, load these modules together with the EU DPP CO modules.
* The modules are developed against CIRPASS-2 CORE ontology v2.0 (P_DPP v2.0.0, MAT v1.0.2; update of 30 April 2026); external references are pinned to these versions.
* No cardinality restrictions in OWL: the mandatory/optional constraints of Regulation (EU) 2023/1542 are to be expressed in separate SHACL shapes.
* **Tier-free ontology**: access tiers (public / legitimate interest / authorities) are carried by the SHACL shapes, not by the ontology — no annotation property, no per-class flags.
* Alignments to BatteryPass-Ready and to the Spherity Battery Pass ontology are to be maintained in a dedicated SSSOM mappings file, not in the ontology itself.
* Controlled vocabularies are declared in their own module rather than inside the T-Box modules, so that they can be versioned independently.
* CORE reuse before local declaration: where the CORE already provides a class or property, it is reused rather than mirrored in the battery namespace.

## Changelog

### battery-extinguisher-classes — 26 August 2026

Closes the open point of [#8](https://github.com/CIRPASS-2/ontologies-battery/issues/8) (3).

* **Reference standard settled: EN 2:2005.** `batext:ClassK` renamed to `batext:ClassF`, `skos:notation "F"`, with `skos:altLabel "K (NFPA 10)"` and a `skos:scopeNote` on the equivalence so NFPA-sourced data — Spherity Battery Pass v0.1 — still maps. Renamed outright, not deprecated: the namespace is not published under `w3id.org`.
* `batext:ClassC` takes its EN 2 reading, fires involving flammable gases. The NFPA reading, energised electrical equipment, is kept as an `skos:editorialNote`: it is a mapping trap, not an open question, and the letter C cannot be carried across unchecked.
* **Re-check flag** on the scheme: ISO 3941:2026 introduces a class L for lithium-ion battery fires, which EN 2 does not have. To be re-checked if EN 2 is amended or if the final labelling Implementing Act references another standard.

### battery-performance — 26 August 2026

Closes item (1) of [#7](https://github.com/CIRPASS-2/ontologies-battery/issues/7).

* Units are no longer comment-only. New annotation property `batperf:measurementUnit` carries the SI Digital Framework IRI of the unit on each datatype property — the module follows its parent module, as `dpp:hasMeasurementUnit` anchors P_DPP on `si:MeasurementUnit`. `dpp:hasMeasurementUnit` itself does not apply here: it is an object property on `QuantitativeProperty`, and turning quantities into `QuantitativeProperty` instances is a separate question.
* **14 of the 36 properties that carry a unit could be annotated** — volt, watt, ohm, degree Celsius, minute. The other 22 have no IRI in the framework, which publishes SI units and a short list of accepted non-SI units: percent (11), percent per month (2), kilowatt-hour (3), ampere-hour (3), year (1), A/Ah and W/Wh (2). They stay in `rdfs:comment` and the cases are listed in the module header, per the rule agreed in #7. Almost every battery-specific quantity is in that list — which is the substance of [ontologies-core#58](https://github.com/CIRPASS-2/ontologies-core/issues/58) on the CORE-wide unit mechanism.

### Umbrella — 26 August 2026

* New property `bat:warrantyPeriod` (`xsd:duration`, domain `bat:Battery`), for data point 35 of the Commission guidance — Annex XIII 1(m), BatteryPass-Ready attribute 17. Declared here rather than in the CORE on the decision of 26 August 2026: [ontologies-core#34](https://github.com/CIRPASS-2/ontologies-core/issues/34) asked for a cross-sectoral warranty period, but the ESPR does not require one while Regulation (EU) 2023/1542 does, so the term stays sectoral.
* The attribute is conditional — *"if applicable (if commercial warranty envisaged)"* for all three passport categories — an optionality for the [#10](https://github.com/CIRPASS-2/ontologies-battery/issues/10) shapes, not for the ontology.

### battery-performance 0.3.0 — 25 August 2026

Closes [#6](https://github.com/CIRPASS-2/ontologies-battery/issues/6).

* New class `batperf:BatteryStateRecord` (`⊑ dpp:Property`), new object property `batperf:hasBatteryStateRecord` (`⊑ dpp:hasProperty`) and new datatype property `batperf:asOfDate` (`xsd:dateTimeStamp`). One record per BMS reading; the series of records is the history Annex XIII 4 and Annex VII Part B describe. `dateTimeStamp` rather than `dateTime` makes the time zone offset mandatory, so no separate offset property is needed.
* **22 properties re-anchored** from `BatteryPerformance`, `BatteryDurability` and `TemperatureExposure` onto `BatteryStateRecord`. Which ones is not a local judgement: the BatteryPass-Ready long list v1.3 carries a *"Data behavioural characteristic: static vs. dynamic"* column, and the 18 attributes it marks dynamic (BPR 60, 63, 64, 65, 70, 76, 79, 80, 85, 88, 89, 91, 94-97, 98, 99) move. The four fades and increases it marks static (BPR 61, 71, 77, 82) move as well: their update rule is *"upon placement on market and battery status change"*, so they do change, and a fade with no date is ambiguous.
* Only `rdfs:domain` changes. No IRI renamed, nothing deprecated: the modules are not published under `w3id.org` yet.
* `TemperatureExposure` is kept, holding the two idle-state boundaries (BPR 92, 93), which are static specifications under Annex XIII 1(l).
* `AccidentEvent` is untouched, and still carries no timestamp: the CORE event module declares no time property outside `evt:EPCISCarrier`.

### Metadata — 25 August 2026

* `dcterms:creator "Marc-Andree Wolf"` added to all ten modules, alongside Nader Jelassi. Patch version bump on the six modules where this is the only change.

### Umbrella 0.4.0 — 25 August 2026

* New property `bat:partNumber` (`xsd:string`), for data point 46 of the Commission guidance (Annex XIII 2(b), BatteryPass-Ready attribute 45). Domain is `dpp:Product`, not `bat:Battery`: the Regulation asks for the part numbers *of the components*, and a component is a product linked through `dpp:isComponentOf` — CIRPASS-2 decided in June 2026 not to introduce a Component class. Declared in the battery namespace because the CORE has no cross-sectoral part number; adding one went to the Commission as a recommendation. Typed as in Spherity Battery Pass v0.1, where `bp:partNumber` is an `xsd:string` datatype property.
* `bat:safetyMeasures` carries an `rdfs:seeAlso` to `eudpp:DigitalInstruction` (P_DPP). Not a SKOS mapping: the battery term is a datatype property carrying a URL, the CORE term is a class of documents, and an alignment between the two would not hold at audit. Re-expressing the property on a CORE document pattern remains the subject of [#11](https://github.com/CIRPASS-2/ontologies-battery/issues/11).
* Module list in `rdfs:seeAlso` and in the description corrected: it named five companion modules out of the eight that exist.

### battery-locations 0.1.0 — 25 August 2026

* New module. One `skos:ConceptScheme` and the three locations of Annex XIII 2(a) — `cathode`, `anode`, `electrolyte` — as individuals of `batmat:BatteryLocation` and `skos:Concept`, with `skos:notation` carrying the term as written in the Regulation.
* Closes the gap recorded against data point 45 of the Commission guidance: `batmat:BatteryLocation` was declared but had no value set, so cathode / anode / electrolyte could not be named.
* Deliberately limited to the three locations the Regulation names. Separator, casing and current collectors are not in Annex XIII 2(a) and are not declared; no definition is asserted, since the Regulation names these locations without defining them.

### battery-materials 0.3.0 — 25 August 2026

* `batmat:BatteryLocation` points at its new value set; the class comment no longer describes it as having none.


### battery-cf-shapes 0.1.0 — 19 August 2026

Answers [#1](https://github.com/CIRPASS-2/ontologies-battery/issues/1). No ontology file changed: the issue asks for a binding, not for local modelling.

* New `battery-cf-shapes.ttl`. Two active shapes constrain what the CORE provides today; nine deactivated shapes express the rest of the binding, each tagged PENDING, MISSING or UNKNOWN.
* Each deactivated shape is tagged PENDING (the term is to be created by a CORE issue that #1 itself cites), MISSING (#1 treats it as available and it is absent from a module file that is complete) or UNKNOWN (it belongs to the LCA module, which is not in the folder — no claim either way).
* Verified findings: `dpp:hasLCAStudy` is declared with domain `Product` and **no `rdfs:range`**; CONNECTOR has **no COMP properties at all** — neither `hasEUDeclarationOfConformity`, nor `hasNotifiedBody`, nor `hasComplianceDeclaration`; and `comp.owl` has **no DoC identifier term** — `certificateNumber` and `certificateRevisionNumber` hang off `ConformityCertificate`, not off `EUDeclarationOfConformity`. The `moduleD1` individual does exist.
* `core.owl` imports SOC, EVENT, MAT, P_DPP, IDENT, CON and ACTOR. **LCA and COMP are not imported**, so two of the three modules named in the title of #1 are not part of the CORE today.

### Umbrella 0.3.0 — 19 August 2026

Closes [#3](https://github.com/CIRPASS-2/ontologies-battery/issues/3) for the battery-side scope; the passport-side points are already covered by the CORE or raised as CORE issues.

* New module `battery-statuses.ttl`: one `skos:ConceptScheme` and the five Annex XIII 4(c) statuses as `skos:Concept` individuals — `original`, `repurposed`, `re-used`, `remanufactured`, `waste` — with `skos:notation` carrying the literal value to publish.
* New property `bat:hasBatteryStatus` (`bat:Battery` → `skos:Concept`). Declared locally because the CORE has no generic product status to reuse. This is a stopgap: [ontologies-core#35](https://github.com/CIRPASS-2/ontologies-core/issues/35), opened on 22 June 2026 and still open, requests a cross-sectoral `eudpp:productStatus` on `eudpp:Product` — motivated by this very attribute. The property carries an `rdfs:seeAlso` to that issue and is flagged for deprecation when it lands.
* **Passport lifecycle: nothing added.** Verified in `p_dpp.owl` — `dpp:DPP` already carries `dppStatus` (enumerated `Active` / `Archived` / `Inactive` / `Invalid`), `linkToPreviousDPP` (ESPR Art. 11(d)), `validFrom`, `validUntil` and `lastUpdate`; the EVENT module already has `DPPCreationEvent`, `DPPUpdateEvent` and `DPPArchivalEvent` under `DPPEvent`. Deactivation semantics and the predecessor link are cross-sectoral and stay in the CORE.
* **Repair is not a status.** Annex XIII 4(c) records a repaired battery under `re-used`; the repair history belongs to the CORE event module (`dpp:RepairEvent`). No sixth status value, no repair property — recorded as a `skos:scopeNote` on `batstat:ReUsed`.
* Access to the battery status is restricted to persons with a legitimate interest. Per the tier-free convention that is a SHACL rule, not an ontology axiom; recorded in the scheme `skos:scopeNote`.

### battery-performance 0.2.0 — 19 August 2026

Closes [#7](https://github.com/CIRPASS-2/ontologies-battery/issues/7) points (2) to (4); point (1) — unit alignment — waits on a CORE-level decision.

* **18 properties were `xsd:integer`; the 14 measured quantities are now `xsd:decimal`**: rated and remaining capacity, certified and remaining usable battery energy, original and remaining power capability, initial internal resistance, temperature information, the two idle-state temperature boundaries, and the four aggregated times spent in extreme temperatures. Whole ohms could not express the mΩ range, whole kWh could not express usable energy, whole °C could not express a boundary.
* Four properties stay `xsd:integer` because they are counts, not measurements: `numberOfDeepDischargeEvents`, `numberOfOverchargeEvents`, `numberOfFullCycles`, `expectedLifetimeCycles`.
* The three object properties of the module — `hasBatteryPerformance`, `hasBatteryDurability`, `hasTemperatureExposure` — are declared `rdfs:subPropertyOf dpp:hasProperty`. The chain requested for verification holds in P_DPP v2.0.0: `Durability ⊑ QualityIndicator ⊑ QuantitativeProperty ⊑ Property`, and `dpp:hasProperty` is `Product → Property`.
* `BatteryPerformance` and `TemperatureExposure` had no parent; both are now `⊑ dpp:Property`. Deliberately **not** `dpp:QuantitativeProperty`: they are containers grouping several measured quantities, not quantities themselves, and would otherwise inherit `hasMeasurementUnit` (domain `QuantitativeProperty`), which has no meaning on a container. This also makes the three `subPropertyOf` declarations above coherent, since `dpp:hasProperty` ranges over `Property`.
* `AccidentEvent` re-anchored from `dpp:MaintenanceEvent` to `dpp:ProductEvent`. Verified in the EVENT module: `ProductEvent ⊑ ESPREvent`, with `MaintenanceEvent`, `RepairEvent`, `RefurbishmentEvent`, `RemanufacturingEvent`, `DestructionEvent` and `UpgradingEvent` as its subclasses — an accident is none of those, so the generic parent is the right anchor.
* **Open point on units.** They remain in `rdfs:comment` only. P_DPP anchors units on the **SI Digital Framework** (`hasMeasurementUnit` → `si:MeasurementUnit`), not on OM-2; no OM-2 reference was found in `p_dpp.owl`. If LCA does use OM-2, the CORE carries two unit mechanisms and the question has to be settled there before the 42 properties of this module are converted.

### battery-labeling 0.2.0 — 19 August 2026

Closes [#8](https://github.com/CIRPASS-2/ontologies-battery/issues/8) points (1) to (4); point (5) waits for the CORE `Labelling` class.

* `batlab:cadmiumLeadSymbol` split into `batlab:cadmiumSymbol` and `batlab:leadSymbol`, each carrying its own legal trigger in `rdfs:comment` (> 0,002 % cadmium, > 0,004 % lead). The two symbols are required independently of one another, so one property could not express either state.
* Removed `batlab:labelingSubject`. It duplicated the typed properties, imposed a second labelling mechanism alongside them, and carried the `CarbonFootPrint` typo. Dropping it settles all three at once and leaves typed properties as the only mechanism. Nothing else referenced it.
* New module `battery-extinguisher-classes.ttl`: the five extinguisher classes as `skos:Concept` individuals, with `skos:notation` carrying the letter. `batlab:extinguishingAgent` retyped from a free-text datatype property to an object property with range `skos:Concept`. Renamed directly rather than deprecated: the module has never been published under `w3id.org`.
* **Open point on the extinguisher vocabulary** — settled on 26 August 2026, see the entry of that date. The five letters A, B, C, D, K were those of the Spherity Battery Pass ontology v0.1, while BatteryPass-Ready long list attribute 24 pins the fire class to **EN 2:2005**, which defines A, B, C, D and **F**.
* Data carrier / QR (point 4): **nothing added**. Verified in `ident.owl` and `connector.owl` — IDENT declares 13 identifier and scheme classes and no QR, barcode, NFC or data-carrier concept; the only GS1 references are the GLN and GTIN identifier schemes. This is a cross-sectoral gap, to be raised as a CORE issue rather than patched here.
* `batlab:BatteryLabel` marked provisional, with an `rdfs:seeAlso` to [ontologies-core#55](https://github.com/CIRPASS-2/ontologies-core/issues/55); it is to be re-anchored on the cross-sectoral `Labelling` class when that lands.
* Module now counts 1 class, 2 object properties and 4 datatype properties (was 1 / 1 / 5).

### Umbrella 0.2.0 — 18 August 2026

* New module `battery-categories.ttl`: one `skos:ConceptScheme` and the five categories as individuals of `dpp:ClassificationCode` + `skos:Concept`, with the Art. 3(1) definitions quoted verbatim. Closes [#2](https://github.com/CIRPASS-2/ontologies-battery/issues/2).
* `eudpp:ClassificationCode` reused as-is; the fallback `bat:batteryCategory` is **not** created.
* Corrected the legal reference: the definitions are in **Art. 3(1)**, not Art. 2. `bat:Battery` updated accordingly.
* Umbrella: `battery-categories` added to `rdfs:seeAlso` and to the description.
* Five documentation links added on `bat:Battery`, all `xsd:anyURI`: `dueDiligenceReport` and `dueDiligenceAudit` (Art. 52 / Annex X — closes [#4](https://github.com/CIRPASS-2/ontologies-battery/issues/4)); `dismantlingInformation`, `safetyMeasures` and `testReportResults` (Annex XIII 2(c), 2(d), 3 — closes [#5](https://github.com/CIRPASS-2/ontologies-battery/issues/5)).
* `xsd:anyURI` rather than the CORE `Source` pattern: no `Source` class was found in any CORE module.
* Access-tier decision recorded: the ontology stays tier-free (see Modelling conventions).

### battery-materials 0.2.0 — 18 August 2026

Closes [#9](https://github.com/CIRPASS-2/ontologies-battery/issues/9) points (1) and (2); point (3) waits for MAT v2.

* `batmat:hasBatteryChemistry rdfs:subPropertyOf dpp:hasMaterial` — was prose only.
* New module `battery-chemistries.ttl`: the ten chemistry terms of the draft labelling Implementing Act (BatteryPass-Ready long list, attribute 39), as individuals of `dpp:MaterialType`, reached through the inherited `dpp:hasMaterialType`. No new property in `batmat:`. `skos:notation` carries the term to print on the label.
* Removed `chemistryShortName` and `chemistryClearName`: the short code is `skos:notation`, the full name `skos:prefLabel`.
* Point (3) — MAT two-level refactoring — deferred: mapping `BatteryLocation` to the part level before MAT v2 exists would have to be redone.

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
