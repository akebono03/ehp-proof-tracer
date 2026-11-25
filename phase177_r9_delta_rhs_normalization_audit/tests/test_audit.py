"""Diagnostic contract tests; no synthetic proof is accepted as live evidence."""
from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase177_r9_delta_rhs_normalization_audit.audit import (
    HEAD, PINS, canonical_delta, flatten_typed, probe_goals, route_matches, status,
)
from proof import Relation


def variant():
    canonical = canonical_delta()
    a,b,c = flatten_typed(canonical.rhs)
    db = replace(a.expression,name="ν'",generator=GeneratorSymbol("\\nu'"))
    actual = Relation(canonical.lhs, Composition(IteratedSuspension(db,1),Composition(b,c)))
    return canonical,actual


def test_exact_diagnostic_variant_and_probes():
    canonical,actual = variant()
    assert route_matches(canonical,actual)
    probes = probe_goals(canonical,actual)
    assert len(probes) == 16
    assert probes['canonical_delta'] == canonical
    assert probes['actual_delta'] == actual
    assert probes['entire_rhs_equality'] == Relation(canonical.rhs,actual.rhs)
    a,b,c = flatten_typed(canonical.rhs)
    assert probes['canonical_associativity'] == Relation(canonical.rhs,Composition(a,Composition(b,c)))
    assert probes['notation_only_delta'].rhs == Composition(Composition(actual.rhs.left,b),c)
    for name,g in probes.items():
        if name.endswith('_delta'):
            assert g.lhs == canonical.lhs
            assert typed_endpoints(g.rhs) == typed_endpoints(canonical.rhs)
        else:
            assert typed_endpoints(g.lhs) is not None
            assert typed_endpoints(g.lhs) == typed_endpoints(g.rhs)
            assert g.lhs != g.rhs


def test_does_not_identify_nu4_or_unrelated_alias():
    canonical,actual = variant()
    d = actual.rhs.left
    wrong_nu = HomotopyElement('ν₄',4,7,4,GeneratorSymbol('ν',index=4))
    for wrong in (wrong_nu, replace(d,exponent=2),
                  replace(d,expression=replace(d.expression,name='unrelated')),
                  replace(d,expression=replace(d.expression,generator=GeneratorSymbol('η'))),
                  replace(d,expression=replace(d.expression,source=7))):
        target = Relation(actual.lhs,Composition(wrong,actual.rhs.right))
        assert not route_matches(canonical,target)
        with pytest.raises(ValueError,match='EXPECTED_STRICT_ROUTE_VARIANT'):
            probe_goals(canonical,target)


def test_flatten_preserves_order_and_rejects_bad_composition():
    canonical,actual = variant()
    a,b,c = flatten_typed(canonical.rhs)
    assert flatten_typed(Composition(a,Composition(b,c))) == (a,b,c)
    assert flatten_typed(Composition(b,a)) is None
    assert flatten_typed(object()) is None
    assert flatten_typed(actual.rhs)[1:] == (b,c)


@pytest.mark.parametrize('row,expected', [
    ({'proved':True,'target_calls':[]},'PROVED'),
    ({'proved':False,'target_calls':[]},'NO_CANDIDATES'),
    ({'proved':False,'target_calls':[[],[]]},'NO_CANDIDATES'),
    ({'proved':False,'target_calls':[[],[{'rule':'candidate'}]]},'CANDIDATES_UNRESOLVED'),
])
def test_status(row,expected):
    assert status(row) == expected


def test_review_pins():
    assert HEAD == '8127b7b6424f294a6e03b3e2d12e66a83e77cf5d'
    assert 'phase177_r8_unsigned_delta_public/provider.py' in PINS
    assert 'phase174_r3_r7_r9_composition_associativity/rule.py' in PINS
    assert all(len(pin)==40 for pin in PINS.values())
