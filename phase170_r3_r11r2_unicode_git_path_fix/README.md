# Phase 170 R3-R11R2 — Unicode-safe Git diff for end-of-phase closeout

This is an audit-harness-only correction for the Windows Git `core.quotePath` default. The previous runner rejected a Japanese Markdown filename added under the approved R3-R10 audit directory because Git returned the filename in octal-escaped quotes (e.g. `"\\347..."`). This did not indicate a mathematical source change or a failure of the 33/33 audit.

## Change and safety boundary

Only `closeout.py::preflight` changes its historical Git diff invocation to `git -c core.quotePath=false diff --name-status <audited-head> HEAD --`. Git now returns UTF-8 path text that the existing Python decoder and exact path allowlist can compare. The reviewed commit IDs, allowed directories, `A`-only restriction, committed source blob hashes, clean tracked tree checks, 33-row validation, and active pytest command remain unchanged. No `git config` modification, checkout, reset, source patch, or documentation rewrite is performed on the user's repository.

The test module now imports this package and retains all prior contract tests. Additional coverage checks a Japanese audit filename with a real temporary Git repository and rejects an added Japanese filename outside the approved directories.

## Windows execution

Extract the ZIP in the repository root. Then:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase170_r3_r11r2_unicode_git_path_fix.zip" `
  -DestinationPath "." `
  -Force
powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\phase170_r3_r11r2_unicode_git_path_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\phase170_r3_r11r2_unicode_git_path_fix\run.ps1"
git status -sb
```

An explicitly specified domain report is supported using `-AuditReport "C:\path\to\audit.json"`. Otherwise the runner selects the latest validated original R3-R10 33-stem audit report in `%LOCALAPPDATA%\EHPProofTracerRecovery`.

`-DryRun` validates the Git boundary and 33/33 report without the full suite. A normal run executes the established Phase 169 active-suite command **once**, only after report validation:

```powershell
python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests
```

The active-suite result and logs are written to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase170_r3_r11_active_closeout_*`. The package does not claim full-suite success in advance. After a successful closeout, update canonical documentation in a separate reviewed phase-final task.

## Contract tests

```powershell
python -B -m pytest -q -p no:cacheprovider .\phase170_r3_r11r2_unicode_git_path_fix\tests\test_contract.py
```

The local isolated contract tests passed 24/24, including the temporary Git repository regression. The Windows full active suite has not yet been run by the assistant.
