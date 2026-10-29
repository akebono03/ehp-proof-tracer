# EHP Proof Tracer — Phase 170 R3-R11 Active Suite Closeout

This package checks the completed Phase 170 R3-R10 audit and runs the **active end-of-phase test suite** without changing application code. It does not edit the five project documents.

## Scope and safeguards

The script requires the reviewed `develop` commit `08382968b5359d6c956b48acec333f127014d4c8`, confirms the remote `develop` revision, checks the committed Git blobs of the proof/audit dependencies, and refuses staged or unstaged tracked changes. Untracked audit packages are left alone.

Before a full suite run, the script locates a fresh R3-R10 `audit.json` under `%LOCALAPPDATA%\EHPProofTracerRecovery` (or accepts an exact explicit file path). It validates all 33 distinct `n=2, k=1..33` rows, the search and Web verification fields, and the previous worker and HEAD identifiers. A dry-run or a summarized count is never accepted in place of those rows.

The full active-suite command matches the previous phase's documented boundary:

```powershell
python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests
```

The `-p no:cacheprovider` option prevents pytest from updating tracked pytest cache files. The tool does not `git restore`, checkout, reset, commit, or modify the project's production Python files. If tests modify tracked files, it flags the change for investigation rather than automatically deleting it.

## Windows execution

Extract the ZIP at the repository root (`C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`), then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r11_active_suite_closeout\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r11_active_suite_closeout\run.ps1"
git status -sb
```

To require an exact earlier report instead of automatic discovery, pass the absolute path with `-AuditReport` to either command.

## Verification and outputs

The focused package contract tests (which **do not run the whole application suite**) can be executed with:

```powershell
python -B -m pytest -q -p no:cacheprovider .\phase170_r3_r11_active_suite_closeout\tests\test_contract.py
```

The tool writes `closeout.json` and, for a real run, `full_pytest.log` under a new `%LOCALAPPDATA%\EHPProofTracerRecovery\phase170_r3_r11_active_closeout_*` directory. It succeeds only if the prior 33/33 proof+Web audit is valid, active pytest exits 0, and the tracked Git state remains clean. A passing active suite is **not** a proof that every mathematical claim in the database or Toda's transcriptions is correct.

The project-wide `README.md`, `docs/design.md`, `docs/development_log.md`, `docs/roadmap.md`, and `docs/proof_records.md` should be updated after the actual full-suite result is reviewed. Do not pre-record a pass.
