# Phase 166 R3-B: publication-order binding test correction

This repair updates only two tests in the R3-B package. It preserves the existing reference-ID exact-match implementation and the Phase 163 manifest data. There is no locator fallback, TeX re-parsing, publication renumbering, proof-search change, or SQLite migration.

Extract this package into the project root, overwriting the earlier R3-B package, and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase166_r3b_publication_order_binding\run.ps1"
```

The script copies the full unchanged production module and full corrected test module to their existing project-root locations, runs three explicitly selected pytest modules, and writes an audit result. No full pytest suite is invoked. The previous two errors were incorrect test expectations: a missing `fact:` fixture and an expected exception where the exact-ID policy should instead leave a mismatched ID unbound.
