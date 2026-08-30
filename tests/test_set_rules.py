from algebra import (
  GroupElement,
  Subgroup,
  generated_subgroup_elements,
)
from expression import (
  eta,
  nu,
)
from models import (
  AbelianGroup,
  GroupComponent,
)
from proof import (
  ProofRule,
  ProofStep,
  apply_inference_match,
  find_inference_match,
  run_inference_round,
)
from set_rules import (
  MembershipStatement,
  SubgroupEqualityStatement,
  SubsetStatement,
  membership_subset_propagation_inference_rule,
  subgroup_equality_membership_propagation_inference_rule,
)


def make_cyclic_group(
  order,
  generator,
):
  return AbelianGroup(
    n=0,
    k=0,
    components=[
      GroupComponent(
        id=0,
        order=order,
        generator=generator,
        element=[],
        gen_coe=[],
      )
    ],
  )


def make_subgroup(
  group,
  generators,
):
  generators = tuple(
    GroupElement(
      group,
      coefficients,
    )
    for coefficients in generators
  )

  elements = generated_subgroup_elements(
    group,
    generators,
  )

  return Subgroup(
    ambient_group=group,
    elements=elements,
    generators=generators,
  )


def test_membership_statement():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)

  statement = MembershipStatement(
    element=alpha,
    subgroup=subgroup,
  )

  assert statement.element == alpha
  assert statement.subgroup == subgroup


def test_membership_statement_has_structural_equality():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)

  first = MembershipStatement(
    element=alpha,
    subgroup=subgroup,
  )

  second = MembershipStatement(
    element=alpha,
    subgroup=subgroup,
  )

  assert first == second


def test_membership_statement_distinguishes_element():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  alpha_statement = MembershipStatement(
    element=alpha,
    subgroup=subgroup,
  )

  beta_statement = MembershipStatement(
    element=beta,
    subgroup=subgroup,
  )

  assert alpha_statement != beta_statement


def test_membership_statement_distinguishes_subgroup():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup_two = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  alpha = eta(3)

  subgroup_two_statement = MembershipStatement(
    element=alpha,
    subgroup=subgroup_two,
  )

  whole_group_statement = MembershipStatement(
    element=alpha,
    subgroup=whole_group,
  )

  assert (
    subgroup_two_statement
    != whole_group_statement
  )


def test_subset_statement():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  statement = SubsetStatement(
    subset=subgroup,
    superset=whole_group,
  )

  assert statement.subset == subgroup
  assert statement.superset == whole_group


def test_subset_statement_has_structural_equality():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  first = SubsetStatement(
    subset=subgroup,
    superset=whole_group,
  )

  second = SubsetStatement(
    subset=subgroup,
    superset=whole_group,
  )

  assert first == second


def test_subset_statement_distinguishes_subset():
  group = make_cyclic_group(
    4,
    "a",
  )

  trivial_subgroup = make_subgroup(
    group,
    [],
  )

  subgroup_two = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  trivial_statement = SubsetStatement(
    subset=trivial_subgroup,
    superset=whole_group,
  )

  subgroup_two_statement = SubsetStatement(
    subset=subgroup_two,
    superset=whole_group,
  )

  assert (
    trivial_statement
    != subgroup_two_statement
  )


def test_subset_statement_distinguishes_superset():
  group = make_cyclic_group(
    4,
    "a",
  )

  trivial_subgroup = make_subgroup(
    group,
    [],
  )

  subgroup_two = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  subgroup_statement = SubsetStatement(
    subset=trivial_subgroup,
    superset=subgroup_two,
  )

  whole_group_statement = SubsetStatement(
    subset=trivial_subgroup,
    superset=whole_group,
  )

  assert (
    subgroup_statement
    != whole_group_statement
  )


def test_membership_subset_propagation():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=subgroup,
      superset=whole_group,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    membership_subset_propagation_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
      subset_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == MembershipStatement(
    element=alpha,
    subgroup=whole_group,
  )


def test_membership_subset_propagation_requires_matching_subgroup():
  group = make_cyclic_group(
    4,
    "a",
  )

  trivial_subgroup = make_subgroup(
    group,
    [],
  )

  subgroup_two = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=trivial_subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  unrelated_subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=subgroup_two,
      superset=whole_group,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    membership_subset_propagation_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
      unrelated_subset_step,
    ),
  )

  assert match is None


def test_membership_subset_propagation_uses_bound_element_and_superset():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  alpha = eta(3)
  beta = nu(4)

  alpha_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_step = ProofStep(
    conclusion=MembershipStatement(
      element=beta,
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=subgroup,
      superset=whole_group,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    membership_subset_propagation_inference_rule()
  )

  new_steps = run_inference_round(
    (
      rule,
    ),
    (
      alpha_step,
      beta_step,
      subset_step,
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in new_steps
  )

  assert MembershipStatement(
    element=alpha,
    subgroup=whole_group,
  ) in conclusions

  assert MembershipStatement(
    element=beta,
    subgroup=whole_group,
  ) in conclusions


def test_membership_subset_propagation_preserves_provenance():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=subgroup,
      superset=whole_group,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    membership_subset_propagation_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
      subset_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    membership_step,
    subset_step,
  )


def test_subgroup_equality_statement():
  group = make_cyclic_group(
    4,
    "a",
  )

  left = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  right = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  statement = SubgroupEqualityStatement(
    left=left,
    right=right,
  )

  assert statement.left == left
  assert statement.right == right


def test_subgroup_equality_statement_has_structural_equality():
  group = make_cyclic_group(
    4,
    "a",
  )

  left = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  right = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  first = SubgroupEqualityStatement(
    left=left,
    right=right,
  )

  second = SubgroupEqualityStatement(
    left=left,
    right=right,
  )

  assert first == second


def test_subgroup_equality_membership_propagation():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  equal_subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=subgroup,
      right=equal_subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_membership_propagation_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == MembershipStatement(
    element=alpha,
    subgroup=equal_subgroup,
  )


def test_subgroup_equality_membership_propagation_reverse_direction():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  equal_subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=equal_subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=subgroup,
      right=equal_subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_membership_propagation_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == MembershipStatement(
    element=alpha,
    subgroup=subgroup,
  )


def test_subgroup_equality_membership_propagation_rejects_unrelated_subgroup():
  group = make_cyclic_group(
    4,
    "a",
  )

  trivial_subgroup = make_subgroup(
    group,
    [],
  )

  subgroup_two = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=trivial_subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=subgroup_two,
      right=whole_group,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_membership_propagation_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
      equality_step,
    ),
  )

  assert match is None


def test_subgroup_equality_membership_propagation_preserves_provenance():
  group = make_cyclic_group(
    4,
    "a",
  )

  subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  equal_subgroup = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=subgroup,
      right=equal_subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_membership_propagation_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    membership_step,
    equality_step,
  )







