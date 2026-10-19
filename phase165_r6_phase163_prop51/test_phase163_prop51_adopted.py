"""Phase 165 R6: explicit typed Proposition 5.1 input, not legacy proof extraction."""
from dataclasses import fields, replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, ScalarSymbol
from homotopy_groups import FreeCyclicGroup
from phase163_r4_r12_literature_registration import (
    LiteratureComponentInput,
    SCOPES,
    register_prop51_prop53_literature_statements,
    _validate_component,
)
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from proof import ProofRule, Relation
from scalar_rules import ScalarGreaterEqualStatement


def prop51_explicit_inputs():
    """Use the current explicitly adopted typed clauses, never old ProofSteps."""
    adopted = build_adopted_prop51_reference()
    content = adopted.registry.assertion(
        "toda:adopted:prop5.1:finite_dimensional"
    ).content
    keys = (
        "pi3_2_group_relation",
        "eta2_hopf_relation",
        "delta_iota5_relation",
        "higher_eta_group_relation",
    )
    n = ScalarSymbol(name="n")
    return tuple(
        LiteratureComponentInput(
            locator="Proposition 5.1",
            component_key=key,
            statement=getattr(content, key),
            source_description="Explicitly adopted typed Proposition 5.1; edition unverified",
            scope_statement=(
                ScalarGreaterEqualStatement(left=n, right=SCOPES["Proposition 5.1"])
                if key == "higher_eta_group_relation" else None
            ),
        )
        for key in keys
    )


def test_prop51_adopted_four_typed_components_pass_validation():
    items = prop51_explicit_inputs()
    assert len(items) == 4
    for item in items:
        _validate_component(item)
    assert {item.component_key for item in items} == {
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    }


def test_prop51_wrong_generator_is_rejected():
    item = prop51_explicit_inputs()[0]
    bad = replace(item.statement, rhs=FreeCyclicGroup(
        generator=HomotopyElement(
            name="other", dimension=2,
            generator=GeneratorSymbol(family="η", index=9),
        )
    ))
    assert isinstance(item.statement, Relation)
    with pytest.raises(ValueError, match="generator"):
        _validate_component(replace(item, statement=bad))


def test_prop51_wrong_higher_scope_is_rejected():
    item = prop51_explicit_inputs()[-1]
    with pytest.raises(ValueError, match="scope"):
        _validate_component(replace(item, scope_statement=ScalarGreaterEqualStatement(
            left=ScalarSymbol(name="n"), right=5,
        )))


def test_prop51_adopted_reference_has_no_certified_proof_ancestry():
    bridge = build_adopted_prop51_reference()
    assertion = bridge.registry.assertion("toda:adopted:prop5.1:finite_dimensional")
    assert assertion.content is not None
    assert len(fields(assertion.content)) == 4
    # A registered literature claim must not be mistaken for a derived inference.
    assert all(link.step.conclusion != assertion.content or link.step.rule is not ProofRule.INFERENCE
               for link in bridge.proof_links)
