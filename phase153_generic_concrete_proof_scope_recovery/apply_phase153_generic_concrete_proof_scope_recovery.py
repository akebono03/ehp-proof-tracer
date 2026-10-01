from __future__ import annotations

from pathlib import Path


ROOT = Path.cwd()
TARGET = ROOT / "toda_calculation.py"
TEST = ROOT / "tests" / "test_phase153_generic_concrete_proof_scope_recovery.py"


OLD_IMPORT = '''from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
)
from proof_repository import (
'''

NEW_IMPORT = '''from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
)
from proof import (
  ProofStep,
)
from proof_repository import (
'''


OLD_STABLE_METADATA_END = '''_STABLE_TODA_GROUP_SOURCES = {
  1: (
    "eta",
    "55",
    "Toda Proposition 5.1",
  ),
  2: (
    "eta_squared",
    "59",
    "Toda Proposition 5.3",
  ),
  3: (
    "nu",
    "65",
    "Toda Proposition 5.6",
  ),
  4: (
    "four_stem_zero",
    "68",
    "Toda Proposition 5.8",
  ),
  5: (
    "five_stem_zero",
    "70",
    "Toda Proposition 5.9",
  ),
  6: (
    "nu_squared",
    "73",
    "Toda Proposition 5.11",
  ),
}


def _generator_family_and_index(
'''

NEW_STABLE_METADATA_END = '''_STABLE_TODA_GROUP_SOURCES = {
  1: (
    "eta",
    "55",
    "Toda Proposition 5.1",
  ),
  2: (
    "eta_squared",
    "59",
    "Toda Proposition 5.3",
  ),
  3: (
    "nu",
    "65",
    "Toda Proposition 5.6",
  ),
  4: (
    "four_stem_zero",
    "68",
    "Toda Proposition 5.8",
  ),
  5: (
    "five_stem_zero",
    "70",
    "Toda Proposition 5.9",
  ),
  6: (
    "nu_squared",
    "73",
    "Toda Proposition 5.11",
  ),
}


_CONCRETE_TODA_RULE_SOURCE_METADATA = (
  (
    "Toda Lemma 5.4 ",
    "Lemma 5.4",
    "60",
    "Toda Lemma 5.4",
  ),
  (
    "Toda Proposition 5.8 ",
    "Proposition 5.8",
    "68",
    "Toda Proposition 5.8",
  ),
  (
    "Toda Proposition 5.9 ",
    "Proposition 5.9",
    "70",
    "Toda Proposition 5.9",
  ),
  (
    "Toda Proposition 5.11 ",
    "Proposition 5.11",
    "73",
    "Toda Proposition 5.11",
  ),
)


def _generator_family_and_index(
'''


INSERT_BEFORE_SPECIALIZED = '''def _find_specialized_stable_toda_group_results(
'''

NEW_CONCRETE_FUNCTIONS = '''def _proof_step_repeats_conclusion_in_ancestry(
  step: ProofStep,
) -> bool:
  if not isinstance(
    step,
    ProofStep,
  ):
    raise TypeError(
      "step must be a ProofStep"
    )

  target_conclusion = step.conclusion
  visited_step_ids = set()
  stack = [
    premise
    for premise in step.premises
    if isinstance(
      premise,
      ProofStep,
    )
  ]

  while stack:
    current = stack.pop()
    current_id = id(
      current
    )

    if current_id in visited_step_ids:
      continue

    visited_step_ids.add(
      current_id
    )

    if (
      current.conclusion
      == target_conclusion
    ):
      return True

    stack.extend(
      premise
      for premise in current.premises
      if isinstance(
        premise,
        ProofStep,
      )
    )

  return False


def _resolve_existing_concrete_toda_step_source_metadata(
  step: ProofStep,
):
  if not isinstance(
    step,
    ProofStep,
  ):
    raise TypeError(
      "step must be a ProofStep"
    )

  inference_rule = (
    step.inference_rule
  )

  if inference_rule is None:
    return None

  literature_reference = (
    inference_rule.literature_reference
  )
  reference_locator = (
    None
    if literature_reference is None
    else (
      literature_reference.locator
      or literature_reference.label
    )
  )

  for (
    rule_prefix,
    locator,
    phase,
    theorem,
  ) in _CONCRETE_TODA_RULE_SOURCE_METADATA:
    if (
      reference_locator == locator
      or inference_rule.name.startswith(
        rule_prefix
      )
    ):
      return (
        phase,
        theorem,
      )

  return None


def _find_existing_concrete_proof_scope_group_results(
  repository: ProofRepository,
  query: TodaGroupQuery,
):
  if (
    query.k
    not in _STABLE_TODA_GROUP_SOURCES
  ):
    return ()

  scope = build_repository_proof_scope(
    repository
  )

  candidates = []

  for node in scope.nodes:
    step = node.proof_step

    if not is_toda_group_result_for_target(
      step.conclusion,
      query.target,
    ):
      continue

    source_metadata = (
      _resolve_existing_concrete_toda_step_source_metadata(
        step
      )
    )

    if source_metadata is None:
      continue

    if _proof_step_repeats_conclusion_in_ancestry(
      step
    ):
      continue

    candidates.append(
      (
        node,
        source_metadata,
      )
    )

  if not candidates:
    return ()

  (
    source_node,
    (
      phase,
      theorem,
    ),
  ) = min(
    candidates,
    key=lambda candidate: (
      candidate[
        0
      ].shortest_depth,
      candidate[
        0
      ].root_entry.key,
      (
        ""
        if candidate[
          0
        ].proof_step.inference_rule
        is None
        else candidate[
          0
        ].proof_step.inference_rule.name
      ),
    ),
  )

  source_entry = ProofRepositoryEntry(
    key=(
      "standard.toda.concrete::"
      f"pi_{query.n + query.k}_{query.n}"
    ),
    step=source_node.proof_step,
    phase=phase,
    theorem=theorem,
  )

  return (
    normalize_toda_group_result(
      source_entry
    ),
  )


'''


OLD_SELECTION = '''  if not group_results:
    group_results = (
      _find_specialized_stable_toda_group_results(
        repository,
        query,
      )
    )
'''

NEW_SELECTION = '''  if not group_results:
    group_results = (
      _find_existing_concrete_proof_scope_group_results(
        repository,
        query,
      )
    )

  if not group_results:
    group_results = (
      _find_specialized_stable_toda_group_results(
        repository,
        query,
      )
    )
'''


TEST_TEXT = '''import pytest

from proof import (
  ProofStep,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_calculation import (
  build_known_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import (
  TodaGroupQuery,
)


_CONCRETE_CASES = (
  (
    5,
    1,
    "standard.toda.concrete::pi_6_5",
    "60",
    "Toda Lemma 5.4",
    "Toda Lemma 5.4 pi_6^5 finite-cyclic specialization",
  ),
  (
    6,
    4,
    "standard.toda.concrete::pi_10_6",
    "68",
    "Toda Proposition 5.8",
    "Toda Proposition 5.8 pi_10^6 zero",
  ),
  (
    7,
    3,
    "standard.toda.concrete::pi_10_7",
    "73",
    "Toda Proposition 5.11",
    "Toda Proposition 5.11 pi_10^7 nu_7 specialization",
  ),
  (
    7,
    5,
    "standard.toda.concrete::pi_12_7",
    "70",
    "Toda Proposition 5.9",
    "Toda Proposition 5.9 pi_12^7 zero",
  ),
  (
    9,
    3,
    "standard.toda.concrete::pi_12_9",
    "73",
    "Toda Proposition 5.11",
    "Toda Proposition 5.11 pi_12^9 nu_9 specialization",
  ),
  (
    11,
    2,
    "standard.toda.concrete::pi_13_11",
    "73",
    "Toda Proposition 5.11",
    "Toda Proposition 5.11 pi_13^11 eta_11 squared",
  ),
  (
    13,
    1,
    "standard.toda.concrete::pi_14_13",
    "73",
    "Toda Proposition 5.11",
    "Toda Proposition 5.11 pi_14^13 eta_13",
  ),
)


@pytest.mark.parametrize(
  (
    "n",
    "k",
    "expected_key",
    "expected_phase",
    "expected_theorem",
    "expected_rule_name",
  ),
  _CONCRETE_CASES,
)
def test_phase153_generic_concrete_recovery_precedes_stable_specialization(
  n,
  k,
  expected_key,
  expected_phase,
  expected_theorem,
  expected_rule_name,
):
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=n,
        k=k,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert (
    group_result.source_entry.key
    == expected_key
  )
  assert (
    group_result.source_entry.phase
    == expected_phase
  )
  assert (
    group_result.source_entry.theorem
    == expected_theorem
  )
  assert (
    group_result.proof_step
    is group_result.source_entry.step
  )
  assert isinstance(
    group_result.proof_step,
    ProofStep,
  )
  assert (
    group_result.proof_step.inference_rule
    is not None
  )
  assert (
    group_result.proof_step.inference_rule.name
    == expected_rule_name
  )
  assert not (
    group_result.source_entry.key.startswith(
      "standard.toda.stable::"
    )
  )


def test_phase153_generic_concrete_recovery_keeps_stable_specialization_fallback():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=6,
        k=3,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert (
    group_result.source_entry.key
    == (
      "standard.toda.stable::"
      "nu_6_specialization"
    )
  )
  assert (
    group_result.source_entry.phase
    == "65"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.6"
  )


def test_phase153_generic_concrete_recovery_does_not_mutate_repository_roots():
  repository = (
    build_standard_production_proof_repository()
  )

  before = tuple(
    entry.key
    for entry in repository.entries()
  )

  for (
    n,
    k,
    _expected_key,
    _expected_phase,
    _expected_theorem,
    _expected_rule_name,
  ) in _CONCRETE_CASES:
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=n,
        k=k,
      ),
    )

  after = tuple(
    entry.key
    for entry in repository.entries()
  )

  assert before == (
    "standard.toda.prop56",
    "standard.toda.prop58",
    "standard.toda.prop511",
    "standard.toda.prop515",
  )
  assert after == before
'''


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      f"missing target file: {TARGET}"
    )

  text = TARGET.read_text(
    encoding="utf-8"
  )

  text = replace_once(
    text,
    OLD_IMPORT,
    NEW_IMPORT,
    "import update",
  )
  text = replace_once(
    text,
    OLD_STABLE_METADATA_END,
    NEW_STABLE_METADATA_END,
    "metadata insertion",
  )
  text = replace_once(
    text,
    INSERT_BEFORE_SPECIALIZED,
    (
      NEW_CONCRETE_FUNCTIONS
      + INSERT_BEFORE_SPECIALIZED
    ),
    "concrete recovery insertion",
  )
  text = replace_once(
    text,
    OLD_SELECTION,
    NEW_SELECTION,
    "selection priority update",
  )

  TARGET.write_text(
    text,
    encoding="utf-8",
  )

  TEST.write_text(
    TEST_TEXT,
    encoding="utf-8",
  )

  print(
    "Applied Phase 153 generic concrete proof-scope recovery."
  )
  print(
    "Changed: toda_calculation.py"
  )
  print(
    "Added: tests/test_phase153_generic_concrete_proof_scope_recovery.py"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
