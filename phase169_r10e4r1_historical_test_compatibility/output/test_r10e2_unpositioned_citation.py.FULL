"""R10E2: unpositioned goal uses only screened positioned source assertions."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import (
    FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree, verify_proof_tree_for_narrative,
)
from phase169_r10e1_general_group_transport.transport import (
    expand_prior_general_group_transport,
)
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
    uniquely_screened_prior_sources,
)
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def _element(family_id: int, n: int) -> HomotopyElement:
    family = next(x for x in read_registered_stable_families()
                  if x.family_id == family_id)
    return HomotopyElement(
        name=family.name_at(n),
        dimension=n, source=n + family.stem, target=n,
        generator=GeneratorSymbol(family=family.symbol_family, index=n),
    )


def _relation(family_id: int, n: int, order: int) -> Relation:
    family = next(x for x in read_registered_stable_families()
                  if x.family_id == family_id)
    return Relation(
        TodaPrimaryGroup(n + family.stem, n),
        FiniteCyclicGroup(order, _element(family_id, n)),
        RelationType.EQUALITY,
    )


def _bridge(*statements, positioned=True, extra_links=()) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    links = list(extra_links)
    for i, content in enumerate(statements):
        ref_id = f"r10e2:source:{i}"
        assertion_id = f"r10e2:assertion:{i}"
        registry.add_reference(LiteratureEntry(
            ref_id, ReferenceKind.PROPOSITION, "Proposition test " + str(i),
            publication_position=(8400 + i * 100) if positioned else None,
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id, ref_id, AssertionKind.STATEMENT, content,
            AssertionOrigin.FIXED_STATEMENT, component_position=100,
        ))
        if i == 0 and extra_links:
            continue
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            content, (), ProofRule.GIVEN,
        )))
    return RegistryBridgeResult(registry, (), tuple(links))


def _iso(n: int, k: int, r: int):
    return Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
        exponent=r,
        source_group=TodaPrimaryGroup(n + k, n),
        target_group=TodaPrimaryGroup(n + k + r, n + r),
    ))


def test_r10e2_positioned_sigma_source_generates_unpositioned_candidate():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source), goal=goal,
    )
    assert len(screened.proof_links) == 1
    assert uniquely_screened_prior_sources(screened, goal=goal, source_n=9) == (source,)
    options = expand_prior_general_group_transport(
        goal, (_iso(9, 7, 3),), screened, proof_target=goal,
    )
    # The registry family metadata supplies types only; the suspension image
    # is still a separate Goal and requires independent proof.
    assert len(options) == 1
    assert options[0].subgoals[0] == source
    assert options[0].subgoals[1] == _iso(9, 7, 3)
    assert len(options[0].subgoals) == 5
    assert all(type(step).__name__ != 'ProofStep' for step in options[0].subgoals)


def test_r10e2_unpositioned_target_is_not_inserted_as_given():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source, goal), goal=goal,
    )
    assert len(screened.proof_links) == 1
    assert screened.proof_links[0].step.conclusion == source


def test_r10e2_missing_publication_position_is_not_a_proof_source():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source, positioned=False), goal=goal,
    )
    assert screened.proof_links == ()
    assert uniquely_screened_prior_sources(screened, goal=goal, source_n=9) == ()
    assert expand_prior_general_group_transport(
        goal, (_iso(9, 7, 3),), screened, proof_target=goal,
    ) == ()


def test_r10e2_inconsistent_given_is_rejected():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    forged = ProofStep(goal, (), ProofRule.GIVEN)
    bridge = _bridge(source, extra_links=(ProofStepLink(
        'r10e2:assertion:0', step=forged,
    ),))
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    assert screened.proof_links == ()


def test_r10e2_competing_source_structures_fail_closed():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    other = replace(source, rhs=FiniteCyclicGroup(8, source.rhs.generator))
    # Different presentations cannot be selected by ordering the candidates.
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source, other), goal=goal,
    )
    assert uniquely_screened_prior_sources(screened, goal=goal, source_n=9) == (source,)
    # Only the 16-torsion source fits this target. Two genuinely matching
    # different source structures will be refused as ambiguous.
    assert len(screened.proof_links) == 2


def test_r10e2_zero_groups_need_no_generator_image():
    source = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 8))
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source), goal=goal,
    )
    options = expand_prior_general_group_transport(
        goal, (_iso(6, 4, 2),), screened, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals == (source, _iso(6, 4, 2))


def test_r10e2_no_unpositioned_root_given_can_pass_verifier():
    from phase165_r52_partial_proof import (
        ProofSearchStatus, GroupStructureStatus, make_partial_proof_result,
    )
    goal = _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(goal), goal=goal,
    )
    direct = ProofStep(goal, (), ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=12, k=7, structure_status=GroupStructureStatus.UNKNOWN,
        status=ProofSearchStatus.COMPLETE,
        proven_steps=(direct,), conclusion=goal,
    )
    with pytest.raises(UnverifiedProofTree):
        verify_proof_tree_for_narrative(
            result, screened, citing_assertion_id=None,
            derived_target_without_citing_id=True,
        )


def test_r10e2_positioned_existing_citation_api_is_unchanged():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    bridge = _bridge(source)
    from phase165_r52_partial_proof import (
        ProofSearchStatus, make_partial_proof_result,
    )
    result = make_partial_proof_result(
        n=12, k=7, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(goal,),
        diagnostics=("purposefully unresolved test goal",),
    )
    with pytest.raises(ValueError, match='positioned goal'):
        verify_proof_tree_for_narrative(
            result, bridge, citing_assertion_id=None,
        )


def test_r10e2_guarded_patch_refuses_double_application():
    from phase169_r10e2_unpositioned_citation.patch import transform
    target = 'phase169_r10e1_general_group_transport/transport.py'
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    before = root / "phase169_r10e2_unpositioned_citation" / "output" / (
        target.replace("/", "__") + ".before"
    )
    original = before.read_bytes()
    updated, functions = transform(target, original)
    assert 'uniquely_screened_prior_sources' in functions[
        'expand_prior_general_group_transport'
    ]
    # Later phases may append new transport policy to the same function.
    # Verify the R10E2 source-first guard survives without requiring the
    # entire production file to equal the old R10E2 snapshot.
    current = (root / target).read_bytes()
    assert b"uniquely_screened_prior_sources" in updated
    assert b"uniquely_screened_prior_sources" in current
    assert b"exact_prior_database_result" in current
    with pytest.raises(RuntimeError, match='expected changed source'):
        transform(target, updated)


def test_r10e2r1_renderer_keeps_frozen_reference_locator():
    from pathlib import Path

    renderer = (Path(__file__).resolve().parents[2]
                / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8")
    assert 'locator = citation.reference.locator or citation.reference.label' in renderer
    assert 'locator = "η 系列の定義（Chapter V, i）"' not in renderer
