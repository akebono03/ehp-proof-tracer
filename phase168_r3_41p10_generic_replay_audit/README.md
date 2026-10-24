# Phase 168 R3-41P10 — Generic ProofStep Replay Audit

This is an **audit-only** experiment, not an application patch. It measures
whether the existing generic inference matcher can validate all displayed
inference steps at a single proof-model boundary, including counterfeit steps.

The experiment intentionally **replays** mathematical inference checks.
It does not create or propose a new inference rule or claim that replay is a
better long-term trust boundary than provenance from the canonical search.

## Use

Extract this package into the root of the EHP Proof Tracer checkout and run
`powershell -ExecutionPolicy Bypass -File .\phase168_r3_41p10_generic_replay_audit\run.ps1`.
Use `-SkipTests` only to skip focused pytest. The full test suite is not run.

Generated `output/review_bundle.zip` contains the audit JSON/Markdown, proof
full texts, focused test output, and Git status logs. No application code or
existing test file is modified. Files under `output/` are generated artifacts.

## What is and is not certified

The prototype replays inference matching and compares generated conclusions.
It deliberately does **not** validate the provenance or publication order of
`GIVEN` steps. It also does not confer trust on manually constructed
`PartialProofResult` or `ProofNarrativeModel` objects.

Source inspection used the live `develop` branch of `akebono03/ehp-proof-tracer`
with checks for `proof.py`, `phase165_r3_recursive_search.py`,
`phase164_r8_proofstep_factory.py`, `phase165_r52_r2_search_adapter.py`,
`phase165_r52_partial_proof.py`, and
`phase168_r3_3_proof_narrative_model.py` and their relevant tests.
