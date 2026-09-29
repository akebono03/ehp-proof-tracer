from dataclasses import dataclass
from enum import Enum

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)
from toda_rules import (
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


class ClaimKind(Enum):
  GROUP_GENERATOR = "group_generator"
  ELEMENT_ORDER = "element_order"
  FREE_SUMMAND = "free_summand"
  FINITE_SUMMAND = "finite_summand"
  GROUP_DECOMPOSITION = "group_decomposition"


class ProviderKind(Enum):
  ROOT_RELATION = "root_relation"
  GROUP_RELATION = "group_relation"
  HOPF_ISOMORPHISM = "hopf_isomorphism"
  TRANSPORTED_DECOMPOSITION = "transported_decomposition"
  TARGET_ORDER = "target_order"
  DECOMPOSITION_TRANSPORT = "decomposition_transport"


@dataclass(frozen=True)
class Claim:
  kind: ClaimKind
  target_group: object
  generator: object | None = None
  order: int | None = None
  group_structure: object | None = None


@dataclass(frozen=True)
class ProviderClaim:
  provider_kind: ProviderKind
  source_step_id: int
  claim: Claim
  note: str


def _group_result(n, k):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return report.candidates[0].source_candidate.group_result


def _state(n, k):
  group_result = _group_result(n, k)
  provenance = extract_toda_recursive_proof_provenance(
    group_result
  )
  full_depth = max(
    node.shortest_depth
    for node in provenance.nodes
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=full_depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return provenance, full_depth, presentation


def _group_claims(target_group, structure):
  claims = [
    Claim(
      kind=ClaimKind.GROUP_DECOMPOSITION,
      target_group=target_group,
      group_structure=structure,
    ),
  ]

  if isinstance(structure, FreeCyclicGroup):
    claims.append(
      Claim(
        kind=ClaimKind.GROUP_GENERATOR,
        target_group=target_group,
        generator=structure.generator,
      )
    )
    claims.append(
      Claim(
        kind=ClaimKind.FREE_SUMMAND,
        target_group=target_group,
        generator=structure.generator,
      )
    )
    return tuple(claims)

  if isinstance(structure, FiniteCyclicGroup):
    claims.append(
      Claim(
        kind=ClaimKind.GROUP_GENERATOR,
        target_group=target_group,
        generator=structure.generator,
      )
    )
    claims.append(
      Claim(
        kind=ClaimKind.ELEMENT_ORDER,
        target_group=target_group,
        generator=structure.generator,
        order=structure.order,
      )
    )
    claims.append(
      Claim(
        kind=ClaimKind.FINITE_SUMMAND,
        target_group=target_group,
        generator=structure.generator,
        order=structure.order,
      )
    )
    return tuple(claims)

  if isinstance(structure, DirectSumGroup):
    for summand in structure.summands:
      if isinstance(summand, FreeCyclicGroup):
        claims.append(
          Claim(
            kind=ClaimKind.FREE_SUMMAND,
            target_group=target_group,
            generator=summand.generator,
          )
        )
      elif isinstance(summand, FiniteCyclicGroup):
        claims.append(
          Claim(
            kind=ClaimKind.FINITE_SUMMAND,
            target_group=target_group,
            generator=summand.generator,
            order=summand.order,
          )
        )
        claims.append(
          Claim(
            kind=ClaimKind.ELEMENT_ORDER,
            target_group=target_group,
            generator=summand.generator,
            order=summand.order,
          )
        )
    return tuple(claims)

  return tuple(claims)


def _root_expected_claims(presentation):
  statement = presentation.root_step.conclusion
  if not isinstance(statement, Relation):
    return ()
  if statement.relation_type is not RelationType.EQUALITY:
    return ()
  if not isinstance(statement.lhs, TodaPrimaryGroup):
    return ()
  return _group_claims(
    statement.lhs,
    statement.rhs,
  )


def _relation_provider_claims(step):
  statement = step.conclusion
  if not isinstance(statement, Relation):
    return ()
  if statement.relation_type is not RelationType.EQUALITY:
    return ()
  if not isinstance(statement.lhs, TodaPrimaryGroup):
    return ()

  return tuple(
    ProviderClaim(
      provider_kind=ProviderKind.GROUP_RELATION,
      source_step_id=id(step),
      claim=claim,
      note="typed TodaPrimaryGroup equality",
    )
    for claim in _group_claims(
      statement.lhs,
      statement.rhs,
    )
  )


def _hopf_provider_claims(step):
  statement = step.conclusion
  if not isinstance(
    statement,
    TodaProp515Pi12_5HopfIsomorphismStatement,
  ):
    return ()

  source_group = statement.map.source_group
  image_group = statement.image_group

  if not isinstance(
    image_group,
    FiniteCyclicGroup,
  ):
    return ()

  source_structure = FiniteCyclicGroup(
    order=image_group.order,
    generator=statement.source_generator,
  )

  return tuple(
    ProviderClaim(
      provider_kind=ProviderKind.HOPF_ISOMORPHISM,
      source_step_id=id(step),
      claim=claim,
      note=(
        "typed Hopf isomorphism transports image-group order "
        "to source_generator"
      ),
    )
    for claim in _group_claims(
      source_group,
      source_structure,
    )
  )


def _transported_decomposition_provider_claims(step):
  statement = step.conclusion
  if not isinstance(
    statement,
    Toda515Sigma8TransportedDecompositionStatement,
  ):
    return ()

  target_group = (
    statement.prop44_isomorphism.map.target_group
  )

  return tuple(
    ProviderClaim(
      provider_kind=ProviderKind.TRANSPORTED_DECOMPOSITION,
      source_step_id=id(step),
      claim=claim,
      note="typed transported_group",
    )
    for claim in _group_claims(
      target_group,
      statement.transported_group,
    )
  )


def _target_order_provider_claims(step, root_claims):
  statement = step.conclusion
  if not isinstance(
    statement,
    Toda48Pi16_9OrderAndE4InjectiveStatement,
  ):
    return ()

  matching_generators = {
    claim.generator
    for claim in root_claims
    if (
      claim.kind is ClaimKind.GROUP_GENERATOR
      and claim.target_group == statement.target_group
    )
  }

  if len(matching_generators) != 1:
    return ()

  generator = next(
    iter(matching_generators)
  )

  return (
    ProviderClaim(
      provider_kind=ProviderKind.TARGET_ORDER,
      source_step_id=id(step),
      claim=Claim(
        kind=ClaimKind.ELEMENT_ORDER,
        target_group=statement.target_group,
        generator=generator,
        order=statement.target_order,
      ),
      note=(
        "typed target_group + target_order; generator identity "
        "comes from the root claim for the same target group"
      ),
    ),
  )


def _find_relation_structure_by_group(provenance):
  result = {}
  for node in provenance.nodes:
    statement = node.proof_step.conclusion
    if not isinstance(statement, Relation):
      continue
    if statement.relation_type is not RelationType.EQUALITY:
      continue
    if not isinstance(statement.lhs, TodaPrimaryGroup):
      continue
    result.setdefault(
      statement.lhs,
      [],
    ).append(
      (
        node.proof_step,
        statement.rhs,
      )
    )
  return result


def _decomposition_transport_provider_claims(
  step,
  provenance,
):
  statement = step.conclusion
  if not isinstance(
    statement,
    Toda56Nu4DecompositionStatement,
  ):
    return ()

  decomposition_map = (
    statement.decomposition_isomorphism
    .prop44_isomorphism.map
  )
  source_group = decomposition_map.source_group
  target_group = decomposition_map.target_group

  if not isinstance(
    source_group,
    DirectSumGroup,
  ):
    return ()

  if len(source_group.summands) != 2:
    return ()

  relation_structures = _find_relation_structure_by_group(
    provenance
  )

  first_group = source_group.summands[0]
  second_group = source_group.summands[1]

  first_candidates = relation_structures.get(
    first_group,
    (),
  )
  second_candidates = relation_structures.get(
    second_group,
    (),
  )

  if not first_candidates or not second_candidates:
    return ()

  first_structure = first_candidates[0][1]
  second_structure = second_candidates[0][1]

  transported_summands = []

  if isinstance(
    first_structure,
    FreeCyclicGroup,
  ):
    from homotopy_groups import Suspension
    transported_summands.append(
      FreeCyclicGroup(
        generator=Suspension(
          expression=first_structure.generator
        )
      )
    )
  elif isinstance(
    first_structure,
    FiniteCyclicGroup,
  ):
    from homotopy_groups import Suspension
    transported_summands.append(
      FiniteCyclicGroup(
        order=first_structure.order,
        generator=Suspension(
          expression=first_structure.generator
        ),
      )
    )

  if isinstance(
    second_structure,
    FreeCyclicGroup,
  ):
    from homotopy_groups import Composition
    transported_summands.append(
      FreeCyclicGroup(
        generator=Composition(
          left=decomposition_map.alpha,
          right=second_structure.generator,
        )
      )
    )
  elif isinstance(
    second_structure,
    FiniteCyclicGroup,
  ):
    from homotopy_groups import Composition
    transported_summands.append(
      FiniteCyclicGroup(
        order=second_structure.order,
        generator=Composition(
          left=decomposition_map.alpha,
          right=second_structure.generator,
        ),
      )
    )

  nonzero_summands = tuple(
    summand
    for summand in transported_summands
    if summand is not None
  )

  if len(nonzero_summands) == 1:
    transported_group = nonzero_summands[0]
  else:
    transported_group = DirectSumGroup(
      summands=nonzero_summands
    )

  return tuple(
    ProviderClaim(
      provider_kind=ProviderKind.DECOMPOSITION_TRANSPORT,
      source_step_id=id(step),
      claim=claim,
      note=(
        "typed decomposition map transports source-group "
        "cyclic structures into target-group generators"
      ),
    )
    for claim in _group_claims(
      target_group,
      transported_group,
    )
  )


def _provider_claims(
  step,
  provenance,
  root_claims,
):
  result = []
  result.extend(
    _relation_provider_claims(
      step
    )
  )
  result.extend(
    _hopf_provider_claims(
      step
    )
  )
  result.extend(
    _transported_decomposition_provider_claims(
      step
    )
  )
  result.extend(
    _target_order_provider_claims(
      step,
      root_claims,
    )
  )
  result.extend(
    _decomposition_transport_provider_claims(
      step,
      provenance,
    )
  )
  return tuple(result)


def _claim_text(claim):
  return (
    f"{claim.kind.value}: "
    f"target={claim.target_group!r}, "
    f"generator={claim.generator!r}, "
    f"order={claim.order!r}, "
    f"structure={claim.group_structure!r}"
  )


def main():
  print("=" * 120)
  print("Phase 144-6-R5-12 typed provider semantics prototype audit")
  print("=" * 120)
  print(
    "Audit only. No production code, tests, or project documents are modified."
  )
  print(
    "Classification uses Python statement types and typed fields only. "
    "Inference-rule names are not parsed."
  )
  print()

  total_expected = 0
  total_matched = 0
  total_unmatched = 0
  provider_kind_counts = {}

  for n, k in TARGETS:
    provenance, full_depth, presentation = _state(
      n,
      k,
    )
    expected = _root_expected_claims(
      presentation
    )

    providers = []
    for node in provenance.nodes:
      providers.extend(
        _provider_claims(
          node.proof_step,
          provenance,
          expected,
        )
      )

    root_step_id = id(
      presentation.root_step
    )
    non_root_providers = tuple(
      provider
      for provider in providers
      if provider.source_step_id != root_step_id
    )

    print("-" * 120)
    print(
      f"TARGET n={n}, k={k} "
      f"full_depth={full_depth} "
      f"expected_claims={len(expected)} "
      f"provider_claims={len(non_root_providers)}"
    )
    print("-" * 120)

    for index, claim in enumerate(
      expected,
      start=1,
    ):
      matches = tuple(
        provider
        for provider in non_root_providers
        if provider.claim == claim
      )

      total_expected += 1
      if matches:
        total_matched += 1
      else:
        total_unmatched += 1

      print(
        f"EXPECTED[{index:02d}] {_claim_text(claim)}"
      )
      print(
        f"  matched_provider_count={len(matches)}"
      )

      for match_index, provider in enumerate(
        matches,
        start=1,
      ):
        provider_kind_counts[
          provider.provider_kind
        ] = (
          provider_kind_counts.get(
            provider.provider_kind,
            0,
          )
          + 1
        )
        print(
          f"  MATCH[{match_index:02d}] "
          f"kind={provider.provider_kind.value} "
          f"note={provider.note}"
        )

    unmatched_provider_claims = tuple(
      provider
      for provider in non_root_providers
      if provider.claim not in expected
    )

    print(
      f"unmatched_non_root_provider_claims="
      f"{len(unmatched_provider_claims)}"
    )
    for index, provider in enumerate(
      unmatched_provider_claims[:12],
      start=1,
    ):
      print(
        f"  EXTRA[{index:02d}] "
        f"kind={provider.provider_kind.value} "
        f"{_claim_text(provider.claim)}"
      )
    if len(unmatched_provider_claims) > 12:
      print(
        f"  ... {len(unmatched_provider_claims) - 12} more"
      )

    print()

  print("=" * 120)
  print("SUMMARY")
  print("=" * 120)
  print(
    f"total_expected_claims={total_expected}"
  )
  print(
    f"total_matched_expected_claims={total_matched}"
  )
  print(
    f"total_unmatched_expected_claims={total_unmatched}"
  )
  print(
    "matched_provider_kind_counts="
    + repr(
      {
        kind.value: count
        for kind, count in sorted(
          provider_kind_counts.items(),
          key=lambda item: item[0].value,
        )
      }
    )
  )
  print()
  print("=" * 120)
  print("INTERPRETATION")
  print("=" * 120)
  print(
    "PASS criterion for this prototype: every final root claim component "
    "that should have an explanatory provider is matched by at least one "
    "non-root typed provider, without rule-name parsing."
  )
  print(
    "GROUP_DECOMPOSITION may remain unmatched for cases where the root inference "
    "itself is the integration step. Such cases must be inspected rather than "
    "silently treated as provider failure."
  )
  print(
    "If pi_10^4 matches through decomposition_transport, the audit demonstrates "
    "that a distributed provider can be reconstructed from typed source-group "
    "relations plus a typed decomposition map."
  )
  print(
    "If duplicate matches remain, the next problem is provider selection, not "
    "claim discovery."
  )


if __name__ == "__main__":
  main()
