"""R56 の旧 import を現行 shared components に合わせて検査する。"""
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import diagonal_suspension_subgoals
from proof import ProofRule, ProofStep
from toda_group_proof_narrative_shared_components import _render_generic_narrative_step


def test_shared_generator_suspension_is_rendered_as_math():
    suspension = TodaSuspensionMap(TodaPrimaryGroup(1, 1), TodaPrimaryGroup(2, 2))
    statement = diagonal_suspension_subgoals(suspension)[2]
    rendered = _render_generic_narrative_step(
        ProofStep(conclusion=statement, premises=(), rule=ProofRule.GIVEN)
    )
    assert "GeneratorSuspension" not in rendered
    assert "E(" in rendered
    assert "\\iota" in rendered


def test_completed_pi32_uses_shared_generator_math():
    from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    rendered = render_partial_proof_markdown(result)
    assert "GeneratorSuspension（数式表示未対応）" not in rendered
    assert "E(" in rendered
