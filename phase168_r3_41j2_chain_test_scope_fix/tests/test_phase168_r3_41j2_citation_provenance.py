"""R3-41J limited proof-linked citation tests; no fixed group prose added."""
import re

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_26_exactness_projection import project_exactness_chains
from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r12_r21_eta_generator_chain import _eta_pair
from proof import ProofRule
from phase168_r3_38_frozen_fulltext_audit.audit import sections


@pytest.fixture(scope='module')
def cases():
    bridge = build_shared_typed_bridge()
    results = {}
    for key, n, k, count in (('pi3_2', 2, 1, 18), ('pi4_3', 3, 1, 25), ('pi5_4', 4, 1, 10)):
        # The public Web route builds the citation model from the context
        # screened for this search, not from the unscreened input registry.
        search_contexts = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=search_contexts.append,
        )
        assert result.status is ProofSearchStatus.COMPLETE
        assert search_contexts
        model_bridge = search_contexts[-1]
        model = build_linked_proof_narrative_model(result, model_bridge)
        assert len(model.steps) == count
        results[key] = (result, model, render_model_backed_narrative_markdown(result, model))
    return results


def _reference_number(model, expected_text):
    references = [cite.number for cite in model.citations
                  if expected_text in (cite.reference.locator or cite.reference.label)]
    assert len(references) == 1
    return references[0]


def _has_typed_source_ancestor(step, statement_type):
    pending = [step]
    visited = set()
    while pending:
        candidate = pending.pop()
        if id(candidate) in visited:
            continue
        visited.add(id(candidate))
        if candidate.rule is ProofRule.GIVEN and isinstance(candidate.conclusion, statement_type):
            return True
        pending.extend(candidate.premises)
    return False


@pytest.mark.parametrize('name', ['pi3_2', 'pi4_3'])
def test_exactness_chain_cites_only_proved_prop42_ancestor(cases, name):
    result, model, markdown = cases[name]
    cited = _reference_number(model, 'Proposition 4.2')
    chains = project_exactness_chains(model)
    assert len(chains) == 1
    assert any(_has_typed_source_ancestor(model.steps[i], TodaProp42GeneralExactnessStatement)
               for i in chains[0].step_indices)
    assert f'[R{cited}]を用いて次の完全列を考える.' in markdown
    assert markdown.count('完全列を考える.') == 1


@pytest.mark.parametrize('name,source,target', [
    ('pi4_3', 2, 3),
    ('pi5_4', 3, 4),
])
def test_eta_suspension_cites_only_proved_eta_definition_ancestor(cases, name, source, target):
    result, model, markdown = cases[name]
    cited = _reference_number(model, 'eta-family notation')
    eta_witnesses = [step for step in model.steps
                     if isinstance(step.conclusion, GeneratorSuspension)
                     and _eta_pair(step.conclusion) is not None]
    assert eta_witnesses
    assert any(_has_typed_source_ancestor(step, TodaEtaFamilyGeneralDefinition)
               for step in eta_witnesses)
    expected = f'[R{cited}]より, $E(\\eta_{{{source}}})=\\eta_{{{target}}}$.'
    assert expected in markdown


@pytest.mark.parametrize('name', ['pi3_2', 'pi4_3', 'pi5_4'])
def test_every_reference_has_a_proved_proof_body_use(cases, name):
    result, model, markdown = cases[name]
    reference, proof = sections(markdown)
    expected = {citation.number for citation in model.citations}
    assert set(int(x) for x in re.findall(r'\[R(\d+)\]', proof)) == expected
    assert all(citation.statement_bodies for citation in model.citations)
    assert proof.rstrip().endswith('□')
    assert '未解決 Goal' not in proof


def test_pi54_specialization_remains_typed_and_ordered(cases):
    result, model, markdown = cases['pi5_4']
    _, proof = sections(markdown)
    assert proof.index(r'\pi_{4}^{3} = \mathbb{Z}/2') < proof.index('(n,m,k)=(3,4,1)')
    assert proof.index('(n,m,k)=(3,4,1)') < proof.index(r'E(\eta_{3})=\eta_{4}')
    assert proof.rstrip().endswith('□')


def test_reference_delta_and_merged_proof_delta_are_distinct_sections(cases):
    result, model, markdown = cases['pi3_2']
    reference, proof = sections(markdown)
    assert r"\xrightarrow{\Delta}" in reference
    assert proof.count(r"\xrightarrow{\Delta}") == 1
    assert proof.count("次の完全列を考える") == 1
