"""Small, source-independent tests for R3R1 diagnostic helpers."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from expression import HomotopyElement, MapApplication
from map_facts import EHP_H_MAP
from phase172_r3r1_hopf_chain_audit.audit import (
    descendants_of_proof_premises,
    exact_math_line_candidates,
    index_for,
    is_hopf_relation,
)
from proof import Relation, RelationType


@dataclass(frozen=True)
class Node:
    name: str
    premises: tuple[object, ...] = ()


def test_index_for_unique_identity_and_equal_value():
    steps = (Node('premise'), Node('conclusion'))
    assert index_for(steps[0], steps) == 0
    assert index_for(Node('premise'), steps) == 0


def test_index_for_fails_closed_when_missing_or_ambiguous():
    with pytest.raises(ValueError):
        index_for(Node('absent'), (Node('premise'),))
    with pytest.raises(ValueError):
        index_for(Node('same'), (Node('same'), Node('same')))


def test_descendants_traverse_actual_premise_closure():
    a = Node('a')
    b = Node('b', (a,))
    c = Node('c', (b, a))
    assert descendants_of_proof_premises((a, b, c), 2) == (0, 1, 2)
    assert descendants_of_proof_premises((a, b, c), 0) == (0,)


def test_line_correspondence_requires_an_exact_math_block():
    body = ['$H(x)=y$.', '$H(x)=yz$.', '$H(x)=y$ は結論.', '文字列 H(x)=y']
    candidates = exact_math_line_candidates(body, 'H(x)=y')
    assert [x['line_number'] for x in candidates] == [1, 3]
    assert exact_math_line_candidates(body, None) == []


def test_hopf_relation_requires_typed_map_and_equality():
    x = HomotopyElement('x', 3)
    y = HomotopyElement('y', 3)
    target = Relation(MapApplication(EHP_H_MAP, x), y, RelationType.EQUALITY)
    assert is_hopf_relation(target)
    assert not is_hopf_relation(Relation(x, y, RelationType.EQUALITY))
    assert not is_hopf_relation('H(x)=y')
