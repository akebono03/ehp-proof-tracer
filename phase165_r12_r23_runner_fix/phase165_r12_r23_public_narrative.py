"""R12-R23: read-only verified quotient proof to common public Narrative."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from expression import Multiple
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap, FiniteCyclicGroup
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r14_kernel_closure import prove_kernel_in_screened_context
from phase165_r12_r15_toda51 import prove_surjectivity_in_screened_context
from phase165_r12_r16_bridges import (
    concrete_cyclic_kernel_as_multiple_rule, derive_from_certified_proof,
    suspension_surjectivity_as_generic_surjectivity_rule,
)
from phase165_r12_r18_evidence_reuse import extract_completed_root
from phase165_r12_r19_generator_connection import expand_generator_presentation
from phase165_r12_r21_eta_generator_chain import proof_has_cited_eta_general_ancestor
from phase165_r12_r22_quotient_closure import close_quotient_from_verified_steps, proof_ancestors
from phase165_r12_r2_quotient_rules import HomomorphismPresentationStatement
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result, render_partial_proof_markdown
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider
from proof import ProofRule, ProofStep, Relation, RelationType
from toda_rules import toda_eta_family_definition_statement


@dataclass(frozen=True)
class NarrativeAuditResult:
    root: ProofStep
    markdown: str
    sources: tuple[str, ...]
    node_count: int


def proof_nodes(root: ProofStep) -> tuple[ProofStep, ...]:
    """Traverse the actual proof DAG, no synthetic leaves."""
    nodes = []
    visited = set()

    def visit(step):
        if id(step) in visited:
            return
        visited.add(id(step))
        for p in step.premises:
            visit(p)
        nodes.append(step)

    visit(root)
    return tuple(nodes)


def fixed_reference_locators(root: ProofStep) -> tuple[str, ...]:
    result = []
    for step in proof_nodes(root):
        if step.rule is not ProofRule.GIVEN:
            continue
        rule = getattr(step, 'inference_rule', None)
        reference = getattr(rule, 'literature_reference', None)
        locator = getattr(reference, 'locator', None)
        if isinstance(locator, str) and locator and locator not in result:
            result.append(locator)
    return tuple(result)


def build_verified_pi43_narrative() -> NarrativeAuditResult:
    """Recreate R22 closure from verified typed proofs, not a known result fixture."""
    import importlib.util
    source_audit = Path(__file__).resolve().parent / 'phase165_r12_r22_quotient_closure' / 'audit.py'
    if not source_audit.is_file():
        raise ValueError('R12-R22 audit script is unavailable')
    spec = importlib.util.spec_from_file_location('phase165_r12_r22_runtime_audit', source_audit)
    if spec is None or spec.loader is None:
        raise ValueError('R12-R22 audit loader unavailable')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    certificate = module.perform_audit()
    if certificate.get('pi43_proof_certified') is not True:
        raise ValueError('R12-R22 certificate did not succeed: ' + str(certificate.get('blocker')))

    source = TodaPrimaryGroup(3, 2)
    target = TodaPrimaryGroup(4, 3)
    mapping = TodaSuspensionMap(source, target)
    eta2 = toda_eta_family_definition_statement(2).element
    eta3 = toda_eta_family_definition_statement(3).element
    bridge = build_shared_typed_bridge()
    citing = next(iter(bridge.registry._assertions))
    scope = Relation(target, object(), relation_type=RelationType.EQUALITY)
    goal = Relation(target, FiniteCyclicGroup(2, eta3), relation_type=RelationType.EQUALITY)

    prior = search_shared_group_goal(n=2, k=1, group_structure=FreeCyclicGroup(eta2), bridge=bridge)
    source_result = extract_completed_root(prior, Relation(source, FreeCyclicGroup(eta2)))
    if source_result.proof is None:
        raise ValueError('pi32 source proof missing')
    source_root = source_result.proof

    kernel = prove_kernel_in_screened_context(
        SuspensionKernelFreeCyclicStatement(mapping, FreeCyclicGroup(Multiple(2, eta2))),
        bridge, citing_assertion_id=citing, proof_target=scope,
    )
    if kernel.status != 'CERTIFIED' or kernel.proof is None:
        raise ValueError('certified kernel proof missing')
    kstep = derive_from_certified_proof(concrete_cyclic_kernel_as_multiple_rule(), kernel.proof)

    onto = prove_surjectivity_in_screened_context(
        MapSurjective(mapping), bridge, citing_assertion_id=citing, proof_target=scope,
    )
    if onto.status != 'CERTIFIED' or onto.proof is None:
        raise ValueError('certified surjectivity proof missing')
    sstep = derive_from_certified_proof(suspension_surjectivity_as_generic_surjectivity_rule(), onto.proof)

    pgoal = HomomorphismPresentationStatement(mapping, source, target, eta2, eta3)
    provider = shared_expansion_provider(bridge, extra_providers=(expand_generator_presentation,))
    pstep = reconstruct_registered_goal(
        pgoal, bridge, citing_assertion_id=citing,
        expansion_provider=provider, lookup_mode='typed_reference',
    )
    if pstep.conclusion != pgoal or not proof_has_cited_eta_general_ancestor(pstep):
        raise ValueError('certified eta presentation proof missing')

    closure = close_quotient_from_verified_steps(pstep, kstep, sstep, source_root)
    root = closure.proof
    if root is None or root.conclusion != goal or root.rule is not ProofRule.INFERENCE:
        raise ValueError('final quotient inference unresolved')
    if not proof_ancestors(root, (pstep, kernel.proof, onto.proof, source_root)):
        raise ValueError('quotient ancestry is incomplete')

    nodes = proof_nodes(root)
    sources = fixed_reference_locators(root)
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(root,), conclusion=goal, references=sources,
    )
    markdown = render_partial_proof_markdown(result)
    if not isinstance(markdown, str) or not markdown.strip():
        raise ValueError('renderer returned empty narrative')
    return NarrativeAuditResult(root=root, markdown=markdown, sources=sources, node_count=len(nodes))
