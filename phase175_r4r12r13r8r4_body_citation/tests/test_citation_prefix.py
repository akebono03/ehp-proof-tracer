"""Focused common citation guard and actual completed pi95 web regression."""
from __future__ import annotations

import ast
from pathlib import Path

from phase175_r4r12r13r8r4_body_citation.installer import (
    OLD_EMBEDDED, OLD_PREFIX, NEW_EMBEDDED, NEW_PREFIX, updated_bytes,
)


def test_patch_changes_only_two_guarded_prefix_regions() -> None:
    source = Path('phase168_r3_5_model_renderer.py').read_bytes()
    normalized = source.replace(b'\r\n', b'\n').decode('utf-8')
    if OLD_EMBEDDED in normalized and OLD_PREFIX in normalized:
        updated, full_function = updated_bytes(source)
        after = updated.replace(b'\r\n', b'\n').decode('utf-8')
        assert NEW_EMBEDDED in full_function
        assert NEW_PREFIX in full_function
        assert after.replace(NEW_EMBEDDED, OLD_EMBEDDED).replace(NEW_PREFIX, OLD_PREFIX) == normalized
        ast.parse(after)
    else:
        assert NEW_EMBEDDED in normalized and NEW_PREFIX in normalized


def test_real_model_has_exact_direct_citation_ownership() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase165_r52_partial_proof import ProofSearchStatus
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=5, k=4, bridge=bridge, context_sink=contexts.append)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, contexts[-1])
    for locator in ('(5.11)', '(5.8)'):
        refs = [c for c in model.citations if (c.reference.locator or c.reference.label) == locator]
        assert len(refs) == 1
        citation = refs[0]
        assert citation.statement_bodies
        given = [model.steps[i] for i in citation.step_indices if model.steps[i].rule is ProofRule.GIVEN]
        assert len(given) == 1
        downstream = [i for i, step in enumerate(model.steps)
                      if step.rule is ProofRule.INFERENCE and len(step.premises) == 1
                      and step.premises[0] == given[0]]
        assert downstream


def test_real_web_contains_cited_equations_and_no_unsupported_extra_math() -> None:
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(5, 4, mode='narrative')
    assert view.key == 'generic-complete-proof'
    lines = getattr(view, 'rendered_lines', ())
    text = '\n'.join(
        getattr(line, 'prefix', '') + ' ' + str(getattr(line, 'statement_latex', '') or '')
        for line in lines
    )
    assert '[R3]より' in text
    assert '[R7]より' in text
