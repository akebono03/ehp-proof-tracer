# Phase 173 R4-R10R1 — Reviewed HEAD-Lineage Correction

This package corrects the stale repository HEAD in the **isolated** R4-R10 verification module. GitHub `develop` at commit `924888b257f9fed1e2d34790127b4ff108a7badb` differs from the former `7158a7f544cd7c6750ebdf82a3b946caa980ea04` only by the committed R4-R9 audit directory. The ten reviewed source blobs remain identical.

## Modification boundary

The only modified existing file is `phase173_r4_r10_general_toda56_core/verify.py`. Its sole textual modification is the **complete** constant assignment `REVIEWED_HEAD`. The complete replacement module is included in `replacement_verify.py.txt`. None of its imports, classes, or functions change. The original `core.py`, `run.ps1`, regression tests, production code, and public Web routes remain intact.

New files under `phase173_r4_r10r1_head_lineage_fix/` are `apply.py`, `run.ps1`, `tests/test_apply.py`, `replacement_verify.py.txt`, `__init__.py`, this README, and `監査計画.md`.

The installer requires the exact local and remote `develop` commit, a clean tracked worktree, ten source blobs, and exact byte checksums of the existing `core.py`, `run.ps1`, test, and `verify.py`. It refuses conflicts. A DryRun writes nothing; a normal run atomically patches only the known verification module and then executes the existing R4-R10 DryRun, isolated verification, and focused pytest.

## Run on Windows PowerShell

At the `ehp_proof` repository root, extract `EHP_Phase173_R4_R10R1_HEAD_LINEAGE_FIX.zip` from Downloads and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r10r1_head_lineage_fix\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r10r1_head_lineage_fix\run.ps1'
```

This does **not** certify `pi_11^4` as a complete public proof. R4-R11 source screening and public connection remain future work. No full-suite pytest runs until Phase 173 closeout.
