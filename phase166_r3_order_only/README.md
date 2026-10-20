# Phase 166 R3 — Order-only reference gate

Extract this directory to the EHP Proof Tracer repository root. Run `powershell -ExecutionPolicy Bypass -File .\phase166_r3_order_only\run.ps1`.

This package modifies only `phase165_r3_recursive_search.py`, backing it up first. It uses publication order and, for assertions within one statement, component order. All three existing lookup modes share one reference gate. The `verified_assertion_ids` parameter remains accepted for backward compatibility but does not grant or withhold citation access. Registered fixed statements still require an existing correctly typed GIVEN proof link to serve as proof leaves.

Only focused tests are run. Full pytest is deferred to the end of the phase.
