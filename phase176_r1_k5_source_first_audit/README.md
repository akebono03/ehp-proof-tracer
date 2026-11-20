# Phase 176 R1 — Read-only k=5 source-first proof search audit

Run `run.ps1 -DryRun` first, then `run.ps1`. This package does not patch the repository or execute the full pytest suite. It audits all registered k=5 groups using the current typed search and web proof facade, storing evidence outside the checkout.

Requirements: the package must be extracted at the repository root and run on the `develop` branch; Phase 175's final commit must be an ancestor, and the five active documents must have their formal closeout markers. The last reviewed GitHub `develop` HEAD was `bc318d6a66bd124cb6707559a6d2dc42128443b3` (2026-11-19). Any later commits are visible in the report and require review.

Known historical Phase 174 source-guard failures remain unresolved and are not counted as passing. The report is evidence, not a new proof registration.
