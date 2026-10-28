"""R10ER: retain cited image ancestry and accept replayed Definition images."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import (
    resolve_specialized_goal_citing_id,
)
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from phase169_r10eq_r1_universal_stable_definition.definition import (
    expand_defined_stable_element_image,
)
from proof import ProofRule


@pytest.fixture(scope="module")
def cases():
    bridge = build_shared_typed_bridge()
    results = {}
    for n, k in ((30, 14), (30, 16), (30, 9)):
        contexts = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        assert result.status is ProofSearchStatus.COMPLETE
        assert not result.open_goals and len(contexts) == 1
        citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        verify_proof_tree_for_narrative(
            result, contexts[0], citing_assertion_id=citing,
            derived_target_without_citing_id=citing is None,
        )
        model = build_linked_proof_narrative_model(result, contexts[0])
        order = tuple(row.step_index for row in project_narrative_order(model))
        results[(n, k)] = (result, model, order)
    return results


@pytest.mark.parametrize(
    ("stem", "exponent", "formulae", "definition_steps"),
    (
        (14, 14, (
            r"E^{14}(\sigma_{16}^{2})=\sigma_{30}^{2}",
            r"E^{14}(\kappa_{16})=\kappa_{30}",
        ), 14),
        (16, 12, (
            r"E^{12}(\omega_{18})=\omega_{30}",
            r"E^{12}(\sigma_{18}\mu_{25})=\sigma_{30}\mu_{37}",
        ), 12),
    ),
)
def test_r10er_mixed_direct_sum_has_two_compressed_images(
    cases, stem, exponent, formulae, definition_steps,
):
    result, model, order = cases[(30, stem)]
    display = project_verified_direct_sum_transport(model, order)
    assert display is not None
    assert display.root_index == model.root_index
    assert all(formula in display.statement for formula in formulae)
    assert "Definition" in display.statement
    assert display.citation_numbers == ()
    assert len(display.hidden_indices) >= 2 * exponent
    step_ids_before = tuple(id(step) for step in model.steps)
    citations_before = model.step_citation_numbers
    markdown = render_model_backed_narrative_markdown(result, model)
    assert display.statement in markdown
    assert all(markdown.count(formula) == 1 for formula in formulae)
    assert count_rendered_image_equations(markdown)["total_occurrences"] == 0
    assert tuple(id(step) for step in model.steps) == step_ids_before
    assert model.step_citation_numbers == citations_before
    assert markdown.rstrip().endswith("□")
    definitions = tuple(
        step for step in model.steps
        if step.rule is ProofRule.INFERENCE
        and not step.premises
        and len(expand_defined_stable_element_image(step.conclusion)) == 1
    )
    assert len(definitions) >= definition_steps


def test_r10er_common_definition_replaces_cited_prefix(cases):
    result, model, order = cases[(30, 9)]
    display = project_verified_direct_sum_transport(model, order)
    assert display is not None
    assert display.citation_numbers == ()
    assert display.statement.startswith("Definition より, ")
    locators = tuple(item.reference.locator or item.reference.label
                     for item in model.citations)
    assert len(locators) == 2
    assert any("DB prior:" in locator for locator in locators)
    assert "(4.5)" in locators
    assert display.statement in render_model_backed_narrative_markdown(result, model)


def test_r10er_missing_registered_provenance_still_rejected(cases):
    _, model, order = cases[(30, 14)]
    uncited = replace(
        model,
        step_citation_numbers=tuple(() for _ in model.steps),
        citations=(),
    )
    assert project_verified_direct_sum_transport(uncited, order) is None
    assert project_verified_direct_sum_transport(
        replace(model, root_index=None), order,
    ) is None


def test_r10er_full_function_export_and_exact_source_guard():
    from pathlib import Path

    from phase169_r10er_r1_mixed_definition_projection.patch import (
        HERE, GIT_BLOB_SHA1, git_blob_hash, replacement_content,
    )
    original = (HERE / "projection_reference.py").read_bytes()
    modified, full_function = replacement_content(original)
    assert git_blob_hash(original) == GIT_BLOB_SHA1
    assert modified == (HERE / "full_files" / "projection.py").read_bytes()
    assert full_function == (
        HERE / "full_functions" / "project_verified_direct_sum_transport.py"
    ).read_text(encoding="utf-8")
    assert b"def project_verified_direct_sum_transport(" in modified
    with pytest.raises(RuntimeError, match="SHA1 differs"):
        replacement_content(b"wrong source")
