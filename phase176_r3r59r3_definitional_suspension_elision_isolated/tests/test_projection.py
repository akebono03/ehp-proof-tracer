"""Real accepted proof fixture and negative display-only tests."""
from dataclasses import replace

import pytest

from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase176_r3r54_narrative_audit.audit import snapshot
from phase176_r3r57_composite_hopf_display_isolated.audit import capture
from phase176_r3r59r3_definitional_suspension_elision_isolated.projection import (
    alias_branch, project_definitional_suspension_elision, source_prefix,
)


@pytest.fixture(scope='module')
def verified():
    from phase176_r3r59r4_public_definitional_suspension_elision.apply import previous_stage
    with previous_stage():
        return capture()


def test_actual_elision_and_citations(verified):
    _, (_, model, markdown), _ = verified
    before = snapshot(model)
    projected, plan = project_definitional_suspension_elision(markdown, model)
    assert plan['chain_indices'] == list(range(14,26))
    assert plan['witness_indices'] == [29,36,43]
    assert plan['joined_index'] == 52 and plan['alias_index'] == 51
    assert plan['source_index'] == 26 and plan['source_reference'] == 8
    assert plan['quadruple_index'] == 56 and plan['consumer_index'] == 58
    assert len(plan['removed_sentences']) == 2
    assert len(plan['replacements']) == 2
    assert all(s not in projected.split('\n証明\n',1)[1] for s in plan['removed_sentences'])
    assert any(s.startswith('[R6], [R7], [R8]を用いて, ') for s in plan['replacements'].values())
    assert any(s.startswith('[R8], [R9], [R10]を用いて, ') for s in plan['replacements'].values())
    assert projected.split('\n証明\n',1)[0] == markdown.split('\n証明\n',1)[0]
    assert snapshot(model) == before
    assert project_definitional_suspension_elision(projected, model) == (projected,{})


def test_partial_and_missing_source_refuse(verified):
    _, (_, model, markdown), (_, partial_model, partial) = verified
    assert project_definitional_suspension_elision(partial, partial_model) == (partial,{})
    for changed in (replace(model,citations=()), replace(model,root_index=None),
                    replace(model,citations=tuple(c for c in model.citations if c.number != 8))):
        assert project_definitional_suspension_elision(markdown, changed) == (markdown,{})


def test_missing_duplicate_interrupted_anchors_refuse(verified):
    _, (_, model, markdown), _ = verified
    _, plan = project_definitional_suspension_elision(markdown,model)
    for line in plan['removed_sentences'] + list(plan['replacements']):
        for altered in (markdown.replace(line,'unmatched proof sentence',1),
                        markdown.replace(line,line+'\n\n'+line,1),
                        markdown.replace(line,line+'\n\ninterrupted proof sentence',1)):
            assert altered != markdown
            # Inserting after the final retained quadruple anchor is outside
            # the compressed region; test interruption only inside the region.
            if line == list(plan['replacements'])[-1] and 'interrupted proof sentence' in altered:
                continue
            assert project_definitional_suspension_elision(altered,model) == (altered,{})


def test_alias_branch_requires_real_witness_and_transport(verified):
    _, (_, model, _), _ = verified
    scope = root_ancestor_step_indices(model.steps,model.root_index)
    lookup = {id(s):i for i,s in enumerate(model.steps)}
    parents = {i:tuple(lookup[id(p)] for p in model.steps[i].premises) for i in scope}
    nodes, witnesses = alias_branch(model,scope,51,26,parents)
    assert witnesses == {29,36,43}
    assert 51 in nodes and 52 not in nodes
    assert alias_branch(model,scope,51,19,parents) is None
    numbers = list(model.step_citation_numbers)
    numbers[29] = (8,)
    assert alias_branch(replace(model,step_citation_numbers=tuple(numbers)),scope,51,26,parents) is None
    # A display-equivalent identity is not accepted without its actual typed premises.
    changed = list(model.steps)
    changed[33] = replace(changed[33],conclusion=model.steps[40].conclusion)
    assert alias_branch(replace(model,steps=tuple(changed)),scope,51,26,parents) is None


def test_prefix_never_invents_or_drops_existing_citations():
    assert source_prefix('[R6], [R7]を用いて, $x=y$.',{6,7,8}) == '[R6], [R7], [R8]を用いて, $x=y$.'
    assert source_prefix('[R6]より, $x=y$.',{7,8}) is None
    assert source_prefix('$x=y$.',{6}) is None
