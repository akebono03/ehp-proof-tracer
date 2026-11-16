# EHP Proof Tracer — Phase 175 R3R6

This package adds an **isolated, source-verified general inference** for Toda Lemma 5.7. It does not modify the production proof engine, public search provider, Web renderer, existing references, or registered group results.

## Mathematical scope

For any degree-compatible element `alpha` in `pi_i(S^3)`, the cited Lemma 5.7 states that `E^2(alpha)` belonging to `2 iota_5 o pi_(i+2)(S^5)` implies `E(eta_2 o alpha) = 0`. The universal conditional is one independently cited fixed statement, and the double-suspension membership is a separate **unproved inference obligation**. In particular, `E(eta_2 o nu-prime)=0` is **not registered as a new GIVEN**.

The package uses the source-verified adopted Chapter V TeX, pinned Git blob `579661138928499ba04a51327f686d9b971b5314`, and reviewed publication-order positions: Lemma 5.7 at 9100, Proposition 5.8 at 9200. The original printed edition is not independently verified.

## Changes

Only the new `phase175_r3r6_lemma57_general/` directory is added. Its `source.py` registers the isolated universal conditional and checks publication ordering; `rule.py` implements a dimension-checked, degree-generic implication; `audit.py` checks R3R5 evidence and attempts the canonical recursive proof search using the isolated statement. Four focused test modules, `run.ps1`, and complete Japanese implementation documentation are included. No production file changes or new specific theorem GIVENs are made.

## Windows PowerShell

Unzip `R3R6R2.zip` to the repository root after the successful R3R5 audit. From the `develop` checkout, run:

```powershell
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R3R6R2.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r6_lemma57_general\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R6 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R6 audit failed" }
git status -sb
```

Reports are saved under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r3r6_lemma57_general\<UTC>\report.json` and `report.md`. They distinguish proving a cited schema from proving its concrete membership hypothesis.

## R3R6R1 Windows UTF-8 regression correction

The first Windows R3R6 DryRun reached 54 passing focused tests and one failed older R3R5 test: `test_report_written_outside_source_tree` opened a UTF-8 Markdown report with Windows Python 3.10's default `cp932` encoding and raised `UnicodeDecodeError`. Only the R3R6 runner is changed: it sets `PYTHONUTF8=1` (default file decoding) and `PYTHONIOENCODING=utf-8` (console I/O) before executing Python. The R3R5 audit, its test, mathematical source and other production files are unchanged. The runner is invoked in a child PowerShell session so the calling PowerShell environment is not changed.

`tests/test_powershell_utf8.py` verifies that both variables precede pytest and the audit process, and that child Python reads non-ASCII UTF-8 Markdown successfully without an explicit encoding argument. A successful test run is not a complete homotopy-group proof.

## Completion and next phase

Successful DryRun gate: `PASS_R3R6_READ_ONLY_DRYRUN`. Successful audit gate: `PASS_R3R6_GENERAL_LEMMA57_FRONTIER_RECORDED`. Neither proves `pi_7^3` complete or changes the Web display. R3R7 must independently derive the concrete double-suspension membership from preceding cited results, then connect the existing zero-generator/zero-image/Hopf-injectivity rules. No full-suite pytest is run until Phase 175 closeout.

## R3R6R2: Git ancestry scope correction (2026-11-16)

The Windows R3R6R1 DryRun passed 57 focused tests and the UTF-8 fix, but stopped with `R3_R2_LINEAGE_NOT_AUDIT_ONLY` before any mathematical audit. Its R3R5 `scoped_preflight()` delegated to the historical R3R4 lineage checker, which recognizes added R2 and R3 audit files but not the subsequently committed R3R5 audit package.

R3R6R2 changes **only** this package's `audit.py` (replaces the delegated lineage check with an exact allowlist), adds `tests/test_lineage.py`, and updates the package documentation. The R1/R2/R3 source pins, R2 report verification, R3 worktree guard, and Toda Lemma 5.7 source verification remain mandatory. Only listed audit-package file additions can occur in the R2-to-current Git history. Modified, removed, renamed, unknown, or production files remain disallowed. No Git reset, staging or commit operation is performed. The audit reports lineage mode and the number of committed R3R5 audit files observed.

Run `run.ps1 -DryRun` and then `run.ps1` as above. The full mathematical conclusion is **not** asserted by either audit gate. The local repository-independent focused tests passed (29 passed, 1 skipped); the skipped module needs the full EHP checkout, which the Windows runner tests.
