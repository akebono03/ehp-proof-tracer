"""Public R21 wiring preserves existing priorities and screened provenance."""
from dataclasses import replace
from unittest.mock import patch

import pytest

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, admitted_prior_group_step
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from phase178_r16_toda513_isolated.source import canonical_513
from phase178_r21_finite_cyclic_generator_zero_image_isolated import rule
from phase178_r21r1_finite_cyclic_generator_zero_image_public import installer
from proof import ProofStep, ProofRule, apply_inference_match, find_inference_matches_for_rule
from toda_rules import TodaDeltaZeroStatement


def signature(options):
    return tuple((o.rule.name,o.subgoals) for o in options)


@pytest.fixture(scope='module')
def context():
    root = exact_prior_database_result(6,6)
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root)
    image = canonical_513()[1]
    return root,bridge,TodaDeltaZeroStatement(image.map),image


def test_public_append_only_and_replay(context):
    root,bridge,goal,image = context
    before = tuple(bridge.proof_links),tuple(bridge.registry._assertions.items())
    public = shared_expansion_provider(bridge,proof_target=root)
    extra = signature(rule.build_finite_cyclic_delta_zero_provider(bridge=bridge,proof_target=root)(goal))
    assert extra
    with patch.object(rule,'build_finite_cyclic_delta_zero_provider',return_value=lambda g: ()):
        baseline = signature(public(goal))
        unchanged = tuple(signature(public(g)) for g in (root,image))
    actual = public(goal)
    assert signature(actual)==baseline+tuple(s for s in extra if s not in baseline)
    assert tuple(signature(public(g)) for g in (root,image))==unchanged
    prior = admitted_prior_group_step(goal.map.source_group,proof_target=root,bridge=bridge)
    assert prior is not None
    cited = linked_cited_steps(bridge,image)
    assert cited
    option, = [o for o in actual if o.rule.name==rule.RULE_NAME and o.subgoals==(prior.conclusion,image)]
    assert all(not isinstance(g,ProofStep) for g in option.subgoals)
    match, = find_inference_matches_for_rule(option.rule,(prior,cited[0]))
    result = apply_inference_match(match)
    assert result.conclusion==goal and result.rule is ProofRule.INFERENCE
    assert result.premises==(prior,cited[0])
    assert not find_inference_matches_for_rule(option.rule,(prior,ProofStep(image,(),ProofRule.GIVEN)))
    assert before==(tuple(bridge.proof_links),tuple(bridge.registry._assertions.items()))
    assert not any(link.step is not None and link.step.conclusion==root for link in bridge.proof_links)


def test_missing_screened_image_and_rootless_context(context):
    root,bridge,goal,image = context
    missing = replace(bridge,proof_links=tuple(link for link in bridge.proof_links
                      if link.step is None or link.step.conclusion!=image))
    assert all(o.rule.name!=rule.RULE_NAME for o in shared_expansion_provider(missing,proof_target=root)(goal))
    with patch.object(rule,'build_finite_cyclic_delta_zero_provider',side_effect=AssertionError('rootless call')):
        assert all(o.rule.name!=rule.RULE_NAME for o in shared_expansion_provider(bridge)(goal))


def test_patch_contract():
    from phase178_r20r1_suspension_isomorphism_bridge_public import installer as previous
    from phase178_r1_k6_source_first_audit import audit as r1
    for path,writer in ((installer.TARGET,installer.proposed_source),(installer.OLD_TEST,installer.proposed_test)):
        original = previous.normalized(r1.git('show',installer.HEAD+':'+path))
        assert previous.normalized((installer.ROOT/path).read_bytes())==writer(original)
        with pytest.raises(RuntimeError):
            writer('')
