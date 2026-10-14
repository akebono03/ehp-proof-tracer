"""The shared renderer must print typed suspension generator images mathematically."""
from phase165_r14_r14_diagonal_and_prop42 import diagonal_suspension_subgoals
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from proof import ProofRule, ProofStep
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step


def test_r56_r1_generator_suspension_uses_shared_math_prose():
    e = TodaSuspensionMap(TodaPrimaryGroup(1, 1), TodaPrimaryGroup(2, 2))
    statement = diagonal_suspension_subgoals(e)[2]
    step = ProofStep(conclusion=statement, premises=(), rule=ProofRule.GIVEN)
    rendered = _render_generic_narrative_step(step)
    assert "GeneratorSuspension" not in rendered
    assert "E(" in rendered
    assert "\\iota" in rendered


def test_r56_r1_pi32_completed_proof_has_no_internal_type_name():
    from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
    from phase165_r55_nk_only_goal import search_group_from_registered_goal

    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    rendered = render_partial_proof_markdown(result)
    assert "`GeneratorSuspension`" not in rendered
    assert "E(" in rendered
