"""Phase 169 R2A: cited Toda (5.2) is projected without a proof shortcut."""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_37c_reference_projection import project_reference_bodies
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule


EXPECTED_TODA52_BODY = (
    r"$i\ge 3$ に対し, "
    r"$\eta_2\circ(-):\pi_i^3\xrightarrow{\cong}\pi_i^2$ は同型."
)


def _registry_with_statement(statement):
    return SimpleNamespace(
        assertion=lambda assertion_id: SimpleNamespace(content=statement),
    )


def test_toda52_registered_general_reference_has_full_body():
    registry = _registry_with_statement(Toda52UniversalStatement())
    assert project_reference_bodies(registry, ("toda52",)) == (
        EXPECTED_TODA52_BODY,
    )


def test_toda52_does_not_render_a_different_schema_as_theorem():
    wrong = replace(Toda52UniversalStatement(), map_formula="alpha -> other map")
    registry = _registry_with_statement(wrong)
    assert project_reference_bodies(registry, ("wrong",)) == ()


def test_toda52_unused_assertion_does_not_create_reference_body():
    registry = _registry_with_statement(Toda52UniversalStatement())
    assert project_reference_bodies(registry, ()) == ()


@pytest.fixture(scope="module")
def current_pi42():
    bridge = build_shared_typed_bridge()
    screened = []
    result = search_group_from_registered_goal(
        n=2, k=2, bridge=bridge, context_sink=screened.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert screened
    model = build_linked_proof_narrative_model(result, screened[-1])
    return result, model


def test_live_pi42_uses_real_cited_toda52_given(current_pi42):
    result, model = current_pi42
    assert len(model.steps) == 3
    assert sum(step.rule is ProofRule.GIVEN for step in model.steps) == 2
    assert result.open_goals == ()
    assert len(model.citations) == 2
    by_locator = {item.reference.locator: item for item in model.citations}
    assert set(by_locator) == {"Proposition 5.1", "(5.2)"}
    citation = by_locator["(5.2)"]
    assert citation.assertion_ids
    assert citation.reference_ids
    assert any(
        step.rule is ProofRule.GIVEN
        and isinstance(step.conclusion, Toda52UniversalStatement)
        and index in citation.step_indices
        for index, step in enumerate(model.steps)
    )
    assert citation.statement_bodies == (EXPECTED_TODA52_BODY,)


def test_live_pi42_markdown_shows_toda52_reference_body(current_pi42):
    result, model = current_pi42
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "[R2] (5.2)" in markdown
    assert EXPECTED_TODA52_BODY in markdown
    assert markdown.rstrip().endswith("□")
