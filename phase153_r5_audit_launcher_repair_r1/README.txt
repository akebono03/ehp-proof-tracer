Phase 153-R5 Audit Launcher Repair R1
=====================================

Purpose
-------
This package repairs only the Phase 153-R5 audit launcher.

The production R5 implementation has already been applied successfully,
and the focused pytest result reported by the user was:

10 passed

Observed packaging defect
-------------------------
The original audit script was executed from the package subdirectory:

phase153_r5_root_exclusion_used_external_ancestry\audit_phase153_r5.py

Python therefore placed that subdirectory, rather than the EHP Proof Tracer
repository root, at sys.path[0]. As a result:

ModuleNotFoundError: No module named 'toda_calculation_facade'

A second launcher issue was that PowerShell continued after the failed native
Python process and printed the completion banner.

Repair
------
1. audit_phase153_r5.py
   - Adds the repository root to sys.path before project imports.
   - Does not change production code.

2. run_phase153_r5_audit_repair_r1.ps1
   - Checks $LASTEXITCODE after every Python/pytest command.
   - Stops with an error if compile, pytest, or audit fails.
   - Re-runs only focused tests and the R5 representative audit.
   - Does not run the full test suite.

How to run
----------
Extract this package directly under the ehp_proof repository root.

PowerShell:

cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r5_audit_launcher_repair_r1" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r5_audit_launcher_repair_r1.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r5_audit_launcher_repair_r1\run_phase153_r5_audit_repair_r1.ps1"

Expected sequence
-----------------
[1/3] compile repaired audit
[2/3] focused pytest
[3/3] representative-group audit

The audit covers:

pi_4^2
pi_5^2
pi_6^2
pi_7^2
pi_8^2
pi_9^2
pi_10^6
pi_12^7

Completion condition
--------------------
The final audit must print PASS and no audited group may report:

root selected: YES

Phase boundary
--------------
This repair changes no production logic.

It only makes the already-applied Phase 153-R5 verification runnable and
ensures a failed native command cannot be mistaken for successful completion.
