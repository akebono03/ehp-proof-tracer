# Phase 168 R3-19 — Standard Web model-first cutover

Unpack this directory into the repository root and run `phase168_r3_19_web_model_default/run.ps1` in PowerShell.

This change makes the pre-existing Proof Narrative Model the default source for narrative/outline output from `build_standard_web_group_proof_view`. Explicit `citation_source="legacy"` remains possible as a temporary compatibility path. `trace` is unchanged. No proof-search or mathematical rules are changed.

The current model renderer is intentionally concise and does not yet reproduce the complete long-form mathematical narrative. The next steps implement typed EHP exactness and other missing prose on this route, followed by citation unification and removal of the legacy route. Only focused tests are run here.
