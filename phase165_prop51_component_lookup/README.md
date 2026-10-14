# Phase 165 — Typed Composite Reference Component Lookup

This package adds a read-only lookup API for typed components within existing fixed statements. It does not change the existing proof search or grant citation approval. Run from the repository root after extraction using `powershell -ExecutionPolicy Bypass -File .\phase165_prop51_component_lookup\run.ps1`.

Files installed: `phase165_typed_component_lookup.py` and `test_phase165_typed_component_lookup.py`. Run only `python -m pytest -q test_phase165_typed_component_lookup.py`.

Completion criterion: individual components of a composite fixed assertion are searchable by source locator, field name, and predicate, without copying the parent into independent GIVEN claims. Next-phase boundary: connect verified individual components as evidence-bearing source steps to Phase 165 backward search and implement common EHP inference expansion.
