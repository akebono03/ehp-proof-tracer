# Phase 171 R2J-R3 — Cited EHP Exactness Consequences

This package derives two generic consequences of a previously certified Hopf surjectivity proof, without adding literature leaves or importing historical completed group proofs.

1. Surjective `H: A -> B` and a cited exact `A -> B -> C` window imply `Delta: B -> C = 0`.
2. Zero `Delta: B -> C` and a cited exact `B -> C -> D` window imply injective `E: C -> D`.

For Phase 171, `A=pi_7^3`, `B=pi_7^5`, `C=pi_5^2`, `D=pi_6^3`. Both windows must be derived from the same earlier, citation-screened Toda Proposition 4.2 source. Surjectivity of H is independently reconstructed from R2J-R2 and R2I inference steps.

## R1 installation repair (committed R2J-R2 baseline)

R2J-R2 is now committed as `8b8deb6ef064e11a230b420d8ae4ae54704e6078`. The earlier R2J-R3 installer incorrectly imported `phase171_r2j_r2_cyclic_hopf_surjective.install` as an external prerequisite. This repaired installer instead reads and checks the **committed Git blob** for `phase165_r52_r9_shared_math.py` at that commit. It requires the checked-out `develop` HEAD to descend from the commit and to carry the identical committed source blob, and rejects unrelated uncommitted source changes. It accepts either LF or CRLF checkouts and preserves the worktree's newline style.

Unpack the ZIP into the repository root and run `phase171_r2j_r3_ehp_exactness/run.ps1 -DryRun`, followed by `run.ps1`. The previous failed preflight made no production changes, so no reset or checkout is required. Existing committed R2J-R2 source/tests stay unchanged. On failure during focused tests or proof audit, the runner restores only its R2J-R3 edit via its hash-checked backup.

The installation generates `output/CHANGED_CODE_FULL_JA.md`, including the full modified function, imports, new files and tests. `CODE_NEW_FILES_FULL_JA.md` is supplied for offline inspection.

The only production edit is a single additive hook in `shared_expansion_provider()` in `phase165_r52_r9_shared_math.py`. No new GIVEN, database, source, renderer or other existing API changes are made. Full pytest is reserved for Phase 171 closeout.

This package does not claim a completed proof of `pi_6^3`.
