import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from toda_group_lookup import (
  find_known_toda_group_results,
  is_toda_group_result_for_target,
)
from toda_group_query import (
  TodaGroupQuery,
)


def make_generator(
  name,
  family,
  index,
  dimension,
):
  return HomotopyElement(
    name=name,
    dimension=dimension,
    generator=GeneratorSymbol(
      family=family,
      index=index,
    ),
  )


def make_entry(
  key,
  conclusion,
  rule=ProofRule.GIVEN,
):
  return ProofRepositoryEntry(
    key=key,
    step=ProofStep(
      conclusion=conclusion,
      premises=(),
      rule=rule,
    ),
  )


def test_phase90_3_2_predicate_accepts_finite_cyclic_group_relation():
  target = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=4,
  )
  relation = Relation(
    lhs=target,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=make_generator(
        name="nu4_squared",
        family="nu^2",
        index=4,
        dimension=10,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert is_toda_group_result_for_target(
    relation,
    target,
  )


def test_phase90_3_2_predicate_accepts_free_cyclic_group_relation():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )
  relation = Relation(
    lhs=target,
    rhs=FreeCyclicGroup(
      generator=make_generator(
        name="iota_5",
        family="iota",
        index=5,
        dimension=5,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert is_toda_group_result_for_target(
    relation,
    target,
  )


def test_phase90_3_2_predicate_accepts_direct_sum_group_relation():
  target = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=4,
  )
  relation = Relation(
    lhs=target,
    rhs=DirectSumGroup(
      summands=(
        FreeCyclicGroup(
          generator=make_generator(
            name="nu_4",
            family="nu",
            index=4,
            dimension=7,
          ),
        ),
        FiniteCyclicGroup(
          order=4,
          generator=make_generator(
            name="E_nu_prime",
            family="E_nu_prime",
            index=4,
            dimension=7,
          ),
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert is_toda_group_result_for_target(
    relation,
    target,
  )


def test_phase90_3_2_predicate_accepts_zero_statement():
  target = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=2,
  )
  statement = TodaPrimaryGroupZeroStatement(
    group=target,
  )

  assert is_toda_group_result_for_target(
    statement,
    target,
  )


def test_phase90_3_2_predicate_rejects_wrong_target():
  target = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=4,
  )
  relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=5,
    ),
    rhs=FiniteCyclicGroup(
      order=8,
      generator=make_generator(
        name="nu5_squared",
        family="nu^2",
        index=5,
        dimension=11,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert not is_toda_group_result_for_target(
    relation,
    target,
  )


def test_phase90_3_2_predicate_rejects_non_equality_relation():
  target = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=4,
  )
  relation = Relation(
    lhs=target,
    rhs=8,
    relation_type=RelationType.ORDER,
  )

  assert not is_toda_group_result_for_target(
    relation,
    target,
  )


def test_phase90_3_2_predicate_rejects_unsupported_equality_rhs():
  target = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=4,
  )
  relation = Relation(
    lhs=target,
    rhs="not-a-group-structure",
    relation_type=RelationType.EQUALITY,
  )

  assert not is_toda_group_result_for_target(
    relation,
    target,
  )


def test_phase90_3_2_predicate_rejects_unrelated_statement():
  target = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=4,
  )

  assert not is_toda_group_result_for_target(
    "unrelated",
    target,
  )


def test_phase90_3_2_predicate_rejects_non_toda_target():
  with pytest.raises(
    TypeError,
    match="target must be a TodaPrimaryGroup",
  ):
    is_toda_group_result_for_target(
      "unrelated",
      "not-a-target",
    )


def test_phase90_3_2_lookup_returns_empty_tuple_when_not_found():
  repository = ProofRepository()
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  assert (
    find_known_toda_group_results(
      repository,
      query,
    )
    == ()
  )


def test_phase90_3_2_lookup_returns_given_and_inference_results():
  repository = ProofRepository()
  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  target = query.target
  relation = Relation(
    lhs=target,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=make_generator(
        name="nu4_squared",
        family="nu^2",
        index=4,
        dimension=10,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )
  given_entry = make_entry(
    key="phase90.given",
    conclusion=relation,
    rule=ProofRule.GIVEN,
  )
  inference_entry = make_entry(
    key="phase90.inference",
    conclusion=relation,
    rule=ProofRule.INFERENCE,
  )

  repository.register(
    given_entry
  )
  repository.register(
    inference_entry
  )

  assert (
    find_known_toda_group_results(
      repository,
      query,
    )
    == (
      given_entry,
      inference_entry,
    )
  )


def test_phase90_3_2_lookup_preserves_registration_order():
  repository = ProofRepository()
  query = TodaGroupQuery(
    n=5,
    k=0,
  )
  relation = Relation(
    lhs=query.target,
    rhs=FreeCyclicGroup(
      generator=make_generator(
        name="iota_5",
        family="iota",
        index=5,
        dimension=5,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )
  first_entry = make_entry(
    key="phase90.first",
    conclusion=relation,
  )
  second_entry = make_entry(
    key="phase90.second",
    conclusion=relation,
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  assert (
    find_known_toda_group_results(
      repository,
      query,
    )
    == (
      first_entry,
      second_entry,
    )
  )


def test_phase90_3_2_lookup_includes_zero_statement():
  repository = ProofRepository()
  query = TodaGroupQuery(
    n=2,
    k=7,
  )
  zero_entry = make_entry(
    key="phase90.zero",
    conclusion=(
      TodaPrimaryGroupZeroStatement(
        group=query.target,
      )
    ),
    rule=ProofRule.INFERENCE,
  )

  repository.register(
    zero_entry
  )

  assert (
    find_known_toda_group_results(
      repository,
      query,
    )
    == (
      zero_entry,
    )
  )


def test_phase90_3_2_lookup_excludes_wrong_target_and_non_group_relation():
  repository = ProofRepository()
  query = TodaGroupQuery(
    n=4,
    k=6,
  )
  target = query.target
  matching_entry = make_entry(
    key="phase90.matching",
    conclusion=Relation(
      lhs=target,
      rhs=FiniteCyclicGroup(
        order=8,
        generator=make_generator(
          name="nu4_squared",
          family="nu^2",
          index=4,
          dimension=10,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
  )
  wrong_target_entry = make_entry(
    key="phase90.wrong_target",
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=5,
      ),
      rhs=FiniteCyclicGroup(
        order=8,
        generator=make_generator(
          name="nu5_squared",
          family="nu^2",
          index=5,
          dimension=11,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
  )
  non_group_relation_entry = make_entry(
    key="phase90.non_group_relation",
    conclusion=Relation(
      lhs=target,
      rhs=8,
      relation_type=RelationType.ORDER,
    ),
  )

  repository.register(
    wrong_target_entry
  )
  repository.register(
    matching_entry
  )
  repository.register(
    non_group_relation_entry
  )

  assert (
    find_known_toda_group_results(
      repository,
      query,
    )
    == (
      matching_entry,
    )
  )


def test_phase90_3_2_lookup_rejects_non_repository():
  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  with pytest.raises(
    TypeError,
    match="repository must be a ProofRepository",
  ):
    find_known_toda_group_results(
      "not-a-repository",
      query,
    )


def test_phase90_3_2_lookup_rejects_non_query():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match="query must be a TodaGroupQuery",
  ):
    find_known_toda_group_results(
      repository,
      "not-a-query",
    )
