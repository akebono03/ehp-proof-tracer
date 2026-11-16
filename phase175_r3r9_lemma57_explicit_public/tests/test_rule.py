"""Extract only the actually cited particular nu-prime zero-image clause."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r3r9_lemma57_explicit_public.rule import (
    RULE_NAME,
    exact_lemma57_zero_image_goal,
    expand_cited_lemma57_explicit_zero,
)
from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
from proof import (
    ProofRule,
    ProofStep,
    find_inference_matches_for_rule,
)


def fixture_goal():
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    return GeneratorImage(e, prior.rhs.generator, Zero())


def test_registered_db_nu_prime_alias_matches_explicit_toda_clause() -> None:
    goal = fixture_goal()
    assert exact_lemma57_zero_image_goal(goal)
    offered = expand_cited_lemma57_explicit_zero(goal, (TodaLemma57ExplicitNuPrimeZero(),))
    assert len(offered) == 1
    assert offered[0].rule.name == RULE_NAME
    assert offered[0].subgoals == (TodaLemma57ExplicitNuPrimeZero(),)
    given = ProofStep(TodaLemma57ExplicitNuPrimeZero(), (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(offered[0].rule, (given,))
    assert len(matches) == 1
    inferred = derive_inference_proof_step(matches[0])
    assert inferred.conclusion == goal
    assert inferred.rule is ProofRule.INFERENCE
    assert inferred.premises == (given,)


def test_no_source_means_no_candidate() -> None:
    goal = fixture_goal()
    assert expand_cited_lemma57_explicit_zero(goal, ()) == ()
    assert expand_cited_lemma57_explicit_zero(
        goal, (TodaLemma57ExplicitNuPrimeZero(), TodaLemma57ExplicitNuPrimeZero()),
    ) == ()


def test_spoofed_given_or_missing_premise_is_rejected() -> None:
    goal = fixture_goal()
    option, = expand_cited_lemma57_explicit_zero(
        goal, (TodaLemma57ExplicitNuPrimeZero(),),
    )
    assert find_inference_matches_for_rule(option.rule, ()) == ()
    assert find_inference_matches_for_rule(
        option.rule, (ProofStep("not a source", (), ProofRule.GIVEN),),
    ) == ()
    assert find_inference_matches_for_rule(
        option.rule, (ProofStep(TodaLemma57ExplicitNuPrimeZero(), (), ProofRule.INFERENCE),),
    ) == ()


def test_wrong_nu_prime_and_wrong_suspension_are_rejected() -> None:
    goal = fixture_goal()
    for wrong in (
        replace(goal, map=TodaSuspensionMap(
            TodaPrimaryGroup(7, 3), TodaPrimaryGroup(8, 4),
        )),
        replace(goal, target_generator=HomotopyElement(
            "b", 3, source=7, target=3,
        )),
        replace(goal, source_generator=Composition(
            goal.source_generator.left,
            HomotopyElement(
                "ν′", 3, source=6, target=3,
                generator=GeneratorSymbol("not-registered", 3),
            ),
        )),
    ):
        assert not exact_lemma57_zero_image_goal(wrong)
        assert expand_cited_lemma57_explicit_zero(
            wrong, (TodaLemma57ExplicitNuPrimeZero(),),
        ) == ()
