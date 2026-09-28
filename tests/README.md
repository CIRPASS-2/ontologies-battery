# Tests

`run_tests.py` replays the SHACL profile and the three views against the worked examples of `Examples/` and the fixtures below, including a few negative cases.

```
pip install pyshacl
python run_tests.py
```

## Fixtures

Contributed by Edmondo Grigolato (OrigoVero) in [#14](https://github.com/CIRPASS-2/ontologies-battery/issues/14). A fictional LFP industrial battery, 12.8 V and 200 Ah; every identifier is illustrative (GS1 952 demonstration prefix, example.org URLs, urn:example: operators).

- `demo-lfp-200_public_conforms.jsonld` — public-tier document, 86 triples, as submitted. It carries placeholder due-diligence URLs and a stand-in cadmium symbol, the workarounds #14 reported.
- `demo-lfp-200_public_no-due-diligence.jsonld` — the same without the two due-diligence properties, 84 triples. Submitted as failing the public view; conforms since the #14 changes.
