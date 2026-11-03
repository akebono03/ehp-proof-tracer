# Phase 173 R4-R15R2R1: Reviewed R15R1 HEAD-Lineage Correction

This package corrects only the preflight commit guard for the **read-only** Phase 173 R4-R15R2 generator-obligation audit. The earlier R15R1 core was committed after the first R15R2 ZIP was prepared. The corrected guard accepts exactly two reviewed commit states:

- `7104222524b63c9c517eaf8e09b8f0825842b316`: the original R15R1 baseline with its precisely transformed core installed locally;
- `c44519a123fdbf2c5ec57fe9c89e2fb1027f41a5`: the audited successor with the same transformed core committed.

The new committed core's Git blob must be `d35600804ecbbc5f8566d52e45a2f6ecf8816347`. The R15R1 patch source, the pre-R15R1 original blob and five mathematical dependencies are independently checked. Other commits, staged changes, altered dependencies and unreviewed local core content remain rejected.

## Scope

Updated: `preflight.py`, `run.ps1`; added `tests/test_head_lineage.py`; documentation: `README.md`, `design.md`, `SOURCE_CODE.md`. No production source files or existing mathematical tests are changed. The R15R2 audit remains strictly diagnostic: it does not create proof steps or declare the named generators proved.

## Windows PowerShell

Extract `EHP_Phase173_R4_R15R2R1_HEAD_LINEAGE_FIX.zip` into the repository root, overwriting the existing `phase173_r4_r15r2_generator_obligation_audit` folder, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r2_generator_obligation_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r2_generator_obligation_audit\run.ps1"
```

Both commands check local and `origin/develop` commits before testing. DryRun runs focused static and lineage checks; regular execution also runs the existing R15R2/R15R1/core focused pytest tests and writes `factor_obligation_report.json` under the extracted folder.

Expected guard: `PHASE173_R4_R15R2_HEAD_LINEAGE=PASS`, `PHASE173_R4_R15R2_CORE_STATE=COMMITTED_PATCH` (for the current committed state), `PHASE173_R4_R15R2_SOURCE_GUARD=PASS`. Actual audit completion requires `PHASE173_R4_R15R2_FOCUSED_PYTEST=PASS`, `PHASE173_R4_R15R2_K31_BASELINE=PASS` and `PHASE173_R4_R15R2_AUDIT=PASS`.

The full test suite is reserved for Phase 173 closeout. A successful audit does **not** imply `pi_35^4` is source-certified with all eight named generators. That is a later inference phase.
