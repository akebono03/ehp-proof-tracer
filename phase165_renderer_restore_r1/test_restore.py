from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal


def test_completed_pi32_uses_restored_presentation_adapter():
    import phase165_r56_presentation_adapter as adapter
    source = Path(adapter.__file__).read_text(encoding='utf-8')
    assert 'build_complete_toda_group_result_proof_replay(group_result)' in source
    assert 'return render_toda_group_proof_narrative_markdown(presentation)' in source
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    rendered = render_partial_proof_markdown(result)
    assert 'GeneratorSuspension（数式表示未対応）' not in rendered
    assert '証明' in rendered


def test_completed_pi43_remains_renderable():
    result = search_group_from_registered_goal(n=3, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    rendered = render_partial_proof_markdown(result)
    assert '証明' in rendered
    assert '以上より' in rendered
