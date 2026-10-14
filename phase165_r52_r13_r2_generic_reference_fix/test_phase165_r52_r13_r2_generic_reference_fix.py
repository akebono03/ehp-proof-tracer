"""Regression: explicit composite metadata, arbitrary class names, and narratives."""
from dataclasses import dataclass

from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase165_r52_r13_reference_registration import register_adopted_composite_reference
from phase165_typed_component_lookup import index_typed_components
from proof import ProofRule
from unified_statement_registry import AssertionEntry, AssertionKind, LiteratureEntry, ReferenceKind, UnifiedStatementRegistry


@dataclass(frozen=True)
class PreviouslyUnknownComposite:
    group_claim: int
    delta_claim: str


def test_r13_r2_arbitrary_composite_name_has_searchable_components():
    original = register_adopted_composite_reference(
        assertion_id='generic:prop', locator='Proposition Sample',
        source_id='adopted transcription',
        content=PreviouslyUnknownComposite(23, 'delta fact'),
    )
    fields = index_typed_components(original.registry)
    assert {entry.component_name for entry in fields} == {'group_claim', 'delta_claim'}
    bridge = expand_cited_given_components(original)
    for claim in (23, 'delta fact'):
        proof = reconstruct_registered_goal(
            claim, bridge, 'generic:prop', lambda target: (),
            lookup_mode='typed_reference',
        )
        assert proof.rule is ProofRule.GIVEN
        assert proof.conclusion == claim
        assert proof.inference_rule.literature_reference.locator == 'Proposition Sample'


def test_r13_r2_unannotated_dataclass_stays_atomic():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('ref:a', ReferenceKind.PROPOSITION, 'Proposition A'))
    composite = PreviouslyUnknownComposite(23, 'delta fact')
    registry.add_assertion(AssertionEntry(
        'assertion:a', 'ref:a', AssertionKind.STATEMENT, composite,
    ))
    components = index_typed_components(registry)
    assert len(components) == 1
    assert components[0].component_name == '__self__'
    assert components[0].content == composite


def test_r13_r2_pi32_public_narrative_accepts_registered_given_root():
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(2, 1, 2, 'narrative')
    content = '\n'.join(
        line.prefix + ' ' + ' '.join(piece.value for piece in line.segments)
        for line in view.rendered_lines
    )
    assert '証明対象' in content
    assert '使用する結果' in content
    assert '証明' in content
