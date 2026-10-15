# Phase 165 R57-R6 — Stable transport deletion gate

This package performs a **read-only** audit of whether the existing Toda (4.5) typed stable transport inference rules are invoked from the shared backward-search provider. It also records the R55 registry-goal selection boundary and the live public stable Narrative branch.

The user-observed `pi_5^4` failure occurs before public rendering; the existence of a legacy stable Narrative branch does not establish that typed stable transport is wired into the current proof search. Removing that branch prematurely could discard previously displayed results.

No old proofs are replayed. No GIVEN statements are fabricated. No renderer code, inference rules, registry data, or tests in the repository are modified. The installer is simply the read-only audit; its output is `phase165_r57_r6_stable_transport_audit.json` in the repository root.

Run the included `run.ps1` after extracting this ZIP into the repository root. It executes the audit and four focused pytest tests, **not** the full suite.

The next implementation must register or reuse a typed Toda (4.5) fact, prove the stable base group, retain generator correspondence, and make a backward GoalExpansion before it is safe to retire the live stable renderer branch.
