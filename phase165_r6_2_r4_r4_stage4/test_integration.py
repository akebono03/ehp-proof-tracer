from dataclasses import dataclass
from types import SimpleNamespace

from expression import MapSymbol
from map_property_rules import ImageWholeStatement, KernelZeroStatement, ImageZeroStatement, KernelWholeStatement
from phase165_r6_2_r4_r4_stage4_binding import build_exactness_binding_provider, verified_exactness_from_bridge
from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
from proof import ExactnessStatement, ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class Assertion:
    origin: object
    content: object


class Registry:
    def __init__(self, assertions):
        self.assertions = assertions

    def assertion(self, key):
        return self.assertions[key]


def fixture_bridge():
    f, g = MapSymbol('f'), MapSymbol('g')
    fact = ExactnessStatement(first_map=f, second_map=g, is_exact=True)
    step = ProofStep(conclusion=fact, premises=(), rule=ProofRule.GIVEN)
    bridge = SimpleNamespace(registry=Registry({'cited': Assertion(AssertionOrigin.FIXED_STATEMENT, fact)}),
                             proof_links=(SimpleNamespace(assertion_id='cited', step=step),))
    return bridge, f, g, fact


def test_zero_kernel_binds_predecessor():
    bridge, f, g, fact = fixture_bridge()
    result = build_exactness_binding_provider(bridge)(KernelZeroStatement(map=g))
    assert len(result) == 1
    assert result[0].subgoals == (fact, ImageZeroStatement(map=f))


def test_whole_image_binds_successor():
    bridge, f, g, fact = fixture_bridge()
    result = build_exactness_binding_provider(bridge)(ImageWholeStatement(map=f))
    assert len(result) == 1
    assert result[0].subgoals == (fact, KernelWholeStatement(map=g))


def test_no_match_does_not_guess():
    bridge, f, g, fact = fixture_bridge()
    assert build_exactness_binding_provider(bridge)(KernelZeroStatement(MapSymbol('h'))) == ()


def test_unverified_source_is_not_used():
    bridge, f, g, fact = fixture_bridge()
    bridge.registry.assertions['cited'] = Assertion(AssertionOrigin.PROOF_INTERNAL, fact)
    assert verified_exactness_from_bridge(bridge) == ()
    assert build_exactness_binding_provider(bridge)(KernelZeroStatement(g)) == ()


def test_r26_alone_cannot_guess_predecessor():
    bridge, f, g, fact = fixture_bridge()
    assert build_generic_backward_expansion_provider((
        __import__('map_property_rules').exactness_and_zero_image_implies_zero_kernel_inference_rule(),
    ))(KernelZeroStatement(g)) == ()


def test_forward_rule_accepts_bound_proposals():
    from proof import find_inference_match, apply_inference_match
    bridge, f, g, fact = fixture_bridge()
    proposal = build_exactness_binding_provider(bridge)(KernelZeroStatement(g))[0]
    steps = tuple(ProofStep(conclusion=x, premises=(), rule=ProofRule.GIVEN) for x in proposal.subgoals)
    match = find_inference_match(proposal.rule, steps)
    assert match is not None
    assert apply_inference_match(match).conclusion == KernelZeroStatement(g)
