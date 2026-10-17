# Phase 165 R10 — Shared Rule Registry

This package installs a stable-ID rule registry for the existing zero-argument rule discovery path.
It retains the public `discover_inference_rules()` API and the existing search consumers.
It does not add mathematical rules, grant proof-reference rights, or restore retired catalogs.

Unzip in the repository root, then run `phase165_rule_registry_r10/run.ps1`.
Only targeted pytest tests run; no full test suite is executed.
