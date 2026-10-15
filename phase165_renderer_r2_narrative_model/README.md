# Phase 165 Renderer R2 — Shared Narrative Proof Model

Adds one immutable, evidence-preserving data model for both `PartialProofResult` and `TodaGroupProofPresentation`. This release does not reroute any existing renderer or alter the generated proof text. R3 will connect the new model to the single public rendering interface; R4 will address legacy imports and module retirement.

## Installation

Extract the ZIP at the EHP Proof Tracer project root and run `phase165_renderer_r2_narrative_model/run.ps1` in PowerShell.

The runner installs `phase165_renderer_narrative_model.py` without replacing any existing project source and executes six targeted tests. The complete test suite is not run.
