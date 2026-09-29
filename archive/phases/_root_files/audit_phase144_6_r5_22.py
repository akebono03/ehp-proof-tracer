from dataclasses import dataclass, fields, is_dataclass
from enum import Enum

from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)


MISSING_KEYS = (
  "hopf_nu_prime",
  "nu_eta6_membership",
  "hopf_nu_eta6",
  "pi7_5_group",
)


class StructureLocation(Enum):
  EXACT_PRESENTATION_CONCLUSION = "exact_presentation_conclusion"
  EMBEDDED_IN_PRESENTATION_CONCLUSION = "embedded_in_presentation_conclusion"
  EMBEDDED_IN_PRESENTATION_PREMISE = "embedded_in_presentation_premise"
  ABSENT_FROM_PRESENTATION_CLOSURE = "absent_from_presentation_closure"


@dataclass(frozen=True)
class StructureTrace:
  key: str
  canonical_type: str
  exact_conclusion_hits: int
  embedded_conclusion_hits: int
  embedded_premise_hits: int
  owner_statement_types: tuple[str, ...]
  location: StructureLocation


def _iter_children(value):
  if is_dataclass(value):
    for field in fields(value):
      yield getattr(value, field.name)
    return

  if isinstance(value, dict):
    for key, item in value.items():
      yield key
      yield item
    return

  if isinstance(value, (tuple, list, set, frozenset)):
    yield from value


def _contains_equal(root, target, active_ids=None):
  if root == target:
    return True

  if active_ids is None:
    active_ids = set()

  if isinstance(root, (str, bytes, int, float, bool, type(None), Enum)):
    return False

  root_id = id(root)
  if root_id in active_ids:
    return False

  active_ids.add(root_id)
  try:
    return any(
      _contains_equal(child, target, active_ids)
      for child in _iter_children(root)
    )
  finally:
    active_ids.remove(root_id)


def _walk_premise_steps(step, visited=None):
  if visited is None:
    visited = set()

  step_id = id(step)
  if step_id in visited:
    return

  visited.add(step_id)

  for premise in step.premises:
    yield premise
    yield from _walk_premise_steps(premise, visited)


def _canonical_targets():
  data = build_phase65_3_data()

  hopf_nu_prime = data["hopf_nu_prime_step"].conclusion
  equation57 = data["equation57_step"].conclusion
  nu_eta6 = equation57.lhs.expression
  pi7_5_group = data["prop53_step"].conclusion

  return {
    "hopf_nu_prime": hopf_nu_prime,
    "nu_eta6_membership": nu_eta6,
    "hopf_nu_eta6": equation57,
    "pi7_5_group": pi7_5_group,
  }


def build_statement_structure_traces():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)

  presentation_steps = tuple(
    dict.fromkeys(
      step
      for block in blocks
      for step in block.steps
    )
  )
  targets = _canonical_targets()
  traces = []

  for key in MISSING_KEYS:
    target = targets[key]

    exact_steps = tuple(
      step
      for step in presentation_steps
      if step.conclusion == target
    )
    embedded_conclusion_steps = tuple(
      step
      for step in presentation_steps
      if (
        step.conclusion != target
        and _contains_equal(step.conclusion, target)
      )
    )

    embedded_premise_owners = []
    for owner in presentation_steps:
      if any(
        (
          premise.conclusion == target
          or _contains_equal(premise.conclusion, target)
        )
        for premise in _walk_premise_steps(owner)
      ):
        embedded_premise_owners.append(owner)

    owner_types = tuple(
      dict.fromkeys(
        type(step.conclusion).__name__
        for step in (
          *exact_steps,
          *embedded_conclusion_steps,
          *embedded_premise_owners,
        )
      )
    )

    if exact_steps:
      location = StructureLocation.EXACT_PRESENTATION_CONCLUSION
    elif embedded_conclusion_steps:
      location = StructureLocation.EMBEDDED_IN_PRESENTATION_CONCLUSION
    elif embedded_premise_owners:
      location = StructureLocation.EMBEDDED_IN_PRESENTATION_PREMISE
    else:
      location = StructureLocation.ABSENT_FROM_PRESENTATION_CLOSURE

    traces.append(
      StructureTrace(
        key=key,
        canonical_type=type(target).__name__,
        exact_conclusion_hits=len(exact_steps),
        embedded_conclusion_hits=len(embedded_conclusion_steps),
        embedded_premise_hits=len(embedded_premise_owners),
        owner_statement_types=owner_types,
        location=location,
      )
    )

  return tuple(traces)


def print_audit():
  traces = build_statement_structure_traces()

  print("=" * 78)
  print("Phase 144-6-R5-22 missing 4 facts statement-structure audit")
  print("production changes: none")
  print("=" * 78)

  for trace in traces:
    print(f"\\n{trace.key}")
    print("-" * 78)
    print(f"canonical_type={trace.canonical_type}")
    print(f"exact_conclusion_hits={trace.exact_conclusion_hits}")
    print(f"embedded_conclusion_hits={trace.embedded_conclusion_hits}")
    print(f"embedded_premise_hits={trace.embedded_premise_hits}")
    print(
      "owner_statement_types="
      + (
        ",".join(trace.owner_statement_types)
        if trace.owner_statement_types
        else "-"
      )
    )
    print(f"location={trace.location.value}")

  print("\\nLocation summary")
  print("-" * 78)
  for location in StructureLocation:
    keys = tuple(
      trace.key
      for trace in traces
      if trace.location is location
    )
    print(f"{location.value}: {len(keys)}")
    for key in keys:
      print(f"  - {key}")

  print("\\nInterpretation boundary")
  print("-" * 78)
  print(
    "exact_presentation_conclusion means the mathematical fact already exists "
    "as a current presentation ProofStep conclusion."
  )
  print(
    "embedded_in_presentation_conclusion means the fact is represented as a "
    "field/subobject of a current conclusion rather than as its own conclusion."
  )
  print(
    "embedded_in_presentation_premise means the fact survives only in the "
    "recursive premise closure of a current presentation step."
  )
  print(
    "absent_from_presentation_closure means the canonical Phase 65 object was "
    "not found even recursively; this result requires a subsequent provenance "
    "construction audit before changing rendering."
  )


if __name__ == "__main__":
  print_audit()

