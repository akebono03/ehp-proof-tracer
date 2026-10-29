# Phase 171 R2F: Typed Extension Gap Audit

This package is a read-only diagnostic for the proposed proof of the 2-primary cyclic structure of pi_6(S^3). It does not patch application code, register new literature, add ProofSteps, or claim to prove the target.

The diagnostic inspects the current local `develop` checkout, including existing uncommitted R2E changes. It verifies that the (5.3) Hopf and doubling equalities survive publication-order citation screening, compares the DB generator structurally with the cited generator, inspects the root and cyclic-structure backward expansions, and inventories source requirements from Proposition 2.2, Proposition 4.2 (4.4), (5.2), and Proposition 5.3. It can optionally run the existing registered group search.

Run `run.ps1 -DryRun` for a read-only Git-state preflight. Run `run.ps1` for focused pytest plus typed diagnostics, or `run.ps1 -Search` to additionally execute the existing proof search. The report is written outside the repository under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2f_*\audit.json`.

An existing source statement, a backward expansion, and a complete inference are different things. In particular, the report's prerequisite inventory does not certify a group proof. All repository file edits, checkout, reset, and automated Git synchronization are out of scope.
