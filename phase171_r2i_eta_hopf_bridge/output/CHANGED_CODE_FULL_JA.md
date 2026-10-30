# Phase 171 R2I — 全文コード記録

## 変更対象

- `phase165_r52_r9_shared_math.py` — `shared_expansion_provider` 全体（下記）
- 新規 `phase171_r2i_eta_hopf_bridge/source.py` — 全関数・クラス（下記）
- 新規 `phase171_r2i_eta_hopf_bridge/tests/test_cited_eta_hopf.py` — テスト全文（下記）
- 新規 `phase171_r2i_eta_hopf_bridge/audit.py`、`install.py`、`run.ps1`（ZIP 内の全文）

モジュール先頭の import は変更なし。変更関数内部に R2I の import を追加。
新規ファイルはパッケージの先頭から末尾までが実装全文。

## `shared_expansion_provider` 変更後全文

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

## 新規 `source.py` 全文

```python
"""Compose the cited right-Hopf formula with a proved eta suspension.

Only a source-screened H(alpha)=eta_n and the cited universal eta Definition
can initiate the proof. Every returned object is a backward INFERENCE request;
no relation or group result is registered as GIVEN here.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import Composition, HomotopyElement, MapApplication, Suspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from hopf_rules import ehp_h_preserves_equality_inference_rule
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r12_r28_presentation_connection import _matching_eta_name
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import (
    TodaProp22RightFormula,
    _formula_parts,
)
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from relation_rules import (
    equality_preserved_under_left_composition_inference_rule,
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)
from toda_rules import toda_eta_family_definition_statement


@dataclass(frozen=True)
class EtaHopfChain:
    """Exactly typed goals; a schema, not a source or a proof certificate."""
    alpha: HomotopyElement
    beta: HomotopyElement
    eta_next: HomotopyElement
    generator_suspension: GeneratorSuspension
    eta_forward: Relation
    eta_backward: Relation
    alpha_composition: Relation
    hopf_composition: Relation
    cited_hopf: Relation
    intermediate: Relation
    beta_composition: Relation
    conclusion: Relation


def _eq(lhs: object, rhs: object) -> Relation:
    return Relation(lhs=lhs, rhs=rhs, relation_type=RelationType.EQUALITY)


def _make_chain(hopf: Relation) -> EtaHopfChain | None:
    """Check source, target, eta identity, and the R2H formula's domain."""
    if (not isinstance(hopf, Relation)
            or hopf.relation_type is not RelationType.EQUALITY
            or not isinstance(hopf.lhs, MapApplication)
            or hopf.lhs.map != EHP_H_MAP
            or not isinstance(hopf.lhs.expression, HomotopyElement)
            or not isinstance(hopf.rhs, HomotopyElement)):
        return None
    alpha, beta = hopf.lhs.expression, hopf.rhs
    generator = beta.generator
    if (generator is None or generator.family != "η"
            or generator.decoration is not None
            or type(generator.index) is not int or generator.index < 3):
        return None
    n = generator.index
    older = toda_eta_family_definition_statement(n).element
    newer = toda_eta_family_definition_statement(n + 1).element
    if not _matching_eta_name(beta, older):
        return None
    suspended = Suspension(beta)
    if (not Composition(alpha, suspended).is_type_compatible()
            or not Composition(alpha, newer).is_type_compatible()
            or not Composition(beta, suspended).is_type_compatible()
            or not Composition(beta, newer).is_type_compatible()):
        return None
    cited_hopf = _eq(
        MapApplication(EHP_H_MAP, Composition(alpha, suspended)),
        Composition(beta, suspended),
    )
    formula = _eq(
        cited_hopf.lhs,
        Composition(MapApplication(EHP_H_MAP, alpha), suspended),
    )
    if _formula_parts(formula) is None:
        return None
    witness = GeneratorSuspension(
        TodaSuspensionMap(
            TodaPrimaryGroup(n + 1, n),
            TodaPrimaryGroup(n + 2, n + 1),
        ),
        older,
        newer,
    )
    eta_forward = _eq(suspended, newer)
    eta_backward = _eq(newer, suspended)
    alpha_composition = _eq(
        Composition(alpha, newer), Composition(alpha, suspended),
    )
    hopf_composition = _eq(
        MapApplication(EHP_H_MAP, alpha_composition.lhs),
        MapApplication(EHP_H_MAP, alpha_composition.rhs),
    )
    intermediate = _eq(hopf_composition.lhs, cited_hopf.rhs)
    beta_composition = _eq(
        Composition(beta, suspended), Composition(beta, newer),
    )
    conclusion = _eq(intermediate.lhs, beta_composition.rhs)
    return EtaHopfChain(
        alpha, beta, newer, witness, eta_forward, eta_backward,
        alpha_composition, hopf_composition, cited_hopf, intermediate,
        beta_composition, conclusion,
    )


def eligible_eta_hopf_chains(available: tuple[object, ...]) -> tuple[EtaHopfChain, ...]:
    """Read earlier, screened GIVEN *conclusions* only; never inspect a DB goal."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (available.count(TodaEtaFamilyGeneralDefinition()) != 1
            or available.count(TodaProp22RightFormula()) != 1):
        return ()
    candidates = []
    for item in available:
        if available.count(item) != 1:
            continue
        chain = _make_chain(item)
        if chain is not None:
            candidates.append(chain)
    return tuple(candidates)


def cited_eta_suspension_equality_rule(
    goal: Relation, witness: GeneratorSuspension,
) -> InferenceRule:
    """Turn a DERIVED generator suspension into an equality of elements.

    `_matching_eta_name` handles only the repository's already typed Unicode
    and underscore spellings; the actual suspension assertion must be proved.
    """
    if (not isinstance(witness, GeneratorSuspension)
            or not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, Suspension)
            or not isinstance(goal.lhs.expression, HomotopyElement)
            or not isinstance(goal.rhs, HomotopyElement)):
        raise ValueError("expected a typed eta suspension equality")
    beta = goal.lhs.expression
    n = getattr(getattr(beta, "generator", None), "index", None)
    if type(n) is not int or n < 3:
        raise ValueError("expected a concrete eta-family index")
    from phase165_r12_r21_eta_generator_chain import _eta_pair
    pair = _eta_pair(witness)
    if (pair is None
            or pair[0].index != n
            or pair[1].index != n + 1
            or not _matching_eta_name(beta, pair[0].element)
            or not _matching_eta_name(goal.rhs, pair[1].element)
            or witness.source_generator != pair[0].element
            or witness.target_generator != pair[1].element):
        raise ValueError("generator suspension does not justify this equality")

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.INFERENCE
                and premises[0].conclusion == witness)

    return InferenceRule(
        name="proved consecutive eta suspension yields element equality",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.INFERENCE,
            statement_type=GeneratorSuspension,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_eta_hopf_power(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Backward chain using existing general congruence and equality rules.

    eta_n^2 is represented solely by the exact typed composition
    eta_n o eta_(n+1); its pretty-printed exponent grants no new fact.
    """
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return ()
    proposals = []
    for chain in eligible_eta_hopf_chains(available):
        if goal == chain.eta_forward:
            rule = cited_eta_suspension_equality_rule(goal, chain.generator_suspension)
            subgoals = (chain.generator_suspension,)
        elif goal == chain.eta_backward:
            rule = equality_symmetry_inference_rule()
            subgoals = (chain.eta_forward,)
        elif goal == chain.alpha_composition:
            rule = equality_preserved_under_left_composition_inference_rule(chain.alpha)
            subgoals = (chain.eta_backward,)
        elif goal == chain.hopf_composition:
            rule = ehp_h_preserves_equality_inference_rule()
            subgoals = (chain.alpha_composition,)
        elif goal == chain.intermediate:
            rule = equality_transitivity_inference_rule()
            subgoals = (chain.hopf_composition, chain.cited_hopf)
        elif goal == chain.beta_composition:
            rule = equality_preserved_under_left_composition_inference_rule(chain.beta)
            subgoals = (chain.eta_forward,)
        elif goal == chain.conclusion:
            rule = equality_transitivity_inference_rule()
            subgoals = (chain.intermediate, chain.beta_composition)
        else:
            continue
        if not any(x.subgoals == subgoals and x.rule.name == rule.name for x in proposals):
            proposals.append(GoalExpansion(rule, subgoals))
    return tuple(proposals)

```

## 新規テスト全文

```python
"""R2I: cited Definition, proof ancestry, typed rewriting, and negative cases."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase171_r2i_eta_hopf_bridge.audit import (
    _available,
    _checked_chain,
    _screened_context,
    build_cited_r2i_proof,
)
from phase171_r2i_eta_hopf_bridge.source import (
    _make_chain,
    cited_eta_suspension_equality_rule,
    eligible_eta_hopf_chains,
    expand_cited_eta_hopf_power,
)
from phase169_r10eb_typed_composition_power.display import (
    typed_stable_composition_power_latex,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    find_inference_matches_for_rule,
)


def _case():
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    return chain, available


def test_r2i_cited_proof_tree_without_group_completion():
    proof, chain, ancestry = build_cited_r2i_proof()
    assert proof.conclusion == chain.conclusion
    assert proof.rule is ProofRule.INFERENCE
    assert chain.conclusion.lhs == MapApplication(
        EHP_H_MAP, Composition(chain.alpha, chain.eta_next),
    )
    assert chain.conclusion.rhs == Composition(chain.beta, chain.eta_next)
    assert sum(step.rule is ProofRule.GIVEN for step in ancestry) == 3
    assert sum(step.rule is ProofRule.INFERENCE for step in ancestry) >= 10
    assert all(step.rule is ProofRule.INFERENCE for step in ancestry if step.premises)


def test_r2i_uses_only_screened_both_general_sources():
    chain, available = _case()
    assert eligible_eta_hopf_chains(()) == ()
    without_eta = tuple(x for x in available if not isinstance(x, TodaEtaFamilyGeneralDefinition))
    without_hopf_formula = tuple(x for x in available if not isinstance(x, TodaProp22RightFormula))
    assert expand_cited_eta_hopf_power(chain.conclusion, without_eta) == ()
    assert expand_cited_eta_hopf_power(chain.conclusion, without_hopf_formula) == ()
    assert len(expand_cited_eta_hopf_power(chain.conclusion, available)) == 1


def test_r2i_rejects_wrong_types_and_unrelated_primitive():
    chain, available = _case()
    wrong_beta = replace(chain.beta, source=100)
    wrong_hopf = Relation(
        MapApplication(EHP_H_MAP, chain.alpha),
        wrong_beta,
        RelationType.EQUALITY,
    )
    assert _make_chain(wrong_hopf) is None
    fake = replace(chain.conclusion, rhs=chain.beta)
    assert expand_cited_eta_hopf_power(fake, available) == ()
    assert expand_cited_eta_hopf_power(chain.conclusion, ()) == ()
    with pytest.raises(ValueError):
        cited_eta_suspension_equality_rule(
            Relation(Suspension(wrong_beta), chain.eta_next, RelationType.EQUALITY),
            chain.generator_suspension,
        )


def test_r2i_rejects_fake_given_generator_suspension():
    chain, available = _case()
    rule = cited_eta_suspension_equality_rule(
        chain.eta_forward, chain.generator_suspension,
    )
    forged_leaf = ProofStep(
        conclusion=chain.generator_suspension,
        premises=(),
        rule=ProofRule.GIVEN,
    )
    assert find_inference_matches_for_rule(rule, (forged_leaf,)) == ()
    proposals = expand_cited_eta_hopf_power(chain.eta_forward, available)
    assert len(proposals) == 1
    assert proposals[0].subgoals == (chain.generator_suspension,)


def test_r2i_eta_squared_is_a_typed_composition_not_given():
    proof, chain, ancestry = build_cited_r2i_proof()
    assert isinstance(chain.conclusion.rhs, Composition)
    assert chain.conclusion.rhs.is_type_compatible()
    assert typed_stable_composition_power_latex(chain.conclusion.rhs) == r"\eta_{5}^{2}"
    assert all(step.conclusion != chain.conclusion for step in ancestry if step.rule is ProofRule.GIVEN)

```
