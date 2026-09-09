from functools import lru_cache

from expression import (
  Composition,
  MapApplication,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  ProofRule,
)
from test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)
from toda_rules import (
  TodaHopfInvariantSurjectiveStatement,
)


@lru_cache(maxsize=1)
def build_phase68_2_data():
  phase65_3 = (
    build_phase65_3_data()
  )

  return {
    "phase65_3": phase65_3,
    "equation57_step": (
      phase65_3[
        "equation57_step"
      ]
    ),
    "hopf_surjective_step": (
      phase65_3[
        "hopf_surjective_step"
      ]
    ),
    "nu_prime": phase65_3[
      "nu_prime"
    ],
    "eta_5": phase65_3[
      "eta_5"
    ],
    "eta_6": phase65_3[
      "eta_6"
    ],
  }


def test_phase68_2_reuses_derived_toda57():
  data = build_phase68_2_data()

  assert (
    data[
      "equation57_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_2_toda57_is_h_nu_prime_eta6():
  data = build_phase68_2_data()

  relation = (
    data[
      "equation57_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == MapApplication(
      map=EHP_H_MAP,
      expression=Composition(
        left=data[
          "nu_prime"
        ],
        right=data[
          "eta_6"
        ],
      ),
    )
  )


def test_phase68_2_toda57_value_is_eta5_squared():
  data = build_phase68_2_data()

  assert (
    data[
      "equation57_step"
    ].conclusion.rhs
    == Composition(
      left=data[
        "eta_5"
      ],
      right=data[
        "eta_6"
      ],
    )
  )


def test_phase68_2_reuses_derived_hopf_surjectivity():
  data = build_phase68_2_data()

  step = data[
    "hopf_surjective_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaHopfInvariantSurjectiveStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase68_2_hopf_surjectivity_uses_toda57():
  data = build_phase68_2_data()

  assert (
    data[
      "hopf_surjective_step"
    ].premises[
      0
    ]
    is data[
      "equation57_step"
    ]
  )


def test_phase68_2_does_not_reintroduce_toda57_as_given():
  data = build_phase68_2_data()

  assert (
    data[
      "equation57_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "hopf_surjective_step"
    ].rule
    != ProofRule.GIVEN
  )


