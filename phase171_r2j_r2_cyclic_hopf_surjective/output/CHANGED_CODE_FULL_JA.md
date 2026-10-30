# Phase 171 R2J-R2 変更コード全文

## 変更対象

- 既存ファイル `phase165_r52_r9_shared_math.py`
- 関数 `shared_expansion_provider`（全体を以下に提示）
- 追加位置：R2I `expand_cited_eta_hopf_power` の直後
- 新規 `phase171_r2j_r2_cyclic_hopf_surjective/source.py`（全文）
- 新規 `audit.py`（全文）と `tests/test_cited_cyclic_hopf.py`（全文）
- 既存ファイルのトップレベル import 変更なし

## 既存ファイル import 全文（モジュールドキュメントも含む）

```python
"""Shared Phase 165 typed backward-search path. Never replay saved proofs.

Typed source claims may be reused across goals; a source's role as a leaf
is not a license to use an untyped archive or an earlier derived proof.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage, MapIsomorphism, expand_generic_iso_goal
from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
from phase165_r14_r11_delta_zero import expand_delta_zero_from_suspension_iso
from phase165_r14_r14_diagonal_and_prop42 import expand_diagonal_suspension
from phase165_r14_r33_final_group import reverse_free_cyclic_transport_rule
from phase165_r3_recursive_search import GoalExpansion
from phase165_r6_2_unified_registry_r3_r4.context_provider_registry import build_context_expansion_provider_registry
from phase165_r6_2_unified_registry_r3_r3.provider_registry import build_shared_expansion_provider_registry
from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import build_unified_backward_rule_registry
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import (
    AssertionOrigin, UnifiedStatementRegistry,
)


```

## `shared_expansion_provider` 関数全文

```python
def shared_expansion_provider(bridge: RegistryBridgeResult, extra_providers: tuple = (), *, proof_target=None, prior_conclusions: tuple = ()):
    """Build backward proposals from typed source witnesses and common rules."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    # R4-4 stage4: exactness-map binding from cited fixed statements only.
    from phase165_r6_2_r4_r4_stage4_binding import build_exactness_binding_provider
    from phase165_r12_r11_prop42_unified import build_prop42_specialization_provider
    from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences
    from phase165_r12_r13_kernel_image import build_concrete_kernel_provider
    from phase165_r12_r26_map_candidates import build_cited_eta_quotient_provider
    extra_providers = (build_cited_eta_quotient_provider(bridge),) + tuple(extra_providers)
    from phase165_r12_r28_presentation_connection import expand_eta_presentation
    extra_providers = (expand_eta_presentation,) + tuple(extra_providers)
    from phase165_r12_r29_kernel_connection import expand_kernel_multiple_from_suspension
    extra_providers = (expand_kernel_multiple_from_suspension,) + tuple(extra_providers)
    from phase165_r12_r30_ehp_surjectivity import expand_ehp_whole_image
    extra_providers = (expand_ehp_whole_image,) + tuple(extra_providers)
    from phase165_r12_r31_proven_cyclic_reuse import expand_free_cyclic_structure_from_relation
    extra_providers = (expand_free_cyclic_structure_from_relation,) + tuple(extra_providers)
    extra_providers = (build_concrete_kernel_provider(bridge),) + tuple(extra_providers)
    extra_providers = (build_exactness_binding_provider(bridge), build_prop42_specialization_provider(bridge), expand_ehp_exactness_consequences) + tuple(extra_providers)
    # Phase 169 R3E: connect the pre-existing typed EHP goal expansions.
    # These propose subgoals only; no completed map property or proof leaf is inserted.
    from phase165_r14_r5_ehp_connection import (
        expand_registered_ehp_goal, expand_registered_ehp_terminal_goal,
        expand_cited_ehp_terminal_goal,
    )
    extra_providers = (expand_registered_ehp_goal,) + tuple(extra_providers)
    available = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT:
            available.append(link.step.conclusion)

    from phase165_r12_r15_toda51 import expand_cited_toda51_zero
    from phase165_r12_r24_web_search_connection import expand_finite_cyclic_relation
    from phase165_r12_r20_eta_definition import expand_cited_eta_definition
    from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
    from phase169_r10d2_general_family_definition.family_citation import (
        expand_cited_stable_family,
    )
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")

    from phase165_r57_r7_stable_expansion import (
        expand_registered_toda45_finite_cyclic_goal,
    )
    from phase165_r57_r8_eta_specialization import (
        expand_registered_eta_specialization,
    )

    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
    from phase165_r57_r19_delta_image_backward import expand_registered_delta_image_goal
    from phase165_r57_r20_general_specialization import expand_cited_general_specialization
    from phase165_r57_r26_generic_search_connection import (
        build_generic_backward_expansion_provider,
        merge_backward_expansions,
    )

    unified_registry, _unified_report = build_unified_backward_rule_registry()
    unified_rules = unified_registry.rules()
    generic_provider = build_generic_backward_expansion_provider(unified_rules)

    # R6-2 R4: cited source anchors bind otherwise unknown premise variables.
    from phase165_r6_2_r4_seeded_goals import generate_seeded_backward_goals
    seeded_rules = unified_rules
    seeded_steps = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content
    )

    # R6-2 R3: use only cited GIVEN witnesses for verified inverse proposals.
    from phase165_r6_2_r2_verified_inverse import reverse_rules_from_witnesses
    witness_rules = unified_rules
    cited_witnesses = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content
    )

    shared_provider_registry = build_shared_expansion_provider_registry(
        expand_generic_iso_goal=expand_generic_iso_goal,
        expand_generic_ehp_hopf_goal=expand_generic_ehp_hopf_goal,
        expand_delta_zero_from_suspension_iso=expand_delta_zero_from_suspension_iso,
        expand_diagonal_suspension=expand_diagonal_suspension,
        extra_providers=extra_providers,
    )

    context_provider_registry = build_context_expansion_provider_registry(
        available=tuple(available),
        prior_conclusions=prior_conclusions,
        expand_registered_toda45_finite_cyclic_goal=expand_registered_toda45_finite_cyclic_goal,
        expand_registered_eta_specialization=expand_registered_eta_specialization,
        expand_registered_delta_image_goal=expand_registered_delta_image_goal,
        expand_cited_general_specialization=expand_cited_general_specialization,
    )

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        # R10ET-R5: use the single, replayable Definition for every eligible
        # typed stable GeneratorImage, regardless of the generator's label.
        from phase169_r10eq_r1_universal_stable_definition.definition import (
            expand_defined_stable_element_image,
        )
        defined_options = expand_defined_stable_element_image(goal)
        if defined_options:
            return defined_options
        options = []
        from phase166_r3q_hopf_image_relation import expand_hopf_image_relation
        options.extend(expand_hopf_image_relation(goal, tuple(available)))
        from phase171_r2h_prop22_cited_hopf.source import (
            expand_cited_prop22_right_formula,
        )
        options.extend(expand_cited_prop22_right_formula(goal, tuple(available)))
        from phase171_r2i_eta_hopf_bridge.source import (
            expand_cited_eta_hopf_power,
        )
        options.extend(expand_cited_eta_hopf_power(goal, tuple(available)))
        from phase171_r2j_r2_cyclic_hopf_surjective.source import (
            expand_cited_cyclic_hopf_surjectivity,
        )
        options.extend(expand_cited_cyclic_hopf_surjectivity(
            goal, tuple(available), proof_target=proof_target,
        ))
        options.extend(expand_finite_cyclic_relation(goal))
        from phase169_r3o_stable_composite_rule import (
            expand_cited_toda45_composite_transport,
        )
        options.extend(expand_cited_toda45_composite_transport(
            goal, tuple(available),
        ))
        from phase169_r5b_pi75_prior_transport.rule import (
            expand_prior_cited_toda45_composite_transport,
        )
        legacy_one_step_options = expand_prior_cited_toda45_composite_transport(
            goal, tuple(available), bridge, proof_target=proof_target,
        )
        options.extend(legacy_one_step_options)
        from phase169_r6a_pi86_two_step_transport.rule import (
            expand_prior_two_step_eta_square_transport,
        )
        legacy_two_step_options = expand_prior_two_step_eta_square_transport(
            goal, tuple(available), bridge, proof_target=proof_target,
        )
        options.extend(legacy_two_step_options)
        # R10E1: one typed entry for zero, cyclic, free and direct-sum groups.
        # Previously verified finite-cyclic derivations retain their R7 adapter.
        # Neither DB results nor candidate generators become GIVEN proof leaves.
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from phase169_r10e1_general_group_transport.transport import (
            expand_prior_general_group_transport,
        )
        if (not legacy_one_step_options and not legacy_two_step_options
                and ((isinstance(goal, Relation)
                      and isinstance(goal.lhs, TodaPrimaryGroup)
                      and type(goal.lhs.group_dimension) is int
                      and type(goal.lhs.sphere_dimension) is int)
                     or isinstance(goal, TodaPrimaryGroupZeroStatement))):
            options.extend(expand_prior_general_group_transport(
                goal, tuple(available), bridge, proof_target=proof_target,
            ))
        options.extend(expand_registered_ehp_terminal_goal(goal, tuple(available)))
        # R3I: earlier cited GIVEN sources are valid inference premises.
        # Retain the historical inference-only proposal independently.
        options.extend(expand_cited_ehp_terminal_goal(goal, tuple(available)))
        from phase168_r2_toda52_transport import expand_toda52_finite_cyclic_goal
        options.extend(expand_toda52_finite_cyclic_goal(goal, tuple(available)))
        options.extend(expand_cited_toda51_zero(goal, tuple(available)))
        options.extend(expand_cited_eta_definition(goal, tuple(available)))
        eta_generator_options = expand_cited_eta_generator(goal)
        options.extend(eta_generator_options)
        cited_stable_options = expand_cited_stable_family(
            goal, tuple(available),
        )
        options.extend(cited_stable_options)
        composite_image_options = ()
        if not eta_generator_options:
            from phase169_r10e5_composite_generator_image.rule import (
                expand_composite_generator_image,
            )
            composite_image_options = expand_composite_generator_image(goal)
            options.extend(composite_image_options)
        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
        options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))
        from phase169_r4c_pi64_suspension_iso.rule import expand_pi64_suspension_isomorphism
        options.extend(expand_pi64_suspension_isomorphism(goal))
        from phase166_r3ac_stable_notation import expand_stable_eta_notation
        options.extend(expand_stable_eta_notation(goal, tuple(available)))
        from phase166_r3v_generator_transport import expand_generator_transport_normalization
        options.extend(expand_generator_transport_normalization(goal, tuple(available)))
        if (isinstance(goal, Relation)
                and goal.relation_type is RelationType.EQUALITY
                and isinstance(goal.rhs, FreeCyclicGroup)
                and isinstance(goal.lhs, TodaPrimaryGroup)):
            for image in available:
                if not isinstance(image, GeneratorImage):
                    continue
                if (getattr(image.map, "source_group", None) != goal.lhs
                        or image.source_generator != goal.rhs.generator):
                    continue
                options.append(GoalExpansion(
                    reverse_free_cyclic_transport_rule(),
                    (MapIsomorphism(image.map),
                     Relation(image.map.target_group,
                              FreeCyclicGroup(image.target_generator)),
                     image),
                ))
        for provider in context_provider_registry.providers():
            new = provider(goal)
            if not isinstance(new, tuple) or not all(isinstance(x, GoalExpansion) for x in new):
                raise TypeError("expansion provider contract violated")
            options.extend(new)
        for provider in shared_provider_registry.providers():
            new = provider(goal)
            if not isinstance(new, tuple) or not all(isinstance(x, GoalExpansion) for x in new):
                raise TypeError("expansion provider contract violated")
            options.extend(new)
        # R2 returns candidate Goals only; the recursive search still verifies ProofSteps.
        # Exhaustion is not equivalent to proof; preserve the older search proposals.
        try:
            witness_options = reverse_rules_from_witnesses(
                goal, witness_rules, cited_witnesses, max_combinations=2048,
            )
        except ValueError as exc:
            if str(exc) != "generic witness inverse search budget exceeded":
                raise
            witness_options = ()
        merged = merge_backward_expansions(
            merge_backward_expansions(tuple(options), generic_provider(goal)),
            witness_options,
        )
        try:
            seeded_options = generate_seeded_backward_goals(
                goal, seeded_rules, seeded_steps, max_candidates=2048,
            )
        except ValueError as exc:
            if str(exc) != "seeded backward search budget exceeded":
                raise
            seeded_options = ()
        merged = merge_backward_expansions(merged, seeded_options)
        return retain_ordered_root_expansions(proof_target, goal, merged)
    return expand
```

## 新規 source.py 全文

```python
"""Source-bound cyclic-generator surjectivity, without recycled complete proofs.

The printed group theorem is specialized as an INFERENCE from a screened
fixed general statement.  H(x)=g is separately reconstructed from its own
cited premises; neither is admitted as a new GIVEN.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, IteratedSuspension, MapApplication, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from phase171_r2i_eta_hopf_bridge.source import eligible_eta_hopf_chains
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


def _coordinates(value: object) -> tuple[int, int] | None:
    """Return (source, target) of a well-typed concrete homotopy element."""
    if isinstance(value, HomotopyElement):
        s, t = value.source, value.target
        if (type(s) is int and type(t) is int
                and type(value.dimension) is int
                and value.dimension == t and s >= t >= 2):
            return s, t
        return None
    if isinstance(value, Composition):
        left = _coordinates(value.left)
        right = _coordinates(value.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    if isinstance(value, Suspension):
        inner = _coordinates(value.expression)
        return None if inner is None else (inner[0] + 1, inner[1] + 1)
    if isinstance(value, IteratedSuspension):
        inner = _coordinates(value.expression)
        k = value.exponent
        return (inner[0] + k, inner[1] + k) if inner is not None and type(k) is int and k >= 0 else None
    return None


def _same_generator(left: object, right: object, order: int) -> bool:
    """Use exact typed equality or the pre-existing, ID-checked name alias."""
    if left == right:
        return True
    if type(order) is not int or order <= 1:
        return False
    return same_registered_group_presentation(
        FiniteCyclicGroup(order, left), FiniteCyclicGroup(order, right),
    )


def _eligible_group_instance(source: object, group: Relation) -> bool:
    """Recognize one existing positioned higher-stem group theorem.

    The general source provides the mathematics. HyoujiGen supplies only
    the spelling/degree identity of its concrete named generator.
    """
    if (not isinstance(source, Relation)
            or not isinstance(group, Relation)
            or group.relation_type is not RelationType.EQUALITY
            or not isinstance(group.lhs, TodaPrimaryGroup)
            or not isinstance(group.rhs, FiniteCyclicGroup)):
        return False
    n = group.lhs.sphere_dimension
    if type(n) is not int:
        return False
    specialized = specialize_registered_higher_stem(source, n)
    return (specialized is not None
            and specialized == group
            and type(group.rhs.order) is int
            and group.rhs.order > 1)


def cyclic_group_from_cited_general_rule(goal: Relation, source: Relation) -> InferenceRule:
    """Specialize the screened general fixed theorem, never the DB result."""
    if not _eligible_group_instance(source, goal):
        raise ValueError("source does not specialize to this typed cyclic group")

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.GIVEN
                and premises[0].conclusion == source
                and _eligible_group_instance(source, goal))

    return InferenceRule(
        name="specialize earlier cited cyclic group schema",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=Relation,
            relation_type=RelationType.EQUALITY,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def _valid_surjective_pair(
    goal: MapSurjective, group: Relation, image: Relation,
) -> bool:
    """Check the exact H-domain, codomain and generating image."""
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaHopfInvariantMap):
        return False
    mapping = goal.map
    if (not isinstance(mapping.source_group, TodaPrimaryGroup)
            or not isinstance(mapping.target_group, TodaPrimaryGroup)
            or not isinstance(group, Relation)
            or group.relation_type is not RelationType.EQUALITY
            or group.lhs != mapping.target_group
            or not isinstance(group.rhs, FiniteCyclicGroup)
            or type(group.rhs.order) is not int or group.rhs.order <= 1
            or not isinstance(image, Relation)
            or image.relation_type is not RelationType.EQUALITY
            or not isinstance(image.lhs, MapApplication)
            or image.lhs.map != EHP_H_MAP):
        return False
    src = _coordinates(image.lhs.expression)
    dst = _coordinates(image.rhs)
    generator = _coordinates(group.rhs.generator)
    if src is None or dst is None or generator is None:
        return False
    q, n = src
    if (q < n or mapping.source_group != TodaPrimaryGroup(q, n)
            or mapping.target_group != TodaPrimaryGroup(q, 2 * n - 1)
            or dst != (q, 2 * n - 1)
            or generator != dst):
        return False
    return _same_generator(group.rhs.generator, image.rhs, group.rhs.order)


def cyclic_generator_image_surjectivity_rule(
    goal: MapSurjective, group: Relation, image: Relation,
) -> InferenceRule:
    """A homomorphism hitting a certified cyclic generator is surjective."""
    if not _valid_surjective_pair(goal, group, image):
        raise ValueError("cyclic group and Hopf generator image do not match")

    def guard(premises, bindings):
        return (len(premises) == 2
                and all(step.rule is ProofRule.INFERENCE for step in premises)
                and premises[0].conclusion == group
                and premises[1].conclusion == image
                and _valid_surjective_pair(goal, group, image))

    return InferenceRule(
        name="cyclic codomain generator in image implies Hopf surjectivity",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation,
                           relation_type=RelationType.EQUALITY),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation,
                           relation_type=RelationType.EQUALITY),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_cyclic_hopf_surjectivity(
    goal: object, available: tuple[object, ...], *, proof_target: object = None,
) -> tuple[GoalExpansion, ...]:
    """Propose only backed-up group specializations and R2I Hopf chains.

    Do not duplicate the group root's independent existing proof search.
    In subgoals of another proof, the specialized group schema remains a
    separate inference obligation; it is never inserted as a GIVEN.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    sources = tuple(value for value in available if isinstance(value, Relation))
    if isinstance(goal, Relation):
        if proof_target is None or goal == proof_target:
            return ()
        proposals = []
        for source in sources:
            if _eligible_group_instance(source, goal):
                proposals.append(GoalExpansion(
                    cyclic_group_from_cited_general_rule(goal, source),
                    (source,),
                ))
        return tuple(proposals)
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaHopfInvariantMap):
        return ()
    proposals = []
    for chain in eligible_eta_hopf_chains(available):
        for source in sources:
            target = goal.map.target_group
            if not isinstance(target, TodaPrimaryGroup):
                continue
            n = target.sphere_dimension
            if type(n) is not int:
                continue
            group = specialize_registered_higher_stem(source, n)
            if group is None or not _valid_surjective_pair(goal, group, chain.conclusion):
                continue
            candidate = GoalExpansion(
                cyclic_generator_image_surjectivity_rule(goal, group, chain.conclusion),
                (group, chain.conclusion),
            )
            if not any(x.subgoals == candidate.subgoals for x in proposals):
                proposals.append(candidate)
    return tuple(proposals)

```

## 新規 audit.py 全文

```python
"""R2J-R2: prove H surjective from a cited cyclic group generator image.

R2I is reconstructed inside this proof, not imported as a completed proof
or inserted as a leaf. This audit does not assert Delta=0 or pi_6^3.
"""
from __future__ import annotations

import json
from pathlib import Path

from expression import Composition, MapApplication
from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import expand_cited_eta_definition
from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase166_r3c_publication_order import precedes_citing_assertion
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from phase171_r2h_prop22_cited_hopf.source import expand_cited_prop22_right_formula
from phase171_r2i_eta_hopf_bridge.audit import _available, _checked_chain, _screened_context
from phase171_r2i_eta_hopf_bridge.source import expand_cited_eta_hopf_power
from phase171_r2j_r2_cyclic_hopf_surjective.source import (
    _valid_surjective_pair,
    expand_cited_cyclic_hopf_surjectivity,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin

OUTPUT = Path(__file__).resolve().parent / "output"
SOURCE = Path(__file__).resolve().parent.parent / "sources" / "toda" / "Toda_05_2.tex"


def _verify_adopted_prop53_text() -> None:
    """Check the reviewed transcription; do not claim original-edition verification."""
    text = SOURCE.read_text(encoding="utf-8-sig")
    begin = text.find(r"\begin{proposition}\label{prop:5.3}")
    end = text.find(r"\end{proposition}", begin)
    if begin < 0 or end <= begin:
        raise RuntimeError("adopted Proposition 5.3 source block missing")
    clause = text[begin:end]
    if any(piece not in clause for piece in (
        r"\pi^{n}_{n+2}", r"\eta_n^{2}", r"\mathbb Z_2", r"n\ge2",
    )):
        raise RuntimeError("adopted Proposition 5.3 theorem text is incomplete")


def _scoped_provider(available: tuple[object, ...], goal: MapSurjective):
    """Exact known obligations; no historical completed-proof import."""
    def expand(current: object):
        return (
            expand_cited_cyclic_hopf_surjectivity(
                current, available, proof_target=goal,
            )
            + expand_cited_eta_hopf_power(current, available)
            + expand_cited_prop22_right_formula(current, available)
            + expand_cited_eta_definition(current, available)
            + expand_cited_eta_generator(current)
        )
    return expand


def build_cited_r2j_r2_proof():
    """Reconstruct the proof tree from four screened, earlier cited leaves."""
    _verify_adopted_prop53_text()
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    hopf = TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    )
    goal = MapSurjective(hopf)
    expected_image = chain.conclusion
    if (expected_image.lhs != MapApplication(
            EHP_H_MAP, Composition(chain.alpha, chain.eta_next),
        ) or not isinstance(expected_image.rhs, Composition)):
        raise RuntimeError("R2I Hopf image has the wrong type")
    proposals = expand_cited_cyclic_hopf_surjectivity(
        goal, available, proof_target=group_goal,
    )
    if len(proposals) != 1 or proposals[0].subgoals[1] != expected_image:
        raise RuntimeError("generator-in-image proposal not uniquely screened")
    prior_group = proposals[0].subgoals[0]
    if not _valid_surjective_pair(goal, prior_group, expected_image):
        raise RuntimeError("cyclic generator/element identity mismatch")
    source_links = []
    for link in screened.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        if not isinstance(link.step.conclusion, Relation):
            continue
        specialized = specialize_registered_higher_stem(
            link.step.conclusion, 5,
        )
        if specialized != prior_group:
            continue
        assertion = screened.registry.assertion(link.assertion_id)
        ref = screened.registry.reference(assertion.reference_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or ref.locator != "Proposition 5.3"
                or not precedes_citing_assertion(
                    screened, link.assertion_id, citing,
                )):
            raise RuntimeError("Proposition 5.3 is not an earlier fixed source")
        source_links.append(link)
    if len(source_links) != 1:
        raise RuntimeError("exactly one screened Proposition 5.3 source required")
    public_options = shared_expansion_provider(
        screened, proof_target=group_goal,
    )(goal)
    if not any(
        option.subgoals == proposals[0].subgoals
        and option.rule.name == proposals[0].rule.name
        for option in public_options
    ):
        raise RuntimeError("R2J rule not connected to shared provider")
    proof = reconstruct_registered_goal(
        goal, screened, citing, _scoped_provider(available, goal),
        lookup_mode="typed_reference_publication",
    )
    if (proof.rule is not ProofRule.INFERENCE
            or proof.conclusion != goal
            or len(proof.premises) != 2
            or any(p.rule is not ProofRule.INFERENCE for p in proof.premises)
            or proof.premises[0].conclusion != prior_group
            or proof.premises[1].conclusion != expected_image):
        raise RuntimeError("H surjectivity was not reconstructed from two inferences")
    nodes = []
    seen = set()

    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        nodes.append(step)
        for parent in step.premises:
            visit(parent)

    visit(proof)
    leaves = [step for step in nodes if step.rule is ProofRule.GIVEN]
    sources = tuple(link.step.conclusion for link in screened.proof_links
                    if link.step is not None and link.step.rule is ProofRule.GIVEN)
    if (len(leaves) != 4
            or any(leaf.premises for leaf in leaves)
            or any(leaf.conclusion not in sources for leaf in leaves)
            or sum(leaf.conclusion == source_links[0].step.conclusion
                   for leaf in leaves) != 1):
        raise RuntimeError("unexpected or fabricated GIVEN in H surjectivity proof")
    if any(step.conclusion == group_goal for step in nodes):
        raise RuntimeError("pi_6^3 group structure improperly inserted")
    if any(step.rule is ProofRule.GIVEN
           and step.conclusion in (prior_group, expected_image, goal)
           for step in nodes):
        raise RuntimeError("derived group/Hopf/map fact promoted to GIVEN")
    return proof, prior_group, chain, tuple(nodes), source_links[0]


def run() -> None:
    proof, group, chain, nodes, link = build_cited_r2j_r2_proof()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {
        "result": "PASS_CITED_H_SURJECTIVE_ONLY",
        "hopf_map": repr(proof.conclusion.map),
        "group": repr(group),
        "r2i_image": repr(chain.conclusion),
        "prop53_assertion_id": link.assertion_id,
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in nodes),
        "given_leaves": sum(step.rule is ProofRule.GIVEN for step in nodes),
        "given_conclusions": [repr(step.conclusion) for step in nodes
                              if step.rule is ProofRule.GIVEN],
        "delta_zero_proven": False,
        "pi63_proven": False,
        "adopted_prop53_text_matched": True,
        "original_edition_verified": False,
        "registration_status_not_upgraded": True,
        "full_pytest": False,
    }
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R2_PROP53_SPECIALIZATION=PASS", flush=True)
    print("PHASE171_R2J_R2_R2I_INFERRED_ANCESTRY=PASS", flush=True)
    print("PHASE171_R2J_R2_CYCLIC_GENERATOR_IN_IMAGE=PASS", flush=True)
    print("PHASE171_R2J_R2_H_SURJECTIVE=PASS", flush=True)
    print("PHASE171_R2J_R2_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R2_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R2_DELTA_ZERO_PROVEN=False", flush=True)
    print("PHASE171_R2J_R2_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R2_RESULT=PASS_CITED_H_SURJECTIVE_ONLY", flush=True)
    print("PHASE171_R2J_R2_REPORT=" + str(OUTPUT / "audit.json"), flush=True)


if __name__ == "__main__":
    run()

```

## 新規テスト全文

```python
"""R2J-R2 regression: valid cited derivation and rejected counterfeit premises."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import MapSurjective
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase171_r2i_eta_hopf_bridge.audit import _available, _checked_chain, _screened_context
from phase171_r2j_r2_cyclic_hopf_surjective.audit import build_cited_r2j_r2_proof
from phase171_r2j_r2_cyclic_hopf_surjective.source import (
    _coordinates,
    _eligible_group_instance,
    _valid_surjective_pair,
    cyclic_generator_image_surjectivity_rule,
    cyclic_group_from_cited_general_rule,
    expand_cited_cyclic_hopf_surjectivity,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _case():
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    goal = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))
    return chain, available, group_goal, goal


def test_cited_proof_of_h_surjectivity_contains_both_inferred_premises():
    proof, group, chain, nodes, source_link = build_cited_r2j_r2_proof()
    assert proof.rule is ProofRule.INFERENCE
    assert len(proof.premises) == 2
    assert all(step.rule is ProofRule.INFERENCE for step in proof.premises)
    assert proof.premises[0].conclusion == group
    assert proof.premises[1].conclusion == chain.conclusion
    assert sum(step.rule is ProofRule.GIVEN for step in nodes) == 4
    assert sum(step.conclusion == source_link.step.conclusion
               for step in nodes if step.rule is ProofRule.GIVEN) == 1


def test_cyclic_group_specialization_requires_screened_general_statement():
    chain, available, root, goal = _case()
    offered = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)
    assert len(offered) == 1
    group = offered[0].subgoals[0]
    assert _valid_surjective_pair(goal, group, chain.conclusion)
    group_options = expand_cited_cyclic_hopf_surjectivity(group, available, proof_target=root)
    assert len(group_options) == 1
    assert group_options[0].subgoals[0] in available
    assert _eligible_group_instance(group_options[0].subgoals[0], group)
    assert expand_cited_cyclic_hopf_surjectivity(group, available, proof_target=group) == ()
    assert expand_cited_cyclic_hopf_surjectivity(goal, (), proof_target=root) == ()


def test_rejects_wrong_hopf_degree_and_wrong_generator():
    chain, available, root, goal = _case()
    group = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)[0].subgoals[0]
    bad_map = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 6),
    ))
    assert not _valid_surjective_pair(bad_map, group, chain.conclusion)
    assert expand_cited_cyclic_hopf_surjectivity(bad_map, available, proof_target=root) == ()
    unrelated = HomotopyElement(
        "η₇", 7, source=8, target=7, generator=GeneratorSymbol("η", index=7),
    )
    bad_group = replace(group, rhs=FiniteCyclicGroup(2, unrelated))
    assert not _valid_surjective_pair(goal, bad_group, chain.conclusion)
    assert _coordinates(Composition(chain.alpha, chain.eta_next)) == (7, 3)
    assert _coordinates(Composition(chain.beta, chain.eta_next)) == (7, 5)


def test_rejects_forged_given_group_or_hopf_result():
    chain, available, root, goal = _case()
    group = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)[0].subgoals[0]
    rule = cyclic_generator_image_surjectivity_rule(goal, group, chain.conclusion)
    forged_group = ProofStep(group, (), ProofRule.GIVEN)
    forged_image = ProofStep(chain.conclusion, (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (forged_group, forged_image)) == ()
    source = expand_cited_cyclic_hopf_surjectivity(group, available, proof_target=root)[0].subgoals[0]
    group_rule = cyclic_group_from_cited_general_rule(group, source)
    assert find_inference_matches_for_rule(
        group_rule, (ProofStep(source, (), ProofRule.INFERENCE),)
    ) == ()


def test_cited_generator_alias_is_typed_not_textual():
    chain, available, root, goal = _case()
    group = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)[0].subgoals[0]
    assert group.rhs.generator != chain.conclusion.rhs or _valid_surjective_pair(
        goal, group, chain.conclusion,
    )
    assert same_registered_group_presentation(
        FiniteCyclicGroup(2, group.rhs.generator),
        FiniteCyclicGroup(2, chain.conclusion.rhs),
    )
    wrong = replace(chain.eta_next, source=80)
    false_image = Relation(
        MapApplication(EHP_H_MAP, Composition(chain.alpha, wrong)),
        chain.conclusion.rhs, RelationType.EQUALITY,
    )
    assert not _valid_surjective_pair(goal, group, false_image)


def test_without_cited_prop53_or_r2i_sources_cannot_propose_surjectivity():
    chain, available, root, goal = _case()
    offered = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)
    assert len(offered) == 1
    group_source = expand_cited_cyclic_hopf_surjectivity(
        offered[0].subgoals[0], available, proof_target=root,
    )[0].subgoals[0]
    without_prop53 = tuple(item for item in available if item != group_source)
    assert expand_cited_cyclic_hopf_surjectivity(goal, without_prop53, proof_target=root) == ()
    hopf_source = Relation(MapApplication(EHP_H_MAP, chain.alpha), chain.beta, RelationType.EQUALITY)
    without_hopf = tuple(item for item in available if item != hopf_source)
    assert expand_cited_cyclic_hopf_surjectivity(goal, without_hopf, proof_target=root) == ()

```
