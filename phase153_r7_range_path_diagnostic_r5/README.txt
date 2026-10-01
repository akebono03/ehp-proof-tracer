Phase 153-R7 R5 Range Path Diagnostic
=====================================

Purpose
-------
Do not make another production change yet.

R4 removed all unwanted Proposition 5.6 group-result siblings from the pi_6^2
proof body, but n >= 6 remains.

This diagnostic prints the actual Proof-graph paths from every n >= 6 step to
presentation.root_step under three conditions:

1. no exclusions;
2. aggregate step excluded;
3. aggregate step plus every unselected direct aggregate sibling excluded.

It also prints:
- the selected Proposition 5.6 component;
- the retained direct premise;
- all unselected direct premises;
- the current pi_6^2 proof body.

Production changes
------------------
None.

Tests
-----
None. This is an audit-only package.

Run
---
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r7_range_path_diagnostic_r5" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r7_range_path_diagnostic_r5.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r7_range_path_diagnostic_r5\run_phase153_r7_range_path_diagnostic_r5.ps1"

Please paste the complete diagnostic output back into the chat.
