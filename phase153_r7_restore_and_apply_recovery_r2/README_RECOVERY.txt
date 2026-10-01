Phase 153-R7 Restore and Apply Recovery R2
=========================================

Why this recovery is required
-----------------------------
The first R7 package passed an illegal newline value to Path.write_text().

On Python 3.10, opening a file with mode="w" happens before the invalid newline
value raises ValueError. Therefore the target file can be truncated to zero
bytes before the exception is reported.

That explains why the next repair attempt could not find the expected
insertion marker.

Recovery source
---------------
The first R7 apply script created this backup directory before attempting any
production write:

phase153_r7_backup_before_apply/

It contains the production files as they existed immediately before R7, i.e.
after the successful Phase 153-R6 work.

Recovery procedure
------------------
1. Restore:
   toda_group_proof_narrative_contribution_renderer.py
   toda_group_proof_narrative_renderer.py

   from:
   phase153_r7_backup_before_apply/

2. Compile the restored files before making any new R7 change.

3. Apply the corrected R7 patch.

4. Compile R7 production/test/audit files.

5. Run only focused tests.

6. Run the representative R7 audit.

No full pytest is run.

Run
---
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r7_restore_and_apply_recovery_r2" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r7_restore_and_apply_recovery_r2.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r7_restore_and_apply_recovery_r2\run_phase153_r7_restore_and_apply_recovery_r2.ps1"

Safety behavior
---------------
The recovery script refuses to continue if:
- phase153_r7_backup_before_apply/ is missing;
- either expected backup file is missing;
- either expected backup file is empty;
- restored production files fail py_compile;
- R7 apply fails;
- focused pytest fails;
- representative audit fails.

Full suite remains deferred until the end of Phase 153.
