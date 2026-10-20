# Phase 166 R3-J: Proof-use order correction

This package supersedes the **unapplied** Phase 166 R3-I package. Apply it to a checkout where R3-H is already installed and R3-I has **not** been applied.

Run `run.ps1` from the repository root. The guarded installer backs up all changed Python modules, prints entire changed functions, and executes focused tests only. No full test suite is run.

Scope: the five separately typed Proposition 5.1 clauses are assigned the accepted proof-use order: Hopf relation, pi3^2, delta relation, pi4^3, higher eta relation. Existing public entry points and the composite reference are retained. The broader migration of cross-reference ordering and the legacy publication-position field is NOT completed by this patch.
