# Phase 163 R4-R69 — Read-Only Candidate Order and Duplicate Audit

This bundle inspects the 17 Reference and 23 Assertion proposals from R4-R68. It does **not** allocate formal IDs, verify mathematical equivalence, assign verified publication positions, or modify the production registry.

Extract the ZIP into the EHP Proof Tracer project root. Run `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r69_order_duplicate_audit\run.ps1` from PowerShell.

Required input: `phase163_r4_r68_output/unnumbered_reference_proposals.json`.

Outputs: `phase163_r4_r69_output/order_duplicate_audit.json`, `order_duplicate_audit.csv`, and `report.md`.

The `candidate_order` is only the ordering of these 17 candidates, not the full Toda publication order. Equal source boundaries and equal source content hashes are audit evidence, not mathematical equivalence. Adjacency is not classified as duplication.

The focused test suite only is run. The full suite remains for Phase 163 closure.
