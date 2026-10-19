from functools import lru_cache

from expression import (
  GeneratorSymbol,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_element_lookup import (
  find_repository_entries_by_conclusion_generator,
)
from test_phase67_pi6_2_eta2_nu_prime import (
  build_phase67_6_data,
)
from test_phase68_pi7_3_nu_prime_eta6 import (
  build_phase68_3_data,
)
from test_phase70_pi8_3_nu_prime_eta6_squared import (
  build_phase70_3_data,
)
from theorem_facts import (
  EPSILON_3_TODA_MEMBERSHIP_FACT,
)


@lru_cache(maxsize=1)
def build_phase99_5_actual_repository():
  phase67 = build_phase67_6_data()
  phase68 = build_phase68_3_data()
  phase70 = build_phase70_3_data()

  theorem_step = (
    EPSILON_3_TODA_MEMBERSHIP_FACT
    .to_proof_step()
  )

  theorem_entry = ProofRepositoryEntry(
    key="phase24.epsilon3_toda_membership",
    step=theorem_step,
    phase="24",
    theorem="Toda bracket membership fact",
  )

  phase67_entry = ProofRepositoryEntry(
    key="phase67.pi6_2_eta2_nu_prime",
    step=phase67[
      "final_step"
    ],
    phase="67",
    theorem="Toda Lemma 5.7",
  )

  phase68_entry = ProofRepositoryEntry(
    key="phase68.pi7_3_nu_prime_eta6",
    step=phase68[
      "final_step"
    ],
    phase="68",
    theorem="Toda Proposition 5.8",
  )

  phase70_entry = ProofRepositoryEntry(
    key="phase70.pi8_3_nu_prime_eta6_squared",
    step=phase70[
      "final_step"
    ],
    phase="70",
    theorem="Toda Proposition 5.9",
  )

  repository = ProofRepository()

  for entry in (
    theorem_entry,
    phase67_entry,
    phase68_entry,
    phase70_entry,
  ):
    repository.register(
      entry
    )

  return {
    "repository": repository,
    "theorem_entry": theorem_entry,
    "phase67_entry": phase67_entry,
    "phase68_entry": phase68_entry,
    "phase70_entry": phase70_entry,
    "theorem_step": theorem_step,
    "phase67": phase67,
    "phase68": phase68,
    "phase70": phase70,
  }


def test_phase99_5_actual_repository_contains_four_representative_entries():
  data = build_phase99_5_actual_repository()

  assert data[
    "repository"
  ].entries() == (
    data[
      "theorem_entry"
    ],
    data[
      "phase67_entry"
    ],
    data[
      "phase68_entry"
    ],
    data[
      "phase70_entry"
    ],
  )


def test_phase99_5_actual_repository_nu_prime_lookup_returns_all_representatives():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_entries_by_conclusion_generator(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert result == (
    data[
      "theorem_entry"
    ],
    data[
      "phase67_entry"
    ],
    data[
      "phase68_entry"
    ],
    data[
      "phase70_entry"
    ],
  )


def test_phase99_5_actual_lookup_finds_nested_theorem_fact_nu_prime():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_entries_by_conclusion_generator(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert data[
    "theorem_entry"
  ] in result

  assert (
    data[
      "theorem_entry"
    ].step
    is data[
      "theorem_step"
    ]
  )

  assert (
    data[
      "theorem_entry"
    ].step.conclusion.bracket.second.expression.generator
    == GeneratorSymbol(
      family="ν",
      decoration="′",
    )
  )


def test_phase99_5_actual_lookup_finds_phase67_eta2_nu_prime_group_result():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_entries_by_conclusion_generator(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert data[
    "phase67_entry"
  ] in result

  generator = (
    data[
      "phase67_entry"
    ].step.conclusion.rhs.generator
  )

  assert generator.right is data[
    "phase67"
  ][
    "nu_prime"
  ]


def test_phase99_5_actual_lookup_finds_phase68_nu_prime_eta6_group_result():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_entries_by_conclusion_generator(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert data[
    "phase68_entry"
  ] in result

  assert (
    data[
      "phase68_entry"
    ].step.conclusion.rhs.generator
    == data[
      "phase68"
    ][
      "nu_prime_eta6"
    ]
  )


def test_phase99_5_actual_lookup_finds_phase70_nu_prime_eta6_squared_group_result():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_entries_by_conclusion_generator(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert data[
    "phase70_entry"
  ] in result

  assert (
    data[
      "phase70_entry"
    ].step.conclusion.rhs.generator
    == data[
      "phase70"
    ][
      "nu_prime_eta6_squared"
    ]
  )


def test_phase99_5_actual_lookup_rejects_plain_nu_for_nu_prime_representatives():
  data = build_phase99_5_actual_repository()

  result = (
    find_repository_entries_by_conclusion_generator(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
      ),
    )
  )

  assert data[
    "theorem_entry"
  ] not in result

  assert data[
    "phase67_entry"
  ] not in result

  assert data[
    "phase68_entry"
  ] not in result

  assert data[
    "phase70_entry"
  ] not in result


def test_phase99_5_actual_lookup_preserves_repository_and_step_identity():
  data = build_phase99_5_actual_repository()

  entries_before = (
    data[
      "repository"
    ].entries()
  )

  steps_before = tuple(
    entry.step
    for entry in entries_before
  )

  result = (
    find_repository_entries_by_conclusion_generator(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )
  )

  assert (
    data[
      "repository"
    ].entries()
    == entries_before
  )

  assert tuple(
    entry.step
    for entry in result
  ) == steps_before

  assert all(
    actual is expected
    for actual, expected in zip(
      (
        entry.step
        for entry in result
      ),
      steps_before,
    )
  )
