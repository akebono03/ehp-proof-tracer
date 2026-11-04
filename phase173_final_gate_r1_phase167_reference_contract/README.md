# Phase 173 Final Gate R1 — Phase 167 Reference Test Contract Fix

This package corrects the **historical test boundary**, not the mathematical proof or public renderer. The Phase 173 active-suite run at HEAD `ac9149beaf91eeef382bc816234bd2d895398667` reported **3,541 passed and 5 failed**. All five failures originated from the three Phase 167 test files below: they looked for a `証明` heading in `WebGroupProofView.rendered_lines`, although `canonicalize_proof_layout()` now replaces that inner heading with a single `separator` between Reference and Proof.

## Files replaced in full

- `tests/test_phase167_r2_range_dedup.py`: change `_reference_text()` only.
- `tests/test_phase167_r2_shared_reference.py`: change `test_phase167_r2_pi43_reference_has_two_general_results()` only.
- `tests/test_phase167_r2_unified_reference.py`: change `_reference_text()` only.

No imports change. All existing assertions about general theorem statements, reference multiplicity, citation provenance, and exclusions remain intact. The replacement is status-agnostic and does not add any dimension-specific implementation logic.

## Run on Windows PowerShell

Extract `EHP_Phase173_FINAL_GATE_R1_PHASE167_REFERENCE_CONTRACT_FIX.zip` at your Git repository root, then run:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_final_gate_r1_phase167_reference_contract\run.ps1' -DryRun
if ($LASTEXITCODE -ne 0) { throw 'Phase 173 final R1 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_final_gate_r1_phase167_reference_contract\run.ps1'
if ($LASTEXITCODE -ne 0) { throw 'Phase 173 final R1 focused test failure' }
git --no-pager status -sb
git --no-pager diff --stat
```

DryRun verifies seven reviewed Git blobs, checks all three old test files, and writes **complete** replacement sources to `full_changed_tests/`, with all imports, as well as `FULL_CHANGED_UNITS.md`. It never modifies production files. The isolated patch contract has nine tests. Apply backs up the original bytes, writes exactly the three test files, and runs **only** the three test modules (six cases). On focused-test failure it restores the prior files from byte-exact backups. The existing failed phase-end report remains untouched. The full original test sources are embedded and verified against their reviewed Git blob IDs. All writes are without `git reset`, `git clean`, `git add`, or `git commit`.

## Closure boundary

This step does **not** rerun the active full suite and does **not** formally close Phase 173. After focused tests pass, the previously failed report must be preserved and a **reviewed, new final-Gate report** should be produced after any necessary Git reconciliation. Do not rerun the earlier `phase173_final_gate/run.ps1` unchanged: it rejects an existing failed report and uncommitted test updates.

The current HTML/visual review and mathematical proof state remain unaffected. In particular, certified abstract group structures are not promoted to completed named-generator proofs.
