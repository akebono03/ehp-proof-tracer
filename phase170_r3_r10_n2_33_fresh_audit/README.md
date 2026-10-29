# EHP Proof Tracer — Phase 170 R3-R10 (fresh n=2 domain audit)

This package runs an **audit only**. It does not patch production code, add literature facts, alter proof inference rules, or run the entire test suite.

## Scope

Run the existing reviewed `phase170_r3_r8_n2_exhaustive_audit/audit.py --worker --k K` for each of the 33 explicit database stems `K=1,...,33`. Each worker invokes ordinary backward proof search and the public trust-gated Web path. The harness requires all proof and Web completion fields, not only a headline status, and saves new observational evidence to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase170_r3_r10_n2_33_...`.

The `k=0` identity group is outside the Toda (5.2) transport domain and is intentionally excluded.

## Requirements

- Windows PowerShell, Python with pytest, and Git.
- Local `develop` at `fdf60522b6d477209e9d8d67720a63f9863e419c`; remote `origin/develop` must still point to that commit.
- The successful, **uncommitted** R3-R9 installation from the preceding R3-R9R2R1 run: the only modified tracked files must be `phase168_r2_toda52_transport.py` and `phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py`.
- The original R3-R9 `source712.py` must be present, with a unique literal `CLAUSE` matching the reviewed Toda (7.12) TeX source.
- The existing committed R3-R8 worker and explicit `data/sphere.csv` records must be available.

## Run

Extract the ZIP at the repository root, then run:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r10_n2_33_fresh_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r10_n2_33_fresh_audit\run.ps1"
git status -sb
```

The launcher first runs **only the 17 contract tests** with pytest caching disabled, preventing changes to tracked `.pytest_cache` files. The audit also enforces UTF-8 in every child process to avoid the previous Windows CP932 output error.

## Acceptance

The successful fresh audit reports:

```text
PHASE170_R3R10_DOMAIN_CHECKED=33
PHASE170_R3R10_DOMAIN_COMPLETE=33
PHASE170_R3R10_DOMAIN_GAPS=0
PHASE170_R3R10_TRACKED_UNCHANGED=True
PHASE170_R3R10_RESULT=DOMAIN_ALL_VERIFIED
```

`audit.json` and each `k_XXX.log` are saved in Recovery, not the Git worktree. In case of failure, the package preserves individual observations and refuses to claim domain completion.

The full pytest suite and Phase closeout documentation remain outside this step.
