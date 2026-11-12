# Phase 175 R3R4 — Audited R2-to-R3 Git Lineage Correction

## Observed failure

The user's R3R3 Windows DryRun passed **112 focused tests** and the scoped
R3-only worktree guard but failed with `R3_R2_LINEAGE_NOT_AUDIT_ONLY`.
The R2 normal report was recorded before the Phase 175 R3 audit directory was
committed. The old `verify_lineage()` permitted only additions beneath the R2
audit directory. Thus legitimate additions of the isolated R3 audit package
were rejected **before any R3R2 proof-search worker ran**.

## Exact scope

The only modified Python files are `audit.py` and `tests/test_audit.py` in
`phase175_r3_pi73_hopf_lift/`.

- `audit.py` introduces the explicit `R3_LINEAGE_ALLOWED_ADDITIONS` set and
  fully replaces `verify_lineage()`. The rule now accepts R2 audit-directory
  additions and **only the twelve named R3 package paths** with Git status
  `A` between the original R2 recorded HEAD and the current HEAD.
- Any modification, deletion, rename, or addition outside that exact boundary
  is rejected. Git ancestry is still mandatory. The prior R1/R2/R3 source
  pins, working-tree snapshot, no-staged-changes rule, and postflight hashes
  are unchanged. The full accepted path list is recorded in `report.json`.
- `tests/test_audit.py` adds four real-Git DAG regression tests: mixed R2/R3
  audit additions, unknown R3 addition, change to an already committed R3
  file, and simultaneous audit addition plus production change.
- `README.md`, `AUDIT_PLAN_JA.md`, and `CODE_FULL_JA.md` contain the full
  current documentation and source listings.

No mathematical rule, literature `GIVEN`, source registry, public provider,
Web renderer, or previous R1/R2 code is modified. The existing `run.ps1`,
`rule.py`, and `frontier.py` are byte-for-byte retained.

## Run on Windows PowerShell

Extract the complete ZIP at the root of the existing `develop` checkout:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R3R4.zip" -DestinationPath "." -Force
$script = ".\phase175_r3_pi73_hopf_lift\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R4 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R4 audit failed" }
git status -sb
```

The expected DryRun gate is `PASS_R3_READ_ONLY_DRYRUN`. The normal run
then executes the existing three-premise isolated Hopf-lift diagnostic. The
proof is **not** asserted complete merely because Git lineage passes.

The audit writes reports under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r3_pi73_hopf_lift`.
Only focused pytest runs in this phase. Full-suite pytest remains deferred
until the Phase 175 closeout.
