# Phase 168 R3-41P2 — Renderer Responsibility Audit Launcher Repair

This package runs a focused read-only audit of proof validation versus narrative rendering in EHP Proof Tracer. It uses the project's real proof search, typed narrative model, common renderer, and frozen textual benchmarks.

**Scope:** This package corrects the audit launcher and updates only one legacy test assertion whose wording no longer matches the R3-41O renderer. No application renderer, proof search, mathematics, citation model, or existing API is changed. The full pytest suite remains deferred until the end of Phase 168.

## Run on Windows PowerShell

From the repository root:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p2_runtime_and_test_fix.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p_boundary_audit\run.ps1"
```

The launcher runs the audit module with `python -B -m phase168_r3_41p_boundary_audit.audit` from the repository root. Running `python -B path/to/audit.py` directly is not supported because sibling project modules may not be on `sys.path`.

It first verifies and backs up a single stale test assertion in `phase168_r3_29_order_projection/tests/test_phase168_r3_29_order_projection.py`. Only `test_pi32_all_steps_preserved_without_suppression()` is changed, replacing the requirement for the exact phrase `零写像である` with the already-proven equation `\operatorname{Im}\Delta=\ker E=0`. The test still checks all steps in the order projection and the single complete sequence. On unfamiliar contents the patch refuses to run rather than overwriting the test.

## Restore the old test

From the repository root:

```powershell
python -B -m phase168_r3_41p_boundary_audit.restore_test
```

The restore tool verifies both SHA-256 hashes and refuses to overwrite later edits. The original bytes are retained under `phase168_r3_41p_boundary_audit/output/backups/`. No application source file is touched.

## Run without focused pytest

```powershell
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p_boundary_audit\run.ps1" `
  -SkipTests
```

The test assertion will still be backed up and updated. Use `restore_test` to revert it.

## Results

The launcher collects the audit output in `phase168_r3_41p_boundary_audit/output/`:

- `audit.md` and `audit.json`: static findings, proof/citation linkage, runtime validation calls, and group-by-group status
- `pi3_2_current.md`, `pi4_3_current.md`, `pi5_4_current.md`: full generated narrative and Reference sections
- `pi*_proof.diff`, `pi*_reference.diff`: frozen baseline textual differences when available
- `test_patch.log`: trace of the one-test-only patch
- `audit_console.log`, `pytest_focused.log`: standard output and errors also saved separately
- `git_status_before.txt`, `git_status_after.txt`: track modifications
- `review_bundle.zip`: consolidated output, even on an audit or test failure

### Validation

The launcher executes only focused tests for R3-41O, R3-41N1, R3-29, R3-39A, R3-8 and audit-runner tests. It does not execute the full suite. Any nonzero audit or pytest status is reported honestly and propagated as a nonzero process exit code.

See `R3-41P2_REPAIR.md` for the precise change list, complete replacement test function, completion conditions, and next-phase boundary.
