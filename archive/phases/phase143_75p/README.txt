Phase 143-75P
=============

Changed files
-------------
toda_group_proof_narrative_renderer.py
tests/test_phase143_75p_prop44_suspension_injective_semantic_rendering.py

Import changes
--------------
None.

New function
------------
Insert immediately before _render_group_proof_narrative_latex:

def _render_prop44_suspension_injective_statement_latex(
  statement,
) -> str | None:
  if (
    type(statement).__name__
    != "TodaProp44SuspensionInjectiveStatement"
  ):
    return None

  suspension_map = statement.map

  return (
    "E: "
    + render_toda_primary_group_latex(
      suspension_map.source_group
    )
    + r" \hookrightarrow "
    + render_toda_primary_group_latex(
      suspension_map.target_group
    )
  )

Changed function
----------------
_render_group_proof_narrative_latex

Immediately after:

  statement = proof_step.conclusion

add:

  prop44_suspension_injective_latex = (
    _render_prop44_suspension_injective_statement_latex(
      statement
    )
  )

  if (
    prop44_suspension_injective_latex
    is not None
  ):
    return prop44_suspension_injective_latex

Tests added
-----------
test_phase143_75p_all_target_occurrences_render_semantically
test_phase143_75p_both_rule_families_use_same_semantic_renderer
test_phase143_75p_concrete_map_uses_source_and_target_groups

Implementation boundary
-----------------------
Only TodaProp44SuspensionInjectiveStatement is connected.
No other remaining fallback statement type is changed.
No rule-name parsing is used.
No proposition-specific prose is used.

Expected
--------
3 passed

target occurrences: 55
semantic renderings: 55
rule-name fallback: 0
errors: 0
PASS

Expected global fallback after 75P:
465 - 55 = 410

The full pytest suite is not run.
