from typing import (
  get_type_hints,
)

from expression import (
  Expression,
  HomotopyElement,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  PrimaryComponent,
  PrimaryComponentMembershipStatement,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
)
from proof import (
  ProofRule,
  ProofStep,
)


def build_phase47_4a_membership(
  alpha_name="α",
):
  n = ScalarSymbol(
    name="n",
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  alpha = HomotopyElement(
    name=alpha_name,
    dimension=two_n_minus_one,
  )

  group = TodaPrimaryGroup(
    group_dimension=two_n_minus_one,
    sphere_dimension=n,
  )

  statement = (
    TodaPrimaryGroupMembershipStatement(
      element=alpha,
      group=group,
    )
  )

  return {
    "n": n,
    "two_n_minus_one": (
      two_n_minus_one
    ),
    "alpha": alpha,
    "group": group,
    "statement": statement,
  }


def test_phase47_4a_membership_element_uses_expression():
  type_hints = get_type_hints(
    TodaPrimaryGroupMembershipStatement
  )

  assert type_hints[
    "element"
  ] is Expression


def test_phase47_4a_membership_group_uses_toda_primary_group():
  type_hints = get_type_hints(
    TodaPrimaryGroupMembershipStatement
  )

  assert type_hints[
    "group"
  ] is TodaPrimaryGroup


def test_phase47_4a_alpha_is_losslessly_preserved():
  data = (
    build_phase47_4a_membership()
  )

  assert data[
    "statement"
  ].element == data[
    "alpha"
  ]


def test_phase47_4a_group_is_losslessly_preserved():
  data = (
    build_phase47_4a_membership()
  )

  assert data[
    "statement"
  ].group == data[
    "group"
  ]


def test_phase47_4a_represents_alpha_in_pi_two_n_minus_one_n():
  data = (
    build_phase47_4a_membership()
  )

  assert data[
    "statement"
  ] == TodaPrimaryGroupMembershipStatement(
    element=HomotopyElement(
      name="α",
      dimension=ScalarSum(
        left=ScalarProduct(
          left=2,
          right=data[
            "n"
          ],
        ),
        right=-1,
      ),
    ),
    group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=ScalarProduct(
          left=2,
          right=data[
            "n"
          ],
        ),
        right=-1,
      ),
      sphere_dimension=data[
        "n"
      ],
    ),
  )


def test_phase47_4a_same_membership_has_structural_equality():
  first = (
    build_phase47_4a_membership()
  )

  second = (
    build_phase47_4a_membership()
  )

  assert (
    first[
      "statement"
    ]
    == second[
      "statement"
    ]
  )


def test_phase47_4a_different_element_is_structurally_distinct():
  first = (
    build_phase47_4a_membership()
  )

  second = (
    build_phase47_4a_membership(
      alpha_name="α'",
    )
  )

  assert (
    first[
      "statement"
    ]
    != second[
      "statement"
    ]
  )


def test_phase47_4a_different_group_dimension_is_structurally_distinct():
  data = (
    build_phase47_4a_membership()
  )

  different = (
    TodaPrimaryGroupMembershipStatement(
      element=data[
        "alpha"
      ],
      group=TodaPrimaryGroup(
        group_dimension=ScalarSymbol(
          name="i",
        ),
        sphere_dimension=data[
          "n"
        ],
      ),
    )
  )

  assert (
    different
    != data[
      "statement"
    ]
  )


def test_phase47_4a_different_sphere_dimension_is_structurally_distinct():
  data = (
    build_phase47_4a_membership()
  )

  different = (
    TodaPrimaryGroupMembershipStatement(
      element=data[
        "alpha"
      ],
      group=TodaPrimaryGroup(
        group_dimension=data[
          "two_n_minus_one"
        ],
        sphere_dimension=ScalarSymbol(
          name="m",
        ),
      ),
    )
  )

  assert (
    different
    != data[
      "statement"
    ]
  )


def test_phase47_4a_toda_membership_is_distinct_from_primary_component_membership():
  data = (
    build_phase47_4a_membership()
  )

  primary_statement = (
    PrimaryComponentMembershipStatement(
      element=data[
        "alpha"
      ],
      component=PrimaryComponent(
        group_dimension=data[
          "two_n_minus_one"
        ],
        sphere_dimension=data[
          "n"
        ],
        prime=2,
      ),
    )
  )

  assert (
    data[
      "statement"
    ]
    != primary_statement
  )


def test_phase47_4a_primary_component_membership_type_contract_is_unchanged():
  type_hints = get_type_hints(
    PrimaryComponentMembershipStatement
  )

  assert type_hints[
    "element"
  ] is Expression

  assert type_hints[
    "component"
  ] is PrimaryComponent


def test_phase47_4a_statement_can_be_given_proof_step():
  data = (
    build_phase47_4a_membership()
  )

  step = ProofStep(
    conclusion=data[
      "statement"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert step.conclusion == (
    data[
      "statement"
    ]
  )

  assert step.premises == ()

  assert step.rule == (
    ProofRule.GIVEN
  )


def test_phase47_4a_statement_has_no_membership_solver():
  data = (
    build_phase47_4a_membership()
  )

  statement = data[
    "statement"
  ]

  assert not hasattr(
    statement,
    "evaluate",
  )

  assert not hasattr(
    statement,
    "is_member",
  )

  assert not hasattr(
    statement,
    "contains",
  )


def test_phase47_4a_statement_has_no_prop44_theorem_semantics():
  data = (
    build_phase47_4a_membership()
  )

  statement = data[
    "statement"
  ]

  assert not hasattr(
    statement,
    "toda_prop44",
  )

  assert not hasattr(
    statement,
    "theorem",
  )

  assert not hasattr(
    statement,
    "isomorphism",
  )


def test_phase47_4a_statement_does_not_validate_element_dimension():
  data = (
    build_phase47_4a_membership()
  )

  arbitrary_element = HomotopyElement(
    name="δ",
    dimension=100,
  )

  statement = (
    TodaPrimaryGroupMembershipStatement(
      element=arbitrary_element,
      group=data[
        "group"
      ],
    )
  )

  assert statement.element == (
    arbitrary_element
  )

  assert statement.group == (
    data[
      "group"
    ]
  )



