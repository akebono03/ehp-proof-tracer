Phase157-R20 repair5

Purpose
-------
Fix the NameError introduced by repair4.

Cause
-----
repair4 added the generic helper

  _normalize_generic_eta_family_latex()

to `toda_group_proof_generic_narrative_renderer.py`.

`toda_group_proof_narrative_contribution_renderer.py` calls that helper from
the generic eta-suspension bridge logic, but repair4 forgot to import it.

Change
------
Update the existing import block:

from toda_group_proof_generic_narrative_renderer import (
  _normalize_generic_eta_family_latex,
  _render_generic_narrative_step,
)

Changed file
------------
- toda_group_proof_narrative_contribution_renderer.py

No function changes.
No test changes.
No documentation changes.
No pi_6^3-specific logic.
No repository-wide pytest.
