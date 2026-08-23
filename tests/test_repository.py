import pytest
from expression import Multiple, Zero, eta, nu
from proof import Relation, RelationType
from repository import RelationRepository


def test_relation_repository_add_relation():
  repository = RelationRepository()

  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  repository.add_relation(relation)

  assert repository.all_relations() == [
    relation
  ]


def test_relation_repository_initial_relations():
  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  repository = RelationRepository([
    relation,
  ])

  assert repository.all_relations() == [
    relation
  ]


def test_relation_repository_find_by_lhs():
  relation1 = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  relation2 = Relation(
    lhs=Multiple(2, nu(4)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  repository = RelationRepository([
    relation1,
    relation2,
  ])

  result = repository.find_relations(
    lhs=Multiple(2, eta(3)),
  )

  assert result == [
    relation1
  ]


def test_relation_repository_find_by_rhs():
  relation1 = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  relation2 = Relation(
    lhs=eta(3),
    rhs=nu(4),
    relation_type=RelationType.EQUALITY,
  )

  repository = RelationRepository([
    relation1,
    relation2,
  ])

  result = repository.find_relations(
    rhs=Zero(),
  )

  assert result == [
    relation1
  ]


def test_relation_repository_find_by_relation_type():
  relation1 = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  relation2 = Relation(
    lhs=eta(3),
    rhs=nu(4),
    relation_type=RelationType.EQUALITY,
  )

  repository = RelationRepository([
    relation1,
    relation2,
  ])

  result = repository.find_relations(
    relation_type=RelationType.ZERO,
  )

  assert result == [
    relation1
  ]


def test_relation_repository_find_by_source():
  relation1 = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  relation2 = Relation(
    lhs=Multiple(2, nu(4)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Other",
  )

  repository = RelationRepository([
    relation1,
    relation2,
  ])

  result = repository.find_relations(
    source="Toda",
  )

  assert result == [
    relation1
  ]


def test_relation_repository_find_multiple_conditions():
  relation1 = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  relation2 = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Other",
  )

  relation3 = Relation(
    lhs=Multiple(2, nu(4)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  repository = RelationRepository([
    relation1,
    relation2,
    relation3,
  ])

  result = repository.find_relations(
    lhs=Multiple(2, eta(3)),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  assert result == [
    relation1
  ]


def test_relation_repository_find_no_match():
  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  repository = RelationRepository([
    relation,
  ])

  result = repository.find_relations(
    lhs=nu(4),
  )

  assert result == []


def test_relation_repository_all_relations_returns_copy():
  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  repository = RelationRepository([
    relation,
  ])

  relations = repository.all_relations()
  relations.clear()

  assert repository.all_relations() == [
    relation
  ]


def test_relation_repository_rejects_non_relation():
  repository = RelationRepository()

  with pytest.raises(TypeError):
    repository.add_relation(
      "2η3 = 0"
    )









