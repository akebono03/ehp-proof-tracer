from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r12_r21_eta_generator_chain import (
    expand_cited_eta_generator, proof_has_cited_eta_general_ancestor,
)
from toda_rules import toda_eta_family_definition_statement


def _goals(n):
    source = toda_eta_family_definition_statement(n - 1).element
    target = toda_eta_family_definition_statement(n).element
    mapping = TodaSuspensionMap(TodaPrimaryGroup(n, n - 1), TodaPrimaryGroup(n + 1, n))
    return GeneratorSuspension(mapping, source, target), GeneratorImage(mapping, source, target)


def test_eta_suspension_is_general_for_multiple_indices():
    for n in (3, 4, 8):
        suspension, image = _goals(n)
        proposals = expand_cited_eta_generator(suspension)
        assert len(proposals) == 1
        assert tuple(x.index for x in proposals[0].subgoals) == (n - 1, n)
        assert len(expand_cited_eta_generator(image)) == 1


def test_malformed_suspension_is_not_a_proof_candidate():
    suspension, image = _goals(3)
    altered = GeneratorSuspension(suspension.map, image.target_generator, image.source_generator)
    assert expand_cited_eta_generator(altered) == ()


def test_missing_cited_proof_does_not_certify():
    from proof import ProofStep, ProofRule
    suspension, image = _goals(3)
    fake = ProofStep(image, (), ProofRule.GIVEN)
    assert not proof_has_cited_eta_general_ancestor(fake)
