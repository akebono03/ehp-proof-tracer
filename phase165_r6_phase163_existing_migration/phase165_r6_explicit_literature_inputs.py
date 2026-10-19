"""Typed literature candidates, never bootstrapped from ProofStep ancestry."""
from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, ScalarSum, ScalarSymbol, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import build_registry_bridge
from phase163_r4_r11_literature_registration import (
    LiteratureAssertionInput, register_prop56_literature_statements,
)
from phase163_r4_r12_literature_registration import (
    LiteratureComponentInput, _validate_component,
    register_prop51_prop53_literature_statements,
)
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from proof import Relation, RelationType
from scalar_rules import ScalarGreaterEqualStatement


def _element(family, index, *, decoration=None):
    return HomotopyElement(
        name=f"{family}_{index}", dimension=index,
        generator=GeneratorSymbol(family=family, index=index, decoration=decoration),
    )


def _equality(dimension, sphere, structure):
    return Relation(
        lhs=TodaPrimaryGroup(group_dimension=dimension, sphere_dimension=sphere),
        rhs=structure,
        relation_type=RelationType.EQUALITY,
    )


def prop53_inputs():
    n = ScalarSymbol(name="n")
    values = (
        ("pi4_2_group_relation", 4, 2),
        ("pi5_3_group_relation", 5, 3),
        ("pi6_4_group_relation", 6, 4),
    )
    output = []
    for key, dimension, sphere in values:
        generator = Composition(_element("η", sphere), _element("η", sphere + 1))
        output.append(LiteratureComponentInput(
            locator="Proposition 5.3", component_key=key,
            statement=_equality(dimension, sphere, FiniteCyclicGroup(order=2, generator=generator)),
            source_description="Explicit typed Toda Proposition 5.3 candidate; source unverified",
        ))
    higher_generator = Composition(_element("η", n), _element("η", ScalarSum(n, 1)))
    output.append(LiteratureComponentInput(
        locator="Proposition 5.3", component_key="higher_eta_squared_group_relation",
        statement=_equality(ScalarSum(n, 2), n, FiniteCyclicGroup(order=2, generator=higher_generator)),
        source_description="Explicit typed Toda Proposition 5.3 candidate; source unverified",
        scope_statement=ScalarGreaterEqualStatement(left=n, right=5),
    ))
    return tuple(output)


def prop51_inputs():
    bridge = build_adopted_prop51_reference()
    adopted = bridge.registry.assertion("toda:adopted:prop5.1:finite_dimensional").content
    keys = (
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    )
    return tuple(LiteratureComponentInput(
        locator="Proposition 5.1", component_key=key,
        statement=getattr(adopted, key),
        source_description="Explicitly adopted typed Proposition 5.1 clause; source unverified",
        scope_statement=(ScalarGreaterEqualStatement(left=ScalarSymbol(name="n"), right=3)
                         if key == "higher_eta_group_relation" else None),
    ) for key in keys)


def prop56_inputs():
    n = ScalarSymbol(name="n")
    eta_triplet = Composition(
        _element("η", 2),
        Composition(_element("η", 3), _element("η", 4)),
    )
    nu_prime = HomotopyElement(
        name="ν′", dimension=3,
        generator=GeneratorSymbol(family="ν", index=3, decoration="′"),
    )
    nu4 = _element("ν", 4)
    nu5 = _element("ν", 5)
    nun = _element("ν", n)
    data = (
        ("pi5_2_group_relation", _equality(5, 2, FiniteCyclicGroup(order=2, generator=eta_triplet)), None),
        ("pi6_3_group_relation", _equality(6, 3, FiniteCyclicGroup(order=4, generator=nu_prime)), None),
        ("pi7_4_group_relation", _equality(7, 4, DirectSumGroup(summands=(
            FreeCyclicGroup(generator=nu4),
            FiniteCyclicGroup(order=4, generator=Suspension(expression=nu_prime)),
        ))), None),
        ("pi8_5_group_relation", _equality(8, 5, FiniteCyclicGroup(order=8, generator=nu5)), None),
        ("higher_nu_group_relation", _equality(ScalarSum(n, 3), n, FiniteCyclicGroup(order=8, generator=nun)),
         ScalarGreaterEqualStatement(left=n, right=6)),
    )
    return tuple(LiteratureAssertionInput(
        component_key=key, statement=statement, scope_statement=scope,
        source_description="Explicit typed Toda Proposition 5.6 candidate; source unverified",
    ) for key, statement, scope in data)



def prop51_prop53_inputs():
    return prop51_inputs() + prop53_inputs()
