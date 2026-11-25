# Phase 176 R3R60R1 — Isolated citation and premise elision

This package adds a final-stage, presentation-only projection. No existing file is changed. The reviewed develop commit is `80b04b769e75e17646195ec99e7e5c253d17a410`.

For the completed proof of $\pi_8^3$, the projection is expected to omit the redundant body statement $E(\eta_2\nu')=0$ (already stated under Lemma 5.7), retain the actual right-composition consequence with consistent juxtaposition notation, and cite Toda (5.5) alone for its verified specialization. It removes the auxiliary ν-family reference block only if the typed family definition has no other proof use, no other attached claim, and no remaining body citation. Remaining display numbers are assigned consecutively, preserving their order and source bodies. The original ten model citations remain unchanged; nine are expected in the narrative only. The mapping is recorded in the audit plan.

The projector replays the existing inference rules and checks exact source identity, premise edges, source text, and unique visible anchors. It declines any incomplete, ambiguous, or unsupported input. It does not introduce mathematical rules, register GIVENs, modify search, or change the trusted proof model. The public renderer is intentionally not connected in this phase. The accepted proof fixture is used for integration tests; no synthetic accepted proof is substituted.

## Run

Extract the ZIP at the repository root, then run `run.ps1 -DryRun` and `run.ps1`. The script runs four focused test groups (19 tests expected), then the isolated audit. No full pytest is run. Reports are written outside the repository under `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r60r1_citation_premise_elision_isolated/`. Review `before.md`, `shadow.md`, `plan.json`, `narrative.diff`, `partial.md`, and `report.json`. The success gate is `PASS_R3R60R1_ISOLATED_CITATION_PREMISE_ELISION`.

Expected invariants: 62 proof steps, 51 INFERENCE, 11 GIVEN, ten internal citations, zero open goals, unchanged partial view, 19 to 18 body rows, ten to nine displayed reference blocks. Public connection and any related historical fixture adaptations are reserved for R3R60R2.
