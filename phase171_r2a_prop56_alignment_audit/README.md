# Phase 171 R2A — Read-only Proposition 5.6 alignment audit

This package compares the **actual typed** `sphere.csv`-derived group proof goals for `n=3,4,5; k=3` with the existing typed Toda Proposition 5.6 *candidates* in `phase165_r6_explicit_literature_inputs.py`. It inspects the matching assertions and linked proof steps in the shared registry. **It does not prove, register, adopt, or edit any mathematical statement.** A `SOURCE_UNVERIFIED` candidate is not an admissible proof leaf.

Preflight requires `develop` to match `origin/develop`, a clean tracked tree, and a history descending from the reviewed `715b00d6` baseline. Every committed path since that baseline must be inside the explicitly reviewed Phase 171 R1, R1C, R1D, or R2A audit directories; otherwise the audit refuses to proceed. The pinned production code/data blobs remain mandatory. In particular, the verified `912322af` R1D-only commit is accepted without hardcoding new commit IDs. The source R1C `audit.json` is validated against the complete 32-group result (29 complete and the three known gaps). Untracked Phase 171 audit folders do not prevent inspection.

Unzip the archive at the root of `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`, then run:

```powershell
$Audit = Join-Path $env:LOCALAPPDATA "EHPProofTracerRecovery\phase171_r1c_k3_20261029_061130_694213\audit.json"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2a_prop56_alignment_audit\run.ps1" -ReportPath $Audit -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2a_prop56_alignment_audit\run.ps1" -ReportPath $Audit
git status -sb
```

The PowerShell runner launches `python -B -m phase171_r2a_prop56_alignment_audit.audit` from the repository root, instead of executing `audit.py` by path. This preserves root-level module discovery for `phase165_r52_r9_shared_math.py` and other project imports. The DryRun mode does not exercise these imports, so the regression tests cover the module entrypoint and sibling-import behavior.

`alignment.json` and `alignment.md` are written only under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2a_prop56_*`. Send the `PHASE171_R2A_DETAIL` lines or the report to evaluate differences and source-link status before choosing the first mathematical implementation. Focused tests only; the full suite remains Phase-final.
