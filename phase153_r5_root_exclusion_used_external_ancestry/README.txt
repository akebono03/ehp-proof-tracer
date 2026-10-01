Phase 153-R5
=============

Theme
-----
root exclusion + used external ancestry preference
(root 除外 + 実際に使われた外部 ancestry 優先)

Scope
-----
Production changes are intentionally minimal.

1. toda_group_proof_narrative_references.py
   Function:
   select_toda_group_proof_narrative_reference_statement_steps()

   Change:
   - Add optional root_step argument.
   - Exclude root_step from external Reference statement candidates.
   - Among remaining candidates, prefer steps actually used as proof-edge premises.
   - Preserve the previous first-candidate fallback for external candidates.
   - Keep backward compatibility when root_step is omitted.

2. toda_group_proof_narrative_contribution_renderer.py
   Function:
   _toda_group_proof_narrative_reference_statement_lines_by_number()

   Change:
   - Pass presentation.root_step to the selector.

3. tests/test_phase153_r5_reference_selection.py
   Added focused tests for:
   - root exclusion,
   - root-only candidate -> no external statement,
   - used external ancestry preference,
   - backward compatibility.

Not included in R5
------------------
- No n=2-specific rule.
- Proposition 5.15 is not removed from provenance.
- Reference prose/wording is not redesigned.
- Reference numbering/granularity is not globally redesigned.
- No unrelated refactoring.
- No full pytest run.

How to run
----------
Extract this directory directly under the ehp-proof-tracer repository root.

PowerShell:

cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r5_root_exclusion_used_external_ancestry" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r5_root_exclusion_used_external_ancestry.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r5_root_exclusion_used_external_ancestry\run_phase153_r5.ps1"

Focused pytest
--------------
python -m pytest -q `
  ".\tests\test_phase153_r5_reference_selection.py" `
  ".\tests\test_phase144_6_r3_structured_references.py" `
  ".\tests\test_phase144_6_r3_production_references.py"

Representative audit
--------------------
The audit covers:

- pi_4^2
- pi_5^2
- pi_6^2
- pi_7^2
- pi_8^2
- pi_9^2
- pi_10^6
- pi_12^7

Completion conditions
---------------------
- presentation.root_step is never selected as an external Reference statement.
- When an external candidate is actually used as a premise in the Proof graph,
  that used candidate is selected before an unused external candidate.
- Existing selector calls without root_step remain valid.
- Existing structured/prod Reference focused tests remain green.
- Representative audit reports no root-selected failure.

Boundary to the next R
----------------------
R5 only fixes root exclusion and used external ancestry preference.

Reference granularity, prose quality, numbering, and broader Reference
selection policy remain outside this R and should be handled separately.
