from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, Multiple, TodaBracket
from phase163_r4_r8_choice_registration import (
    LiteratureChoice,
    build_nu_prime_choice,
    nu_prime_bracket_matches,
    register_literature_choices,
)
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from proof import ProofRule, ProofStep
from toda_rules import TodaBracketMembershipStatement


def _nu_prime_step(index=1):
    nu = HomotopyElement(name="ν′", dimension=3, source=6, target=3,
                         generator=GeneratorSymbol(family="ν", decoration="′"))
    eta3 = HomotopyElement(name="η₃", dimension=3, generator=GeneratorSymbol(family="η", index=3))
    iota4 = HomotopyElement(name="ι_4", dimension=4, generator=GeneratorSymbol(family="ι", index=4))
    eta4 = HomotopyElement(name="η₄", dimension=4, generator=GeneratorSymbol(family="η", index=4))
    statement = TodaBracketMembershipStatement(
        element=nu, bracket=TodaBracket(
            first=eta3, second=Multiple(coefficient=2, expression=iota4),
            third=eta4, index=index,
        )
    )
    return ProofStep(conclusion=statement, premises=(), rule=ProofRule.GIVEN)


def _choice(step):
    return LiteratureChoice(
        assertion_id="boundary:(5.3):nu_prime_bracket_definition",
        reference_locator="(5.3)", component_key="nu_prime_bracket_definition",
        defined_symbol="ν′", statement=step.conclusion, source_step=step,
    )


def test_r4_r8_typed_selection_keeps_full_toda_bracket():
    step = _nu_prime_step()
    assert nu_prime_bracket_matches(step.conclusion)
    assert step.conclusion.bracket.index == 1
    assert step.conclusion.bracket.second.coefficient == 2
    assert step.conclusion.bracket.first.generator.index == 3
    assert step.conclusion.bracket.third.generator.index == 4


def test_r4_r8_selection_keeps_bridge_metadata_only():
    base = build_registry_bridge()
    result = build_nu_prime_choice(base, _nu_prime_step())
    target = "boundary:(5.3):nu_prime_bracket_definition"
    assert result.find(target).statement == _nu_prime_step().conclusion
    assert next(record.status for record in base.records if record.assertion_id == target) is MigrationStatus.METADATA_ONLY
    assert result.bridge is base


def test_r4_r8_wrong_bracket_index_is_rejected():
    with pytest.raises(ValueError, match="not nu-prime"):
        build_nu_prime_choice(build_registry_bridge(), _nu_prime_step(index=2))


def test_r4_r8_given_with_premises_is_rejected():
    step = _nu_prime_step()
    with pytest.raises(ValueError, match="leaf GIVEN"):
        _choice(replace(step, premises=(step,)))


def test_r4_r8_derived_proof_is_not_labeled_choice():
    step = _nu_prime_step()
    with pytest.raises(ValueError, match="leaf GIVEN"):
        _choice(replace(step, rule=ProofRule.INFERENCE))


def test_r4_r8_duplicate_choice_is_rejected():
    step = _nu_prime_step()
    with pytest.raises(ValueError, match="duplicate"):
        register_literature_choices(build_registry_bridge(), (_choice(step), _choice(step)))


def test_r4_r8_wrong_assertion_identity_is_rejected():
    with pytest.raises(ValueError, match="identity mismatch"):
        replace(_choice(_nu_prime_step()), assertion_id="boundary:(5.3):nu_prime_hopf_relation")


def test_r4_r8_unknown_boundary_is_rejected():
    choice = _choice(_nu_prime_step())
    with pytest.raises(ValueError, match="not an eligible boundary"):
        register_literature_choices(
            build_registry_bridge(),
            (replace(choice, reference_locator="(9.9)", assertion_id="boundary:(9.9):nu_prime_bracket_definition"),),
        )
