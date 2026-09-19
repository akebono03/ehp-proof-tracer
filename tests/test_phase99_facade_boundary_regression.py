from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
)
from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_element_facade import (
  explore_repository_generator,
)
from test_phase67_pi6_2_eta2_nu_prime import (
  build_phase67_6_data,
)
from test_phase68_pi7_3_nu_prime_eta6 import (
  build_phase68_3_data,
)


@lru_cache(maxsize=1)
def build_phase99_26_data():
  phase67 = (
    build_phase67_6_data()
  )

  phase68 = (
    build_phase68_3_data()
  )

  nu_prime = phase67[
    "nu_prime"
  ]

  nu_prime_generator = (
    nu_prime.generator
  )

  assert nu_prime_generator is not None

  phase67_entry = ProofRepositoryEntry(
    key=(
      "phase67."
      "pi6_2_eta2_nu_prime"
    ),
    step=phase67[
      "final_step"
    ],
    phase="67",
    theorem="Toda Lemma 5.7",
  )

  phase68_entry = ProofRepositoryEntry(
    key=(
      "phase68."
      "pi7_3_nu_prime_eta6"
    ),
    step=phase68[
      "final_step"
    ],
    phase="68",
    theorem="Toda Proposition 5.8",
  )

  ordered_repository = (
    ProofRepository()
  )

  ordered_repository.register(
    phase68_entry
  )

  ordered_repository.register(
    phase67_entry
  )

  single_repository = (
    ProofRepository()
  )

  single_repository.register(
    phase67_entry
  )

  original_relation = (
    phase67[
      "final_step"
    ].conclusion
  )

  repeated_composition = Composition(
    left=nu_prime,
    right=nu_prime,
  )

  repeated_group = replace(
    original_relation.rhs,
    generator=(
      repeated_composition
    ),
  )

  repeated_relation = replace(
    original_relation,
    rhs=repeated_group,
  )

  repeated_step = ProofStep(
    conclusion=repeated_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  repeated_entry = (
    ProofRepositoryEntry(
      key=(
        "phase99_26."
        "same_entry_multiple_occurrence"
      ),
      step=repeated_step,
      phase="99-26",
      theorem=(
        "Phase 99-26 boundary fixture"
      ),
    )
  )

  repeated_repository = (
    ProofRepository()
  )

  repeated_repository.register(
    repeated_entry
  )

  unknown_generator = GeneratorSymbol(
    family="boundary_unknown",
    index=999,
  )

  return {
    "phase67": phase67,
    "phase68": phase68,
    "nu_prime_generator": (
      nu_prime_generator
    ),
    "phase67_entry": (
      phase67_entry
    ),
    "phase68_entry": (
      phase68_entry
    ),
    "ordered_repository": (
      ordered_repository
    ),
    "single_repository": (
      single_repository
    ),
    "repeated_entry": (
      repeated_entry
    ),
    "repeated_repository": (
      repeated_repository
    ),
    "unknown_generator": (
      unknown_generator
    ),
  }


def test_phase99_26_unknown_generator_returns_zero_occurrences():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "ordered_repository"
      ],
      data[
        "unknown_generator"
      ],
    )
  )

  assert (
    report
    .exploration
    .occurrences
    == ()
  )


def test_phase99_26_unknown_generator_returns_empty_role_views():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "ordered_repository"
      ],
      data[
        "unknown_generator"
      ],
    )
  )

  exploration = (
    report.exploration
  )

  assert (
    exploration
    .group_generator_occurrences
    == ()
  )

  assert (
    exploration
    .composition_left_occurrences
    == ()
  )

  assert (
    exploration
    .composition_right_occurrences
    == ()
  )

  assert (
    exploration
    .toda_bracket_occurrences
    == ()
  )

  assert (
    exploration
    .map_input_occurrences
    == ()
  )


def test_phase99_26_unknown_generator_markdown_reports_zero():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "ordered_repository"
      ],
      data[
        "unknown_generator"
      ],
    )
  )

  assert (
    "Occurrences: 0"
    in report.markdown
  )


def test_phase99_26_unknown_generator_does_not_mutate_repository():
  data = build_phase99_26_data()

  repository = data[
    "ordered_repository"
  ]

  before = (
    repository.entries()
  )

  explore_repository_generator(
    repository,
    data[
      "unknown_generator"
    ],
  )

  assert (
    repository.entries()
    == before
  )


def test_phase99_26_single_repository_returns_exactly_one_occurrence():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "single_repository"
      ],
      data[
        "nu_prime_generator"
      ],
    )
  )

  occurrences = (
    report
    .exploration
    .occurrences
  )

  assert len(
    occurrences
  ) == 1

  assert (
    occurrences[
      0
    ].entry
    is data[
      "phase67_entry"
    ]
  )


def test_phase99_26_single_repository_preserves_composition_right_role():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "single_repository"
      ],
      data[
        "nu_prime_generator"
      ],
    )
  )

  exploration = (
    report.exploration
  )

  assert len(
    exploration
    .composition_right_occurrences
  ) == 1

  assert (
    exploration
    .composition_left_occurrences
    == ()
  )


def test_phase99_26_same_entry_preserves_two_structural_occurrences():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "repeated_repository"
      ],
      data[
        "nu_prime_generator"
      ],
    )
  )

  occurrences = (
    report
    .exploration
    .occurrences
  )

  assert len(
    occurrences
  ) == 2

  assert all(
    occurrence.entry
    is data[
      "repeated_entry"
    ]
    for occurrence in occurrences
  )

  assert (
    occurrences[
      0
    ].path
    != occurrences[
      1
    ].path
  )


def test_phase99_26_same_entry_preserves_left_and_right_views():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "repeated_repository"
      ],
      data[
        "nu_prime_generator"
      ],
    )
  )

  exploration = (
    report.exploration
  )

  assert len(
    exploration
    .composition_left_occurrences
  ) == 1

  assert len(
    exploration
    .composition_right_occurrences
  ) == 1

  assert (
    exploration
    .composition_left_occurrences[
      0
    ].path
    != exploration
    .composition_right_occurrences[
      0
    ].path
  )


def test_phase99_26_repository_registration_order_is_preserved():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "ordered_repository"
      ],
      data[
        "nu_prime_generator"
      ],
    )
  )

  assert tuple(
    occurrence.entry.key
    for occurrence in (
      report
      .exploration
      .occurrences
    )
  ) == (
    (
      "phase68."
      "pi7_3_nu_prime_eta6"
    ),
    (
      "phase67."
      "pi6_2_eta2_nu_prime"
    ),
  )


def test_phase99_26_presentation_preserves_repository_order():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "ordered_repository"
      ],
      data[
        "nu_prime_generator"
      ],
    )
  )

  assert tuple(
    occurrence
    .source_occurrence
    .entry
    .key
    for occurrence in (
      report
      .presentation
      .group_generator_occurrences
    )
  ) == (
    (
      "phase68."
      "pi7_3_nu_prime_eta6"
    ),
    (
      "phase67."
      "pi6_2_eta2_nu_prime"
    ),
  )


def test_phase99_26_markdown_preserves_repository_order():
  data = build_phase99_26_data()

  report = (
    explore_repository_generator(
      data[
        "ordered_repository"
      ],
      data[
        "nu_prime_generator"
      ],
    )
  )

  phase68_position = (
    report.markdown.find(
      "Phase: 68"
    )
  )

  phase67_position = (
    report.markdown.find(
      "Phase: 67"
    )
  )

  assert (
    phase68_position
    != -1
  )

  assert (
    phase67_position
    != -1
  )

  assert (
    phase68_position
    < phase67_position
  )


def test_phase99_26_facade_does_not_mutate_ordered_repository():
  data = build_phase99_26_data()

  repository = data[
    "ordered_repository"
  ]

  before = (
    repository.entries()
  )

  explore_repository_generator(
    repository,
    data[
      "nu_prime_generator"
    ],
  )

  assert (
    repository.entries()
    == before
  )
