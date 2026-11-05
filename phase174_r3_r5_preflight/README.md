# EHP Proof Tracer — Phase 174 R3-R5 Preimplementation Audit

This is a **read-only** source, code, and public-proposal audit that prepares a typed finite cyclic extension rule. It does not yet implement that rule or complete the named proof for `pi_8^5`.

The audit checks the source clauses in Toda (4.8), (5.5), and Proposition 5.6; checks that the Phase 174 R3-R4 `Delta=0` provider is still installed; inspects actual citation-screened root and cyclic-child proposals; and verifies that `Delta=0` is available as a proposed inferred consequence, not as a direct GIVEN.

It supports both the previous local HEAD `b5f5208a` with its reviewed two-line working-tree patch and the subsequently merged GitHub HEAD `7ad6ae86`. Other HEADs fail closed. This audit never modifies the repository, stages files, installs packages, performs Git synchronization, or runs the full pytest suite. The remote branch must still equal the reviewed commit; re-audit is required if it changes.

Unzip into the repository root and run `run.ps1 -DryRun` before `run.ps1`. The focused test run adds four tests and runs the previously available R3-R3 rule tests. Results are written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r5_preflight\audit.json`.

## Phase boundary

R3-R5 implementation still requires a cited typed general conditional Toda (4.8), source-backed (5.5) specialization, verified earlier cyclic-group proof reuse, and a general typed extension rule that checks the two suspension maps, index two, the doubled generator and all group orders. It must not assert any of these as a new group-specific GIVEN.
