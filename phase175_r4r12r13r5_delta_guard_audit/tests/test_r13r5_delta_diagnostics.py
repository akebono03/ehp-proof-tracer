"""No proof may follow from candidate existence or a fabricated generator match."""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import delta_injective_inputs
from phase175_r4r12r13r3_public_delta_e_bridge.provider import delta_free_coordinate_proposals
from proof import Relation, RelationType


def matching_target():
    signed = canonical_toda58()
    return Relation(
        signed.map.target_group,
        DirectSumGroup((
            FreeCyclicGroup(signed.positive_value.left.expression),
            FiniteCyclicGroup(4, signed.positive_value.right.expression),
        )),
        RelationType.EQUALITY,
    )


def test_r13r5_matching_typed_generators_enable_only_a_candidate():
    signed = canonical_toda58()
    goal = MapInjective(signed.map)
    source = Relation(signed.map.source_group, FreeCyclicGroup(signed.element), RelationType.EQUALITY)
    assert delta_injective_inputs(goal, source, matching_target(), signed) is not None
    assert len(delta_free_coordinate_proposals(
        goal, cited58=True, database_lookup=lambda n, k: matching_target() if (n, k) == (4, 3) else None,
    )) == 1


def test_r13r5_missing_citation_does_not_emit_delta_candidate():
    signed = canonical_toda58()
    assert not delta_free_coordinate_proposals(
        MapInjective(signed.map), cited58=False,
        database_lookup=lambda n, k: matching_target(),
    )


def test_r13r5_unmatched_torsion_generator_is_rejected():
    signed = canonical_toda58()
    bad_target = Relation(
        signed.map.target_group,
        DirectSumGroup((FreeCyclicGroup(signed.positive_value.left.expression),
                        FiniteCyclicGroup(4, signed.element))),
        RelationType.EQUALITY,
    )
    source = Relation(signed.map.source_group, FreeCyclicGroup(signed.element), RelationType.EQUALITY)
    assert delta_injective_inputs(MapInjective(signed.map), source, bad_target, signed) is None
