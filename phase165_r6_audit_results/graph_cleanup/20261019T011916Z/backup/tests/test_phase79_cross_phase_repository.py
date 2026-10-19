from functools import lru_cache

from proof import (
  ProofRule,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase76_applicability_provenance import (
  build_phase76_5_data,
)
from test_phase77_applicability_provenance import (
  build_phase77_6_data,
)
from test_phase78_stable_g0_to_g7_integration import (
  build_phase78_11_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaLemma516BracketSumContainmentStatement,
  TodaStableG0ToG7Statement,
)


@lru_cache(maxsize=1)
def build_phase79_7_data():
  phase76 = (
    build_phase76_5_data()
  )

  phase77 = (
    build_phase77_6_data()
  )

  phase78 = (
    build_phase78_11_data()
  )

  repository = ProofRepository()

  phase76_entry = ProofRepositoryEntry(
    key="phase76.delta_iota17",
    step=phase76[
      "final_step"
    ],
    phase="76",
    theorem="Toda Equation (5.16)",
  )

  phase77_entry = ProofRepositoryEntry(
    key="phase77.lemma516",
    step=phase77[
      "final_step"
    ],
    phase="77",
    theorem="Toda Lemma 5.16",
  )

  phase78_entry = ProofRepositoryEntry(
    key="phase78.stable_g0_to_g7",
    step=phase78[
      "aggregate_step"
    ],
    phase="78",
    theorem=(
      "Stable G_0 through G_7 integration"
    ),
  )

  for entry in (
    phase76_entry,
    phase77_entry,
    phase78_entry,
  ):
    repository.register(
      entry
    )

  return {
    "repository": repository,
    "phase76": phase76,
    "phase77": phase77,
    "phase78": phase78,
    "phase76_entry": phase76_entry,
    "phase77_entry": phase77_entry,
    "phase78_entry": phase78_entry,
  }


def test_phase79_7_registers_three_representative_cross_phase_entries():
  data = build_phase79_7_data()
  repository = data[
    "repository"
  ]

  assert (
    repository.get(
      "phase76.delta_iota17"
    )
    is data[
      "phase76_entry"
    ]
  )

  assert (
    repository.get(
      "phase77.lemma516"
    )
    is data[
      "phase77_entry"
    ]
  )

  assert (
    repository.get(
      "phase78.stable_g0_to_g7"
    )
    is data[
      "phase78_entry"
    ]
  )


def test_phase79_7_retrieval_preserves_original_proof_step_identity():
  data = build_phase79_7_data()
  repository = data[
    "repository"
  ]

  assert (
    repository.get(
      "phase76.delta_iota17"
    ).step
    is data[
      "phase76"
    ][
      "final_step"
    ]
  )

  assert (
    repository.get(
      "phase77.lemma516"
    ).step
    is data[
      "phase77"
    ][
      "final_step"
    ]
  )

  assert (
    repository.get(
      "phase78.stable_g0_to_g7"
    ).step
    is data[
      "phase78"
    ][
      "aggregate_step"
    ]
  )


def test_phase79_7_find_by_phase_crosses_statement_kinds():
  data = build_phase79_7_data()
  repository = data[
    "repository"
  ]

  assert (
    repository.find_by_phase(
      "76"
    )
    == (
      data[
        "phase76_entry"
      ],
    )
  )

  assert (
    repository.find_by_phase(
      "77"
    )
    == (
      data[
        "phase77_entry"
      ],
    )
  )

  assert (
    repository.find_by_phase(
      "78"
    )
    == (
      data[
        "phase78_entry"
      ],
    )
  )


def test_phase79_7_find_by_theorem_crosses_phases():
  data = build_phase79_7_data()
  repository = data[
    "repository"
  ]

  assert (
    repository.find_by_theorem(
      "Toda Equation (5.16)"
    )
    == (
      data[
        "phase76_entry"
      ],
    )
  )

  assert (
    repository.find_by_theorem(
      "Toda Lemma 5.16"
    )
    == (
      data[
        "phase77_entry"
      ],
    )
  )

  assert (
    repository.find_by_theorem(
      "Stable G_0 through G_7 integration"
    )
    == (
      data[
        "phase78_entry"
      ],
    )
  )


def test_phase79_7_find_by_conclusion_returns_exact_entries():
  data = build_phase79_7_data()
  repository = data[
    "repository"
  ]

  assert (
    repository.find_by_conclusion(
      data[
        "phase76"
      ][
        "final_step"
      ].conclusion
    )
    == (
      data[
        "phase76_entry"
      ],
    )
  )

  assert (
    repository.find_by_conclusion(
      data[
        "phase77"
      ][
        "final_step"
      ].conclusion
    )
    == (
      data[
        "phase77_entry"
      ],
    )
  )

  assert (
    repository.find_by_conclusion(
      data[
        "phase78"
      ][
        "aggregate_step"
      ].conclusion
    )
    == (
      data[
        "phase78_entry"
      ],
    )
  )


def test_phase79_7_find_phase76_by_statement_type():
  data = build_phase79_7_data()

  assert (
    data[
      "repository"
    ].find_by_statement_type(
      TodaDeltaImageUpToSignStatement
    )
    == (
      data[
        "phase76_entry"
      ],
    )
  )


def test_phase79_7_find_phase77_by_statement_type():
  data = build_phase79_7_data()

  assert (
    data[
      "repository"
    ].find_by_statement_type(
      TodaLemma516BracketSumContainmentStatement
    )
    == (
      data[
        "phase77_entry"
      ],
    )
  )


def test_phase79_7_find_phase78_by_statement_type():
  data = build_phase79_7_data()

  assert (
    data[
      "repository"
    ].find_by_statement_type(
      TodaStableG0ToG7Statement
    )
    == (
      data[
        "phase78_entry"
      ],
    )
  )


def test_phase79_7_phase76_dependencies_are_exact_direct_premises():
  data = build_phase79_7_data()

  dependencies = (
    data[
      "repository"
    ].dependencies(
      data[
        "phase76_entry"
      ]
    )
  )

  assert dependencies == (
    data[
      "phase76"
    ][
      "pi17_17_step"
    ],
    data[
      "phase76"
    ][
      "delta_image_step"
    ],
  )

  assert (
    dependencies[0]
    is data[
      "phase76"
    ][
      "pi17_17_step"
    ]
  )

  assert (
    dependencies[1]
    is data[
      "phase76"
    ][
      "delta_image_step"
    ]
  )


def test_phase79_7_phase77_dependencies_are_exact_direct_premises():
  data = build_phase79_7_data()

  dependencies = (
    data[
      "repository"
    ].dependencies(
      data[
        "phase77_entry"
      ]
    )
  )

  assert dependencies == (
    data[
      "phase77"
    ][
      "bracket_sum_step"
    ],
    data[
      "phase77"
    ][
      "composition_step"
    ],
  )

  assert (
    dependencies[0]
    is data[
      "phase77"
    ][
      "bracket_sum_step"
    ]
  )

  assert (
    dependencies[1]
    is data[
      "phase77"
    ][
      "composition_step"
    ]
  )


def test_phase79_7_phase78_dependencies_are_exact_eight_branches():
  data = build_phase79_7_data()

  dependencies = (
    data[
      "repository"
    ].dependencies(
      data[
        "phase78_entry"
      ]
    )
  )

  assert (
    dependencies
    == data[
      "phase78"
    ][
      "premise_steps"
    ]
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      dependencies,
      data[
        "phase78"
      ][
        "premise_steps"
      ],
    )
  )


def test_phase79_7_unregistered_direct_premises_remain_retrievable():
  data = build_phase79_7_data()
  repository = data[
    "repository"
  ]

  registered_steps = (
    data[
      "phase76_entry"
    ].step,
    data[
      "phase77_entry"
    ].step,
    data[
      "phase78_entry"
    ].step,
  )

  for entry in (
    data[
      "phase76_entry"
    ],
    data[
      "phase77_entry"
    ],
    data[
      "phase78_entry"
    ],
  ):
    dependencies = (
      repository.dependencies(
        entry
      )
    )

    assert dependencies

    assert all(
      dependency
      not in registered_steps
      for dependency in dependencies
    )


def test_phase79_7_repository_does_not_replace_original_premise_tuples():
  data = build_phase79_7_data()
  repository = data[
    "repository"
  ]

  for entry in (
    data[
      "phase76_entry"
    ],
    data[
      "phase77_entry"
    ],
    data[
      "phase78_entry"
    ],
  ):
    assert (
      repository.dependencies(
        entry
      )
      is entry.step.premises
    )


def test_phase79_7_registered_final_steps_remain_inference():
  data = build_phase79_7_data()

  assert all(
    entry.step.rule
    == ProofRule.INFERENCE
    for entry in (
      data[
        "phase76_entry"
      ],
      data[
        "phase77_entry"
      ],
      data[
        "phase78_entry"
      ],
    )
  )


