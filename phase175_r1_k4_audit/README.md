# EHP Proof Tracer — Phase 175 R1, k=4 Source-First Audit

This is a **read-only audit package**, not a proof-engine patch. It checks all six explicitly registered `k=4` groups (`n=2..7`) against the current typed backward search and the canonical model-backed Web proof view. It does not change inference rules, source facts, production APIs, tests outside this package, or the canonical five project documents.

## Reviewed baseline

The reviewed GitHub repository is `akebono03/ehp-proof-tracer`, branch `develop`, after the Phase 174 R74 closeout. The new audit requires a clean `develop` checkout descended from the Phase 174 main merge `4f87fc5722e85f7365250c07e684e959b71ae8bb`, plus exactly pinned Git blobs for the eleven relevant code/data files. The local `origin/develop` reference is recorded but not required to equal HEAD, because the existing local branch was rebuilt from merged `main`. If a protected source changes, the audit refuses to run until reviewed. The runner never fetches, resets, cleans, stages, commits, or modifies tracked files.

There are seven `sphere.csv` component rows in six `(n,k)` groups: `(4,4)` has two summands. The six targets are `(2,4)`, `(3,4)`, `(4,4)`, `(5,4)`, `(6,4)`, and `(7,4)`.

## Windows PowerShell — installation and execution

Run these commands at the existing repository root. Change the ZIP filename only if your browser saved it under another name.

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'

Expand-Archive `
  -Path "$HOME\Downloads\EHP_Phase175_R1_K4_AUDIT_ONLY.zip" `
  -DestinationPath "." `
  -Force

$script = ".\phase175_r1_k4_audit\run.ps1"

powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw 'Phase 175 R1 DryRun failed' }

powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw 'Phase 175 R1 audit failed' }

git status -sb
```

Each invocation performs **only the new audit package's focused pytest** (not the repository-wide suite). `-DryRun` verifies the six-target CSV scope, reviewed source blobs, and Git worktree; it launches no proof searches. A normal run executes six isolated workers (default timeout 300 seconds per group). To change the timeout, add `-TimeoutSeconds 600`.

## Outputs and interpretation

Outputs are written outside the repository under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r1_k4_audit\<UTC timestamp>\`:

- `report.json`: registered source summands, exact Git source pins, typed DB goals, search status, proof steps, open goals, diagnostics, citation model, trusted completion root, and Web line structures for every inspected group.
- `report.md`: a Japanese six-group table and scope disclaimer (normal run).
- `pi_<dimension>_<n>.log`: stdout and stderr of each isolated worker.

`COMPLETE_AND_WEB_VERIFIED` requires a typed DB goal, matching completed search root, explicit proof trust verification, a root in the shared Narrative Model, no open goals, and a complete canonical Web proof. `INCOMPLETE_AND_WEB_CONFIRMED` is a genuine unfinished proof, **not an audit execution failure**. Worker failures, timeout, unverified complete claims, and status disagreement fail the audit. An observation cannot be promoted from a registered database group structure alone.

Results from this package are **not** independent formal verification of Toda's propositions or of every possible inference rule. They are observations of the current public pipeline. Phase 175 R1 makes no new GIVEN registrations and no mathematical rules. The full active `tests/` pytest is reserved for the **end of Phase 175**. No claim of a completed six-group audit is made until the real Windows checkout produces its report.

## Package contents

`audit.py`, `run.ps1`, `tests/test_audit.py`, package initializers, this English README, `AUDIT_PLAN_JA.md`, and `CODE_FULL_JA.md`. All newly introduced Python function bodies, imports, and the complete PowerShell launcher are included without omissions in the Japanese full-code documentation.
