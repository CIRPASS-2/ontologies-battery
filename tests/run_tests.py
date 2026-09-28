#!/usr/bin/env python3
"""Replay the battery SHACL shapes against the worked examples and the fixtures.

    pip install pyshacl
    python run_tests.py

Each check prints PASS or FAIL; the exit code is 1 if one fails.
The CORE modules are read from ../../../2-Core et modules, or from the folder
given in the CORE_DIR environment variable; without them the checks still run.
"""
import os
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, RDF
from rdflib.collection import Collection
from rdflib.namespace import XSD

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXAMPLES = ROOT / "Guide Utilisation"
STH = ROOT / "Shapes SHACL" / "SHACL simple paths"
CORE = Path(os.environ.get("CORE_DIR", ROOT.parent.parent / "2-Core et modules"))
FIXTURES = HERE / "fixtures"

SH = Namespace("http://www.w3.org/ns/shacl#")
DPP = Namespace("https://w3id.org/eudpp#")
BAT = Namespace("https://w3id.org/eudpp/battery#")
BATPERF = Namespace("https://w3id.org/eudpp/battery-performance#")
BATLAB = Namespace("https://w3id.org/eudpp/battery-labeling#")


def graph(*files):
    g = Graph()
    for f in files:
        try:
            g.parse(f)
        except Exception:  # OWL/XML files, which rdflib cannot read
            pass
    return g


ONTO = graph(*[f for f in sorted(ROOT.glob("*.ttl")) if "shapes" not in f.name and "view" not in f.name],
             *sorted(CORE.glob("*.owl")), *sorted(CORE.glob("event.ttl")))
PROFILE = graph(ROOT / "battery-shapes.ttl", ROOT / "battery-cf-shapes.ttl")
VIEWS = {v: graph(ROOT / f"battery-view-{v}.ttl") for v in ("public", "legitimate-interest", "authorities")}


def without(file, *props):
    g = graph(file)
    for p in props:
        g.remove((None, p, None))
    return g


def plus(file, prop, value):
    g = graph(file)
    g.add((next(g.subjects(RDF.type, BAT.Battery)), prop, value))
    return g


def results(data, shapes):
    conforms, report, _ = validate(data, shacl_graph=shapes, ont_graph=ONTO, inference="none", advanced=True)
    found = []
    for r in report.subjects(RDF.type, SH.ValidationResult):
        component = str(report.value(r, SH.sourceConstraintComponent)).rsplit("#", 1)[-1]
        text = " ".join(str(report.value(r, p)) for p in (SH.resultMessage, SH.resultPath, SH.sourceShape))
        path = report.value(r, SH.resultPath)
        if isinstance(path, BNode) and (path, RDF.first, None) in report:
            text += " " + " ".join(map(str, Collection(report, path)))
        found.append((component, text))
    return conforms, found


def check(label, data, shapes, expected):
    conforms, found = results(data if isinstance(data, Graph) else graph(data), shapes)
    if expected == "conforms":
        ok = conforms
    elif expected == "only forbidden data":  # a complete passport carries data a restricted view hides
        ok = all(c == "MaxCountConstraintComponent" for c, _ in found)
    elif expected == "only recycled content":  # known STH difference: the nested form asks every material
        ok = all("hasMaterial" in t or "materialRecycledContent" in t for _, t in found)
    else:  # a token the violation must mention
        ok = not conforms and any(expected in t for _, t in found)
    print(f"{'PASS' if ok else 'FAIL'}  {label}  [{expected}]")
    if not ok:
        for c, t in found[:5]:
            print(f"        {c}: {t[:150]}")
    return ok


checks = []
examples = {c: EXAMPLES / f"example-{c}-battery.ttl" for c in ("ev", "lmt", "industrial")}
for c, f in examples.items():
    if f.exists():
        checks += [(f"{c} example, profile", f, PROFILE, "conforms"),
                   (f"{c} example, authorities view", f, VIEWS["authorities"], "conforms"),
                   (f"{c} example, legitimate-interest view", f, VIEWS["legitimate-interest"], "only forbidden data"),
                   (f"{c} example, public view", f, VIEWS["public"], "only forbidden data")]
        if STH.is_dir():
            checks += [(f"{c} example, profile STH", f, graph(STH / "battery-shapes_version_STH.ttl", ROOT / "battery-cf-shapes.ttl"), "conforms"),
                       (f"{c} example, authorities view STH", f, graph(STH / "battery-view-authorities_version_STH.ttl"),
                        "only recycled content")]

conforming = FIXTURES / "demo-lfp-200_public_conforms.jsonld"
no_dd = FIXTURES / "demo-lfp-200_public_no-due-diligence.jsonld"
checks += [("fixture as submitted, public view", conforming, VIEWS["public"], "conforms"),
           ("fixture without due diligence, public view", no_dd, VIEWS["public"], "conforms"),
           ("fixture without due diligence nor cadmium symbol, public view",
            without(no_dd, BATLAB.cadmiumSymbol), VIEWS["public"], "conforms"),
           ("fixture with a test report, public view",
            plus(conforming, BAT.testReportResults, Literal("https://example.org/test-report", datatype=XSD.anyURI)),
            VIEWS["public"], "testReportResults"),
           ("fixture without battery category, public view",
            without(conforming, DPP.hasProductGroup), VIEWS["public"], "hasProductGroup")]
if examples["lmt"].exists():
    checks += [("lmt example without remaining capacity, profile",
                without(examples["lmt"], BATPERF.remainingCapacity), PROFILE, "attribute 60"),
               ("lmt example without remaining capacity, legitimate-interest view",
                without(examples["lmt"], BATPERF.remainingCapacity), VIEWS["legitimate-interest"], "attribute 60"),
               ("lmt example without battery category, profile",
                without(examples["lmt"], DPP.hasProductGroup), PROFILE, "hasProductGroup")]
if examples["ev"].exists():
    checks += [("ev example without capacity threshold for exhaustion, public view",
                without(examples["ev"], BATPERF.capacityThresholdForExhaustion), VIEWS["public"], "attribute 90")]

failed = sum(not check(*c) for c in checks)
print(f"\n{len(checks) - failed}/{len(checks)} checks passed")
sys.exit(1 if failed else 0)
