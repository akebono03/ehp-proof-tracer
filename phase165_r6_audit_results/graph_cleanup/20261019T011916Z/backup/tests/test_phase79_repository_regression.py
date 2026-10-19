from dataclasses import dataclass

from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase79_cross_phase_repository import (
  build_phase79_7_data,
)


@dataclass(frozen=True)
class RepositoryDuplicateStatement:
  name: str


def _collect_ancestors(
  step,
):
  ancestors = []
  seen = set()
  stack = list(
    step.premises
  )

  while stack:
    current = stack.pop()

    current_id = id(
      current
    )

    if current_id in seen:
      continue

    seen.add(
      current_id
    )
    ancestors.append(
      current
    )
    stack.extend(
      current.premises
    )

  return tuple(
    ancestors
  )


def test_phase79_8_same_conclusion_retains_distinct_entries():
  repository = ProofRepository()

  first_root = ProofStep(
    conclusion=RepositoryDuplicateStatement(
      name="A",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_root = ProofStep(
    conclusion=RepositoryDuplicateStatement(
      name="B",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  shared_conclusion = (
    RepositoryDuplicateStatement(
      name="C",
    )
  )

  first_step = ProofStep(
    conclusion=shared_conclusion,
    premises=(
      first_root,
    ),
    rule=ProofRule.INFERENCE,
  )

  second_step = ProofStep(
    conclusion=shared_conclusion,
    premises=(
      second_root,
    ),
    rule=ProofRule.INFERENCE,
  )

  first_entry = ProofRepositoryEntry(
    key="phase79.duplicate.first",
    step=first_step,
    phase="79",
  )

  second_entry = ProofRepositoryEntry(
    key="phase79.duplicate.second",
    step=second_step,
    phase="79",
  )

  repository.register(
    first_entry
  )

  repository.register(
    second_entry
  )

  assert (
    first_step
    is not second_step
  )

  assert (
    repository.find_by_conclusion(
      shared_conclusion
    )
    == (
      first_entry,
      second_entry,
    )
  )


def test_phase79_8_same_conclusion_lookup_preserves_registration_order():
  repository = ProofRepository()

  shared_conclusion = (
    RepositoryDuplicateStatement(
      name="C",
    )
  )

  first_entry = ProofRepositoryEntry(
    key="phase79.duplicate.first",
    step=ProofStep(
      conclusion=shared_conclusion,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  second_entry = ProofRepositoryEntry(
    key="phase79.duplicate.second",
    step=ProofStep(
      conclusion=shared_conclusion,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  repository.register(
    first_entry
  )

  repository.register(
    second_entry
  )

  assert (
    repository.find_by_conclusion(
      shared_conclusion
    )
    == (
      first_entry,
      second_entry,
    )
  )


def test_phase79_8_same_conclusion_proofs_keep_distinct_dependencies():
  repository = ProofRepository()

  first_root = ProofStep(
    conclusion=RepositoryDuplicateStatement(
      name="A",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_root = ProofStep(
    conclusion=RepositoryDuplicateStatement(
      name="B",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  shared_conclusion = (
    RepositoryDuplicateStatement(
      name="C",
    )
  )

  first_entry = ProofRepositoryEntry(
    key="phase79.duplicate.first",
    step=ProofStep(
      conclusion=shared_conclusion,
      premises=(
        first_root,
      ),
      rule=ProofRule.INFERENCE,
    ),
  )

  second_entry = ProofRepositoryEntry(
    key="phase79.duplicate.second",
    step=ProofStep(
      conclusion=shared_conclusion,
      premises=(
        second_root,
      ),
      rule=ProofRule.INFERENCE,
    ),
  )

  repository.register(
    first_entry
  )

  repository.register(
    second_entry
  )

  assert (
    repository.dependencies(
      first_entry
    )
    == (
      first_root,
    )
  )

  assert (
    repository.dependencies(
      second_entry
    )
    == (
      second_root,
    )
  )

  assert (
    repository.dependencies(
      first_entry
    )[0]
    is first_root
  )

  assert (
    repository.dependencies(
      second_entry
    )[0]
    is second_root
  )


def test_phase79_8_same_step_different_metadata_does_not_mutate_proof():
  data = build_phase79_7_data()

  original_step = (
    data[
      "phase77_entry"
    ].step
  )

  original_premises = (
    original_step.premises
  )

  original_rule = (
    original_step.rule
  )

  original_inference_rule = (
    original_step.inference_rule
  )

  repository = ProofRepository()

  first_entry = ProofRepositoryEntry(
    key="phase77.lemma516",
    step=original_step,
    phase="77",
    theorem="Toda Lemma 5.16",
  )

  alias_entry = ProofRepositoryEntry(
    key="alias.phase77.lemma516",
    step=original_step,
    phase="999",
    theorem="Unrelated catalog label",
  )

  repository.register(
    first_entry
  )

  repository.register(
    alias_entry
  )

  assert (
    repository.get(
      first_entry.key
    ).step
    is original_step
  )

  assert (
    repository.get(
      alias_entry.key
    ).step
    is original_step
  )

  assert (
    original_step.premises
    is original_premises
  )

  assert (
    original_step.rule
    is original_rule
  )

  assert (
    original_step.inference_rule
    is original_inference_rule
  )


def test_phase79_8_phase77_applicability_is_unchanged_by_repository_retrieval():
  data = build_phase79_7_data()

  phase77 = data[
    "phase77"
  ]

  final_rule = (
    phase77[
      "data"
    ][
      "final_rule"
    ]
  )

  original_premises = (
    phase77[
      "final_step"
    ].premises
  )

  retrieved_premises = (
    data[
      "repository"
    ].dependencies(
      data[
        "phase77_entry"
      ]
    )
  )

  original_match = (
    find_inference_match(
      final_rule,
      original_premises,
    )
  )

  retrieved_match = (
    find_inference_match(
      final_rule,
      retrieved_premises,
    )
  )

  assert (
    original_match
    is not None
  )

  assert (
    retrieved_match
    is not None
  )

  assert (
    retrieved_premises
    is original_premises
  )


def test_phase79_8_phase77_applicability_ignores_repository_metadata():
  data = build_phase79_7_data()

  phase77 = data[
    "phase77"
  ]

  final_rule = (
    phase77[
      "data"
    ][
      "final_rule"
    ]
  )

  original_step = (
    data[
      "phase77_entry"
    ].step
  )

  repository = ProofRepository()

  alias_entry = ProofRepositoryEntry(
    key="alias.phase77.lemma516",
    step=original_step,
    phase="999",
    theorem="Unrelated catalog label",
  )

  repository.register(
    alias_entry
  )

  match = find_inference_match(
    final_rule,
    repository.dependencies(
      alias_entry
    ),
  )

  assert (
    match
    is not None
  )

  assert (
    alias_entry.phase
    == "999"
  )

  assert (
    alias_entry.theorem
    == "Unrelated catalog label"
  )


def test_phase79_8_repository_lookups_do_not_create_phase78_graph_nodes():
  data = build_phase79_7_data()

  repository = data[
    "repository"
  ]

  entry = data[
    "phase78_entry"
  ]

  before_ids = {
    id(
      step
    )
    for step in (
      data[
        "phase78"
      ][
        "ancestors"
      ]
    )
  }

  repository.get(
    entry.key
  )

  repository.find_by_phase(
    entry.phase
  )

  repository.find_by_theorem(
    entry.theorem
  )

  repository.find_by_conclusion(
    entry.step.conclusion
  )

  repository.find_by_statement_type(
    type(
      entry.step.conclusion
    )
  )

  repository.dependencies(
    entry
  )

  after_ids = {
    id(
      step
    )
    for step in _collect_ancestors(
      entry.step
    )
  }

  assert (
    after_ids
    == before_ids
  )


def test_phase79_8_phase76_retrieved_proof_remains_non_circular():
  data = build_phase79_7_data()

  final_step = (
    data[
      "repository"
    ].get(
      data[
        "phase76_entry"
      ].key
    ).step
  )

  ancestors = (
    _collect_ancestors(
      final_step
    )
  )

  assert all(
    ancestor
    is not final_step
    for ancestor in ancestors
  )

  assert all(
    ancestor.conclusion
    != final_step.conclusion
    for ancestor in ancestors
  )


def test_phase79_8_phase77_retrieved_proof_remains_non_circular():
  data = build_phase79_7_data()

  final_step = (
    data[
      "repository"
    ].get(
      data[
        "phase77_entry"
      ].key
    ).step
  )

  ancestors = (
    _collect_ancestors(
      final_step
    )
  )

  assert all(
    ancestor
    is not final_step
    for ancestor in ancestors
  )

  assert all(
    ancestor.conclusion
    != final_step.conclusion
    for ancestor in ancestors
  )


def test_phase79_8_phase78_retrieved_proof_remains_non_circular():
  data = build_phase79_7_data()

  final_step = (
    data[
      "repository"
    ].get(
      data[
        "phase78_entry"
      ].key
    ).step
  )

  ancestors = (
    _collect_ancestors(
      final_step
    )
  )

  assert all(
    ancestor
    is not final_step
    for ancestor in ancestors
  )

  assert all(
    ancestor.conclusion
    != final_step.conclusion
    for ancestor in ancestors
  )


def test_phase79_8_phase76_ancestry_is_unchanged_by_registration():
  data = build_phase79_7_data()

  expected_ids = (
    data[
      "phase76"
    ][
      "ancestor_ids"
    ]
  )

  retrieved_step = (
    data[
      "repository"
    ].get(
      data[
        "phase76_entry"
      ].key
    ).step
  )

  actual_ids = {
    id(
      step
    )
    for step in _collect_ancestors(
      retrieved_step
    )
  }

  assert (
    actual_ids
    == expected_ids
  )


def test_phase79_8_phase77_ancestry_is_unchanged_by_registration():
  data = build_phase79_7_data()

  expected_ids = {
    id(
      step
    )
    for step in (
      data[
        "phase77"
      ][
        "ancestors"
      ]
    )
  }

  retrieved_step = (
    data[
      "repository"
    ].get(
      data[
        "phase77_entry"
      ].key
    ).step
  )

  actual_ids = {
    id(
      step
    )
    for step in _collect_ancestors(
      retrieved_step
    )
  }

  assert (
    actual_ids
    == expected_ids
  )


def test_phase79_8_phase78_ancestry_is_unchanged_by_registration():
  data = build_phase79_7_data()

  expected_ids = {
    id(
      step
    )
    for step in (
      data[
        "phase78"
      ][
        "ancestors"
      ]
    )
  }

  retrieved_step = (
    data[
      "repository"
    ].get(
      data[
        "phase78_entry"
      ].key
    ).step
  )

  actual_ids = {
    id(
      step
    )
    for step in _collect_ancestors(
      retrieved_step
    )
  }

  assert (
    actual_ids
    == expected_ids
  )
