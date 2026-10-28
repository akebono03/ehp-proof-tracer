# Phase 169 closeout — R3B Gate report ancestry fix

R3A's final active test suite passed before the audit-only packages were committed. The original R3 documentation validator accepted only two exact Gate-report commit hashes. That incorrectly rejected successful Gate reports taken at an intermediate reviewed commit. R3B accepts a report HEAD only when the Git merge-base checks show it is on the reviewed path from `6e5d6bbed186dd4da706b54c308f94041a32e6d7` to `1e881f45b2f3f3ecbb1052750c9d7a7b5bf95712`.

All other requirements remain: expected Gate mode and decision, 13 reviewed files, 19-case R6 evidence, 67 focused passes, 3,546 active-suite passes, exit code zero for each, preserved Git index, exact active pytest command and both log files on disk. A nonexistent, malformed, unsuccessful or out-of-range report is rejected with a specific reason. Do not fabricate reports or rerun the full suite.

R3B includes a complete, standalone replacement `run.py`, plus the original reviewed complete `run.py` and revised complete source. R3B does not overwrite or delete the old untracked R3 package. On successful verification it updates only the five closeout documents, backs up their entire before/after contents under `%LOCALAPPDATA%\EHPProofTracerRecovery`, and checks preservation of the Git index. It does not modify production code, mathematical rules, existing tests, stage/commit anything, or run full pytest. It retains the `--prepare-only` option.

## Run

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_PHASE169_CLOSEOUT_R3B.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_phase_closeout_r3b_gate_head_fix\run.ps1"
git -c core.longpaths=true status -sb
git -c core.longpaths=true diff --stat -- README.md docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md
```

The original R3 failure wrote no documents. This package keeps the original R3 folder and all audit folders intact. Do not use `git add -A`, `git clean`, `git reset`, `git restore`, or an unconditional `git pull`.

A successful local documentation closeout is not a GitHub commit. Review the five changed files before any future, explicit staging or commit. Phase 170 mathematical/DB audits remain separate.
