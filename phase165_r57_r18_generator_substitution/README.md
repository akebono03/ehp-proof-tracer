# Phase 165 R57-R18: Proved Generator Substitution

This patch opens the typed pi4^3 generator-notation route without admitting the direct Proposition 5.1 target-group specialization as proof.

- New generic rule: finite cyclic generator replacement requires a separately proved equality.
- Typed adapter accepts `η_3` and `η₃` when metadata match.
- Root-order gate allows only the guarded substitution step, not direct structural self-reference.
- No new GIVEN facts, persistent ProofSteps, or unrelated renderer changes.

The patch does **not** certify completion of the pi4^3 or pi5^4 proofs. Further subgoals may remain open.

Run `run.ps1` from Windows PowerShell after extracting this directory into the repository root. Full pytest is not run.
