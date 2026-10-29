# Phase 170 R3-R9: Cited Generator Equality for Toda (5.2)

This guarded patch resolves the final audited `n=2` database group proof gap
at `k=12`, without weakening the existing 32 proved cases. The chapter VII
Toda (7.12) equality is checked against a pinned adopted-TeX Git blob,
reconstructed from HyoujiGen.csv IDs and independently registered with a
publication position. It is a cited proof premise, not a database assumption.

Run `run.ps1 -DryRun`, then `run.ps1` from the extracted folder. The runner
requires the reviewed `develop` HEAD and clean tracked files, saves original
files in the recovery folder, runs focused tests and active Web trust-gate
checks, and restores only this Phase's changes if verification fails.

The patch modifies two existing Python modules and adds one source module.
It does not modify `sphere.csv`, the trust boundary, the Web renderer, or
canonical documentation. Full repository pytest is deliberately excluded.
