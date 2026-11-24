# Phase 176 R3R46R1 — Admitted prior group availability

This package supersedes the **unexecuted** R3R46 package. Start from the R3R45 develop source (reviewed HEAD `d91cb175ea361e0b4433092bc0a004e78a787f15`). Exact reviewed source blobs, including LF/CRLF variants, are checked before any edits. If R3R46 was already installed or a source was changed, the guard stops rather than discarding changes. Re-running this R3R46R1 patch is idempotent. No commit, push, checkout or reset is performed.

## Scope

- Append `admitted_prior_group_step()` to the existing R10E4 DB admission module. Discover by group coordinates, then call the unchanged `admitted_db_step()` gate.
- Insert zero-goal contradiction checks in the canonical recursive resolver and before visiting a candidate's immediate premises. Retain direct eligible zero-reference priority and the existing first-success search. Reject only a known nonzero group; no raw DB row alone is evidence. Rejected goals are not emitted as unresolved search events, and the actual rejection witnesses are separately recorded in the audit.
- Append a general prior-domain candidate provider after the existing shared providers. Reuse the unchanged R40 adopted-DB rule and, when eligible, the existing R9 linked-literature rule. Do not require a stable-family suspension or the cited (5.9) annihilator merely to propose the zero-map obligation. Each generator image must still be inferred.
- No new registered GIVEN, mathematical rule, data row, or target-specific search branch. The original proof target and the existing citation order remain unchanged. No automatic sweep of all historical providers; later consumers can use the common group lookup API.

## Run

Extract the ZIP into the repository root. Run `run.ps1 -DryRun`, then `run.ps1`. The installer emits complete changed functions in `SHARED_FUNCTIONS_FULL_JA.md`. The audit runs the actual Group query (3,5), not a manually constructed completed proof. It requires the earlier DB prior to be eligible and actually accepted in search, a zero-image candidate to be observed, and the contradictory zero group and irrelevant Delta provider not to be visited. It reports generator-image, zero-map and Hopf-injectivity proof status separately; root completion is not required. A failed audit is not a claim of success. The focused suite is listed in `run.ps1`; full pytest is not run.
