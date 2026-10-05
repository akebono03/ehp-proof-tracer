Phase 158-R5-5b repair1o — contribution rendered-reflexive suppression

repair1n diagnosis
==================
The public pipeline was traced stage by stage.

Base multi-Argument:
- eq1 tagged: present
- eq2 tagged: present
- connector: present
- eq3 plain: present

The first destructive stage is:

suppress_toda_group_proof_narrative_reflexive_equalities()

Immediately after that stage:
- eq2 disappears
- eq1 remains
- connector remains temporarily

Then:

suppress_toda_group_proof_narrative_dangling_connectors()

removes the connector because eq2 is gone.

Root cause
==========
Contribution-level reflexive suppression still uses the old rule:

1. render lhs
2. eta-family normalize lhs
3. render rhs
4. eta-family normalize rhs
5. suppress if normalized sides match

This incorrectly treats:

eta_3 eta_4 eta_5 = eta_3^3

as reflexive.

Repair
======
Use actual generic public step rendering.

Suppress only when the displayed equality itself has identical lhs/rhs.

Keep:
eta_3 eta_4 eta_5 = eta_3^3

Suppress:
eta_3^3 = eta_3^3
eta_5 = eta_5

Changed production file
=======================
toda_group_proof_narrative_contribution_renderer.py

Changed:
- generic renderer import block
- suppress_toda_group_proof_narrative_reflexive_equalities()

Removed imports:
- _normalize_generic_eta_family_latex
- _render_generic_narrative_expression_latex

No group-specific logic.

Tests
=====
Focused tests only.
No repository-wide pytest.

Boundary
========
This repair addresses contribution-level reflexive suppression only.

If eq3 remains untagged after this repair, equation numbering is treated as a
separate remaining R5-5b issue and will be diagnosed/fixed separately.
