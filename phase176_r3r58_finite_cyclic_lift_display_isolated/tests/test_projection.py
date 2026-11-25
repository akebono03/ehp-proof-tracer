"""Test the actual trusted complete proof and fail-closed display guards."""
from dataclasses import replace

import pytest

from phase175_r3r11_cited_hopf_narrative.projection import _rendered_sentence
from phase176_r3r54_narrative_audit.audit import snapshot
from phase176_r3r57_composite_hopf_display_isolated.audit import capture
from phase176_r3r58_finite_cyclic_lift_display_isolated.projection import match_lift, project_finite_cyclic_lift


@pytest.fixture(scope='module')
def verified():
    from unittest.mock import patch
    from phase176_r3r58_finite_cyclic_lift_display_isolated import projection
    with patch.object(projection, 'project_finite_cyclic_lift',
                      lambda markdown, model: (markdown, {})):
        return capture()


def test_real_lift_uses_five_actual_premises(verified):
    _, (_, model, markdown), _ = verified
    before = snapshot(model)
    steps, indices, visible_image, source_number = match_lift(model)
    assert indices == (7,9,10,13,59,60,61)
    assert visible_image is model.steps[58]
    assert source_number == 3
    assert all(a is b for a,b in zip(steps[:5], steps[5].premises))
    projected, plan = project_finite_cyclic_lift(markdown, model)
    assert plan['subgroup_order'] == 2
    assert plan['codomain_order'] == 8 and plan['kernel_multiple'] == 4
    assert len(plan['added_sentences']) == 3
    assert all(projected.count(s) == 1 for s in plan['added_sentences'])
    assert projected.split('\n証明\n',1)[0] == markdown.split('\n証明\n',1)[0]
    assert projected.count('以上より, '+_rendered_sentence(steps[-1])) == 1
    assert snapshot(model) == before
    assert project_finite_cyclic_lift(projected, model) == (projected,{})


def test_partial_missing_source_and_wrong_root_refuse(verified):
    _, (_, model, markdown), (_, partial_model, partial) = verified
    assert project_finite_cyclic_lift(partial, partial_model) == (partial,{})
    for invalid in (replace(model, citations=()), replace(model, root_index=59),
                    replace(model, root_index=None)):
        assert project_finite_cyclic_lift(markdown, invalid) == (markdown,{})


def test_missing_duplicate_or_interrupted_anchors_refuse(verified):
    _, (_, model, markdown), _ = verified
    steps, _, visible, _ = match_lift(model)
    witness = _rendered_sentence(visible)
    root = '以上より, '+_rendered_sentence(steps[-1])
    for altered in (markdown.replace(witness,'unmatched image'),
                    markdown.replace(witness,witness+'\n\n'+witness),
                    markdown.replace(root,'other proof statement\n\n'+root),
                    markdown.replace(root,'unmatched root')):
        assert altered != markdown
        assert project_finite_cyclic_lift(altered,model) == (altered,{})


def test_wrong_typed_premise_is_not_accepted(verified):
    _, (_,model,markdown),_ = verified
    steps, indices, _, _ = match_lift(model)
    # Construct a damaged display model only; never pass it to search or trust.
    lift = replace(steps[5], premises=(steps[1], steps[0], *steps[2:5]))
    root = replace(steps[6],premises=(lift,))
    changed = list(model.steps)
    changed[indices[5]],changed[indices[6]] = lift,root
    invalid = replace(model,steps=tuple(changed))
    assert project_finite_cyclic_lift(markdown,invalid) == (markdown,{})
