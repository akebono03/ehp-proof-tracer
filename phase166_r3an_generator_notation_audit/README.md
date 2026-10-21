# Phase 166 R3-AN — Read-only Generator Notation Audit

Run `run.ps1` from the project directory after extracting the ZIP.

The audit enumerates all 112 targets (`2 <= n <= 15`, `0 <= k <= 7`) and obtains typed goals through the current `zero`, `structured`, or `simple` adapters. It renders them with the existing public relation renderer and records expression structure, source generator labels, and `Element` IDs. It reports missing goals, unrenderable targets, and unwanted `E^{1}` or `E^1` notation. No proof search is executed. No production files are patched.

Outputs: `results/report.json` and `results/report.md`. The focused pytest comprises two tests, and is not the full suite.

This is a structural and rendering-level audit, not a mathematical verification of each generator, nor a browser MathJax screenshot check. In particular, names displayed by the `simple` adapter cannot all be independently reconstructed from ID data.
