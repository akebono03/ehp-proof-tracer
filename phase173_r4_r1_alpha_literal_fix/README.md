# Phase 173 R4-R1: alpha TeX fix — pytest collection repair

This package retains the reviewed, guarded, idempotent alpha TeX correction and its committed-Narrative preflight support. The only execution change is to use pytest's `--import-mode=importlib` when running the focused test set. Two independent Phase 173 directories contain `tests/test_live.py`; ordinary pytest import mode imports both as the same top-level module `test_live`, causing an `import file mismatch` collection error. The importlib mode collects both files independently.

## Changed files

- `phase173_r4_r1_alpha_literal_fix/run.ps1`: the full script is provided, with the focused pytest invocation changed to include `--import-mode=importlib`.
- `phase173_r4_r1_alpha_literal_fix/tests/test_install.py`: one offline regression check for the runner invocation was appended. There are no new imports.
- `README.md` and `変更内容.md`: complete updated documentation.

No production mathematics, source statement, Web adapter, projection, installer, or existing test APIs are changed by this runner-only repair.

## Windows PowerShell

Extract the ZIP into the EHP Proof Tracer repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r1_alpha_literal_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r1_alpha_literal_fix\run.ps1"
```

Since the earlier attempt already reported `PHASE173_R4_R1_ALPHA_INSTALL=INSTALLED`, the installer is expected to report `ALREADY_INSTALLED` on a rerun. This is a normal, verified idempotent state. The post-installation tests and both public Web proof verifiers still run.

Run only the focused tests during R4-R1. The repository-wide pytest run is reserved for the end of Phase 173.
