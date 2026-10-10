from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from phase163_r4_r12_literature_registration import (
    COMPONENTS, LiteratureComponentInput, _validate_component,
    register_prop51_prop53_literature_statements,
)
from proof import Relation, RelationType
from scalar_rules import ScalarGreaterEqualStatement


def _inputs():
    from phase163_r4_r12_literature_registration import existing_prop51_prop53_candidates
    return existing_prop51_prop53_candidates()


def test_registers_all_eight_and_preserves_source_metadata():
    base = build_registry_bridge()
    output = register_prop51_prop53_literature_statements(base, _inputs())
    assert len(output.evidence) == 8
    assert output.snapshot.proof_links == base.proof_links
    for record in output.snapshot.records:
        if record.assertion_id in {e.assertion_id for e in output.evidence}:
            assert record.status is MigrationStatus.STRUCTURED
            assert base.registry.assertion(record.assertion_id).content != output.snapshot.registry.assertion(record.assertion_id).content
            assert any(old.assertion_id == record.assertion_id and old.status is MigrationStatus.METADATA_ONLY for old in base.records)
    assert all(e.verification_status == "SOURCE_UNVERIFIED" for e in output.evidence)
    assert all(e.proof_status == "PROOF_ANCESTRY_NOT_CHECKED" for e in output.evidence)


def test_raises_on_missing_or_duplicate_component():
    base = build_registry_bridge()
    inputs = _inputs()
    with pytest.raises(ValueError):
        register_prop51_prop53_literature_statements(base, inputs[:-1])
    with pytest.raises(ValueError):
        register_prop51_prop53_literature_statements(base, inputs[:-1] + (inputs[0],))


def test_rejects_group_wrong_generator():
    item = next(i for i in _inputs() if i.component_key == "pi4_2_group_relation")
    wrong = replace(item.statement, rhs=FiniteCyclicGroup(
        order=2, generator=HomotopyElement(
            name="other", dimension=2, generator=GeneratorSymbol(family="η", index=7)
        )
    ))
    with pytest.raises(ValueError):
        _validate_component(replace(item, statement=wrong))


def test_rejects_wrong_higher_scope():
    item = next(i for i in _inputs() if i.component_key == "higher_eta_squared_group_relation")
    with pytest.raises(ValueError):
        _validate_component(replace(item, scope_statement=ScalarGreaterEqualStatement(
            left=ScalarSymbol(name="n"), right=4
        )))


def test_rejects_missing_scope_and_concrete_extra_scope():
    inputs = _inputs()
    higher = next(i for i in inputs if i.component_key == "higher_eta_group_relation")
    concrete = next(i for i in inputs if i.component_key == "pi5_3_group_relation")
    with pytest.raises(ValueError):
        _validate_component(replace(higher, scope_statement=None))
    with pytest.raises(ValueError):
        _validate_component(replace(concrete, scope_statement=ScalarGreaterEqualStatement(
            left=ScalarSymbol(name="n"), right=5
        )))


def test_registration_does_not_replace_unrelated_records():
    base = build_registry_bridge()
    output = register_prop51_prop53_literature_statements(base, _inputs())
    targets = {e.assertion_id for e in output.evidence}
    assert all(a == b for a, b in zip(
        (r for r in base.records if r.assertion_id not in targets),
        (r for r in output.snapshot.records if r.assertion_id not in targets),
    ))


def test_validation_rejects_incorrect_delta_relation():
    item = next(i for i in _inputs() if i.component_key == "delta_iota5_relation")
    with pytest.raises(ValueError):
        _validate_component(replace(item, statement=Relation(
            lhs="Delta", rhs=0, relation_type=RelationType.EQUALITY
        )))


def test_rejects_wrong_locator_or_unknown_component():
    with pytest.raises(ValueError):
        LiteratureComponentInput("Proposition 5.6", "pi3_2_group_relation", object(), "candidate")
    with pytest.raises(ValueError):
        LiteratureComponentInput("Proposition 5.1", "pi999_group_relation", object(), "candidate")
