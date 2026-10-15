# Phase 165 R57-R21: One Narrative Path

The completed and incomplete public proof displays now call the same proof-evidence Narrative function. This release does not add mathematical facts, change proof search, or claim completion of unresolved goals.

## Install

Unzip the package into the EHP Proof Tracer project root, then run `phase165_r57_r21_narrative_unification/run.ps1` in PowerShell. The runner executes six targeted tests only. It does not run the full test suite.

## Scope

- Replace the completed-view adapter with a direct delegation to the common typed-proof Narrative function.
- Replace the existing partial-view Narrative function with a single presentation structure for both statuses.
- Fix the proof target being replaced by the first unresolved obligation.
- Render only observed ProofSteps, separating cited leaves from inferred conclusions.
- Keep unfinished goals and diagnostics visible without asserting that they are proved.

The previous completed-view replay and legacy Narrative calls are no longer used by the completed adapter. Their modules are not deleted by this phase because other entry points may still import them. Narrative prose may be less elaborate than the retired completed-only renderer; mathematical fidelity takes precedence over speculative text.
