"""Real verified narrative fixture and fail-closed projection guards."""
from dataclasses import replace

import pytest

from phase176_r3r57_composite_hopf_display_isolated.audit import capture
from phase176_r3r57_composite_hopf_display_isolated.projection import project_composite_hopf_chain


@pytest.fixture(scope='module')
def verified():
    return capture()


def test_real_chain_and_idempotence(verified):
    _, (_, model, markdown), _ = verified
    shadow, plan = project_composite_hopf_chain(markdown, model)
    assert plan['chain_indices'] == list(range(14,26))
    assert plan['summary'] in shadow
    assert plan['retained_witness'] in shadow
    assert project_composite_hopf_chain(shadow, model) == (shadow,{})


def test_partial_missing_source_and_missing_anchor(verified):
    _, (_, model, markdown), (_, partial_model, partial) = verified
    assert project_composite_hopf_chain(partial, partial_model) == (partial,{})
    missing = replace(model, citations=tuple(replace(c, assertion_ids=()) for c in model.citations))
    assert project_composite_hopf_chain(markdown, missing) == (markdown,{})
    _, plan = project_composite_hopf_chain(markdown, model)
    broken = markdown.replace(plan['retained_witness'], 'unmatched witness')
    assert project_composite_hopf_chain(broken, model) == (broken,{})


def test_ambiguous_or_interrupted_display(verified):
    _, (_, model, markdown), _ = verified
    _, plan = project_composite_hopf_chain(markdown, model)
    witness = plan['retained_witness']
    for changed in (markdown.replace(witness, witness+'\n\n'+witness),
                    markdown.replace(witness, witness+'\n\nOther proof statement.')):
        assert project_composite_hopf_chain(changed, model) == (changed,{})
