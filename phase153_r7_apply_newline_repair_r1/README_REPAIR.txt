Phase 153-R7 Apply Newline Repair R1
====================================

Observed failure
----------------
The first R7 package stopped before modifying production files:

ValueError: illegal newline value: \n

Cause
-----
The generated apply script passed the literal backslash+n value to
Path.write_text(..., newline=...), instead of Python's newline character.

Scope of this repair
--------------------
Only the apply script packaging defect is fixed.

The R7 production design, test file, audit script, and focused-test scope are
unchanged.

The failed first run did not write the production files because Path.open()
rejected the newline value before opening the destination for writing.

Run
---
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r7_apply_newline_repair_r1" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r7_apply_newline_repair_r1.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r7_apply_newline_repair_r1\run_phase153_r7_apply_newline_repair_r1.ps1"

Full pytest remains deferred until the end of Phase 153.
