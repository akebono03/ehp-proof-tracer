"""Strict, literal patches against R15R16 installed local files and tests."""
from __future__ import annotations

from phase173_r4_r15r16_verified_progress_punctuation.projection_patch import (
    PROJECTION_NEW,
    PROJECTION_OLD,
    patch_projection,
    patch_layout,
)

PROGRESS_NEW = 'def _verified_abstract_progress_lines(\n    structure: CertifiedAbstractStructure,\n) -> tuple[str, ...]:\n    """Render the existing certificate via the same common Narrative renderer.\n\n    No proof-specific prose, four-premise assumption, or new inference.\n    """\n    from phase173_r4_r15r16r3_staged_guard_fix.tree_adapter import (\n        render_verified_tree_progress,\n    )\n\n    return render_verified_tree_progress(\n        structure.group, structure.proof_step,\n    )\n'
REPLACEMENT_TEST = '@pytest.mark.parametrize("k", (8, 9, 15, 31))\ndef test_abstract_certificate_displays_actual_verified_milestones(k: int) -> None:\n    goal = exact_prior_database_result(4, k)\n    assert goal is not None\n    result = search_group_from_registered_goal(n=4, k=k, goal=goal)\n    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)\n    assert result.conclusion is None and result.open_goals\n    assert result.abstract_structure is not None\n    assert result.abstract_structure.proof_step not in result.proven_steps\n\n    model = build_proof_narrative_model(result)\n    progress = render_certified_abstract_model_section(model)\n    assert progress == render_certified_abstract_section(result)\n    assert "## 検証済みの途中経過" in progress\n    assert "### 検証済み証明木の Reference" in progress\n    assert "### 検証済み ProofStep" in progress\n    assert "Proposition 4.4" in progress\n    assert "Lemma 5.4" in progress\n    assert progress.count("DB prior: sphere.csv") >= 2\n    assert "## 証明済みの抽象群構造" in progress\n    assert "記名生成元の対応は未証明" in progress\n    assert "先行データベースの " not in progress\n    assert "Proposition 4.4 の適用前提となる定理を検証した" not in progress\n    assert progress in render_model_backed_narrative_markdown(result, model)\n\n    view = build_standard_web_group_proof_view(\n        n=4, k=k, goal=goal, mode="narrative", citation_source="model",\n    )\n    assert view.partial_result and view.abstract_structure_certified\n    assert view.key == "generic-partial-proof"\n    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]\n    assert headings.count("検証済みの途中経過") == 1\n    assert headings.count("証明済みの抽象群構造") == 1\n    assert headings.count("未解決 Goal") == 1\n    shown = "\\n".join(\n        seg.value for line in view.rendered_lines for seg in line.segments\n    )\n    assert "sphere.csv" in shown and "Lemma 5.4" in shown\n    assert "Relation(lhs=" not in shown\n    assert "、" not in shown and "。" not in shown\n    assert result.conclusion is None and result.open_goals\n'


def patch_progress(source: str) -> str:
    # R15R16 generated this exact installed source from the reviewed HEAD.
    marker = "def _verified_abstract_progress_lines("
    end = "\n\ndef _render_abstract_claim("
    if source.count(marker) != 1 or source.count(end) != 1:
        raise RuntimeError("R15R16 progress function boundary not found")
    before, rest = source.split(marker, 1)
    _, after = rest.split(end, 1)
    return before + PROGRESS_NEW + "\n" + end.lstrip("\n") + after


def patch_test(source: str) -> str:
    prefix = '@pytest.mark.parametrize("k", (8, 9, 15, 31))\ndef test_abstract_certificate_displays_actual_verified_milestones'
    suffix = "\n\ndef test_completed_view_has_no_abstract_progress_sidecar()"
    if source.count(prefix) != 1 or source.count(suffix) != 1:
        raise RuntimeError("R15R16 test function boundary changed")
    before, rest = source.split(prefix, 1)
    _, after = rest.split(suffix, 1)
    return before + REPLACEMENT_TEST + "\n" + suffix.lstrip("\n") + after


TRANSFORMERS = {
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py": patch_progress,
    "phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py": patch_test,
}
