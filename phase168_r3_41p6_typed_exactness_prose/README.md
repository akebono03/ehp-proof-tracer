# Phase 168 R3-41P6 — Typed Exactness Prose Without Rule-Name Matching

This patch updates only `typed_sentence()` in `phase168_r3_27_typed_statement_projection.py`.

It removes a string-based condition that treated inference rule names containing `exact` as evidence for the phrase “by exactness.” Instead, it uses typed EHP exactness steps already in the Proof Tree. Recursive ancestor traversal remains unchanged.

## PowerShell

From the EHP Proof Tracer repository root:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p6_typed_exactness_prose.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p6_typed_exactness_prose\run.ps1"
```

The patch validates the prior source SHA-256, writes a backup, then runs only focused pytest files. Test failure triggers automatic rollback.

## Outputs

- `output/typed_sentence_FULL.py`: full updated function
- `output/full_files/phase168_r3_27_typed_statement_projection.py`: full updated file
- `output/backups/phase168_r3_27_typed_statement_projection.py`: original file
- `output/pytest_stdout.log`, `output/pytest_stderr.log`: focused pytest
- `output/post_patch.json`: before/after checksums

To restore manually (only if source remains unchanged since the patch):

```powershell
python -B -m phase168_r3_41p6_typed_exactness_prose.restore
```

This patch does not change source references, proof rules, the Proof Tree or the Narrative Model. It is not a Phase 168 full-suite run.
