Phase 153-R7 Scalar Suppression-Key Repair R6
============================================

Confirmed diagnosis
-------------------
The R5 diagnostic proved that the n >= 6 step has zero paths to the final
pi_6^2 root once the Proposition 5.6 aggregate is excluded.

Therefore the Proof-graph relevance logic is already correct.

The remaining display bug is a rendering-key mismatch:

suppression renderer:
`ScalarGreaterEqualStatement`

actual proof body:
$n \ge 6$

Repair
------
For a suppressed ScalarGreaterEqualStatement, construct the suppression key
using the same scalar LaTeX form used by the legacy narrative body.

Production file
---------------
toda_group_proof_narrative_contribution_renderer.py

Import additions
----------------
from scalar_rules import (
  ScalarGreaterEqualStatement,
)

from toda_human_readable_renderer import (
  _render_scalar_latex,
)

No Proof-graph selection rule is changed.
No theorem-specific branch is added.
No full pytest is run.

Run
---
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r7_scalar_suppression_key_repair_r6" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r7_scalar_suppression_key_repair_r6.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r7_scalar_suppression_key_repair_r6\run_phase153_r7_scalar_suppression_key_repair_r6.ps1"
