"""Actual accepted proof and fail-closed display contracts."""
from dataclasses import replace

import pytest

from phase176_r3r54_narrative_audit.audit import snapshot
from phase176_r3r57_composite_hopf_display_isolated.audit import capture
from phase176_r3r60r1_citation_premise_elision_isolated.projection import (
    parse_display, project_citation_premise_elision, rewrite_display,
)


@pytest.fixture(scope='module')
def verified():
    return capture()


def test_real_elision_keeps_model_and_renumbers_display(verified):
    _,(_,model,markdown),_ = verified
    snap = snapshot(model)
    output,plan = project_citation_premise_elision(markdown,model)
    assert (plan['zero_base_index'],plan['zero_consumer_index'],plan['quadruple_index']) == (2,3,56)
    assert plan['removed_reference'] == 9
    assert plan['display_number_map'] == {**{i:i for i in range(1,9)},10:9}
    assert len(plan['removed_sentences']) == 1 and len(plan['replacements']) == 2
    assert '**[R9] (5.5).**' in output and '[R10]' not in output
    assert 'Chapter V, iii)' not in output
    assert r'[R9]より, $4\nu_{5} = \eta_{5}^{3}$.' in output
    assert r"[R2]より, $E(\eta_{2}\nu'\eta_{6})=0$." in output
    assert all(s not in output.split('\n証明\n',1)[1] for s in plan['removed_sentences'])
    assert snapshot(model) == snap and len(model.citations) == 10
    assert project_citation_premise_elision(output,model) == (output,{})


def test_partial_missing_and_unrooted_models_refuse(verified):
    _,(_,model,markdown),(_,partial_model,partial) = verified
    assert project_citation_premise_elision(partial,partial_model) == (partial,{})
    for invalid in (replace(model,citations=()),replace(model,root_index=None),
                    replace(model,citations=tuple(c for c in model.citations if c.number != 9))):
        assert project_citation_premise_elision(markdown,invalid) == (markdown,{})


def test_missing_duplicate_or_interrupted_body_refuses(verified):
    _,(_,model,markdown),_ = verified
    _,plan = project_citation_premise_elision(markdown,model)
    for sentence in plan['removed_sentences']+list(plan['replacements']):
        for invalid in (markdown.replace(sentence,'unmatched body',1),
                        markdown.replace(sentence,sentence+'\n\n'+sentence,1)):
            assert invalid != markdown
            assert project_citation_premise_elision(invalid,model) == (invalid,{})
    sentence = plan['removed_sentences'][0]
    invalid = markdown.replace(sentence,sentence+'\n\nOther proof sentence.',1)
    assert project_citation_premise_elision(invalid,model) == (invalid,{})


def test_extra_definition_use_and_unknown_reference_content_refuse(verified):
    _,(_,model,markdown),_ = verified
    _,plan = project_citation_premise_elision(markdown,model)
    for invalid in (markdown.replace('証明\n','証明\n\n[R9]より, another statement.\n',1),
                    markdown.replace('**[R9] Chapter V, iii).**','**[R9] Chapter V, iii).**\n\nOther cited assertion.',1)):
        assert invalid != markdown
        assert project_citation_premise_elision(invalid,model) == (invalid,{})
    nums = list(model.step_citation_numbers)
    nums[54] = (9,)
    assert project_citation_premise_elision(markdown,replace(model,step_citation_numbers=tuple(nums))) == (markdown,{})


def test_display_mapping_is_simultaneous_and_only_drops_authorized_block():
    md = '使用する結果\n\n**[R1] A.**\n\n$a_2=0$.\n\n**[R2] B.**\n\n$b=0$.\n\n**[R3] C.**\n\n$c=0$.\n\n**[R4] D.**\n\n$d=0$.\n\n証明\n\n[R1]より, $a=0$.\n\n[R2], [R3]を用いて, $c=0$.\n\n[R4]より, $d=0$.\n\n□\n'
    before = '[R2], [R3]を用いて, $c=0$.'
    output,mapping = rewrite_display(md,[],{before:'[R3]より, $c=0$.'},2)
    assert mapping == {1:1,3:2,4:3}
    assert '**[R2] C.**' in output and '**[R3] D.**' in output
    assert '[R2]より, $c=0$.' in output and '[R3]より, $d=0$.' in output
    assert '$a_2=0$.' in output and '**[R2] B.**' not in output
    assert parse_display(output) is not None
    assert rewrite_display(md,[],{before:'[R2]より, $c=0$.'},2) is None
    assert rewrite_display(md,[],{before:'[R3]より, $c=0$.'},1) is None
    assert parse_display(md.replace('**[R3] C.**','**[R2] C.**')) is None
