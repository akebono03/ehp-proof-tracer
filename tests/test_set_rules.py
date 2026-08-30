from algebra import (
  GroupElement,
  GroupMap,
  Subgroup,
  generated_subgroup_elements,
)
from expression import (
  MapApplication,
  MapSymbol,
  Zero,
  eta,
  nu,
)
from models import (
  AbelianGroup,
  GroupComponent,
)
from proof import (
  ExactnessStatement,
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  derive_inference_round_result,
  find_inference_match,
  relation_proof_step,
  run_inference_round,
  run_inference_until_stable_with_history,
)
from set_rules import (
  ImageSubgroupReference,
  KernelSubgroupReference,
  MembershipStatement,
  SubgroupEqualityStatement,
  SubsetStatement,
  exactness_implies_subgroup_equality_inference_rule,
  image_membership_statement,
  kernel_membership_implies_mapped_zero_inference_rule,
  kernel_membership_statement,
  mapped_zero_implies_kernel_membership_inference_rule,
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


def test_kernel_membership_statement():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  f = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  alpha = eta(3)

  statement = kernel_membership_statement(
    element=alpha,
    group_map=f,
  )

  assert statement == MembershipStatement(
    element=alpha,
    subgroup=f.kernel_subgroup(),
  )


def test_kernel_membership_statement_uses_existing_kernel_subgroup():
  source = make_cyclic_group(
    6,
    "a",
  )

  target = make_cyclic_group(
    6,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  alpha = eta(3)

  statement = kernel_membership_statement(
    element=alpha,
    group_map=f,
  )

  expected_kernel = f.kernel_subgroup()

  assert statement.subgroup == expected_kernel
  assert statement.subgroup.ambient_group == source

  assert {
    element.coefficients
    for element in statement.subgroup.elements
  } == {
    (0,),
    (3,),
  }


def test_kernel_membership_statement_distinguishes_kernel():
  group = make_cyclic_group(
    4,
    "a",
  )

  f = GroupMap(
    name="times2",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  g = GroupMap(
    name="zero",
    source=group,
    target=group,
    matrix=[
      [0],
    ],
  )

  alpha = eta(3)

  f_statement = kernel_membership_statement(
    element=alpha,
    group_map=f,
  )

  g_statement = kernel_membership_statement(
    element=alpha,
    group_map=g,
  )

  assert (
    f_statement
    != g_statement
  )

  assert (
    f_statement.subgroup
    != g_statement.subgroup
  )


def test_image_membership_statement():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    4,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  beta = nu(4)

  statement = image_membership_statement(
    element=beta,
    group_map=f,
  )

  assert statement == MembershipStatement(
    element=beta,
    subgroup=f.image_subgroup(),
  )


def test_image_membership_statement_uses_existing_image_subgroup():
  source = make_cyclic_group(
    6,
    "a",
  )

  target = make_cyclic_group(
    6,
    "b",
  )

  f = GroupMap(
    name="times2",
    source=source,
    target=target,
    matrix=[
      [2],
    ],
  )

  beta = nu(4)

  statement = image_membership_statement(
    element=beta,
    group_map=f,
  )

  expected_image = f.image_subgroup()

  assert statement.subgroup == expected_image
  assert statement.subgroup.ambient_group == target

  assert {
    element.coefficients
    for element in statement.subgroup.elements
  } == {
    (0,),
    (2,),
    (4,),
  }


def test_image_membership_statement_distinguishes_image():
  group = make_cyclic_group(
    4,
    "a",
  )

  f = GroupMap(
    name="times2",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  g = GroupMap(
    name="identity",
    source=group,
    target=group,
    matrix=[
      [1],
    ],
  )

  beta = nu(4)

  f_statement = image_membership_statement(
    element=beta,
    group_map=f,
  )

  g_statement = image_membership_statement(
    element=beta,
    group_map=g,
  )

  assert (
    f_statement
    != g_statement
  )

  assert (
    f_statement.subgroup
    != g_statement.subgroup
  )


def test_kernel_membership_implies_mapped_zero():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  group_map = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  map_symbol = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=kernel_membership_statement(
      element=alpha,
      group_map=group_map,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    kernel_membership_implies_mapped_zero_inference_rule(
      group_map=group_map,
      map_symbol=map_symbol,
    )
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == Relation(
    lhs=MapApplication(
      map=map_symbol,
      expression=alpha,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )


def test_kernel_membership_implies_mapped_zero_rejects_different_kernel():
  group = make_cyclic_group(
    4,
    "a",
  )

  target_map = GroupMap(
    name="times2",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  other_map = GroupMap(
    name="zero",
    source=group,
    target=group,
    matrix=[
      [0],
    ],
  )

  map_symbol = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=kernel_membership_statement(
      element=alpha,
      group_map=other_map,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    kernel_membership_implies_mapped_zero_inference_rule(
      group_map=target_map,
      map_symbol=map_symbol,
    )
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
    ),
  )

  assert match is None


def test_kernel_membership_implies_mapped_zero_uses_explicit_map_symbol():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  group_map = GroupMap(
    name="algebra-map-name",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  map_symbol = MapSymbol(
    name="proof-map-symbol",
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=kernel_membership_statement(
      element=alpha,
      group_map=group_map,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    kernel_membership_implies_mapped_zero_inference_rule(
      group_map=group_map,
      map_symbol=map_symbol,
    )
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == Relation(
    lhs=MapApplication(
      map=map_symbol,
      expression=alpha,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )


def test_kernel_membership_implies_mapped_zero_preserves_provenance():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  group_map = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  map_symbol = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  membership_step = ProofStep(
    conclusion=kernel_membership_statement(
      element=alpha,
      group_map=group_map,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    kernel_membership_implies_mapped_zero_inference_rule(
      group_map=group_map,
      map_symbol=map_symbol,
    )
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
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
  )


def test_mapped_zero_implies_kernel_membership():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  group_map = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  map_symbol = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  zero_step = relation_proof_step(
    Relation(
      lhs=MapApplication(
        map=map_symbol,
        expression=alpha,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    mapped_zero_implies_kernel_membership_inference_rule(
      group_map=group_map,
      map_symbol=map_symbol,
    )
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == MembershipStatement(
    element=alpha,
    subgroup=group_map.kernel_subgroup(),
  )


def test_mapped_zero_implies_kernel_membership_rejects_different_map_symbol():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  group_map = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  f_symbol = MapSymbol(
    name="f",
  )

  g_symbol = MapSymbol(
    name="g",
  )

  alpha = eta(3)

  zero_step = relation_proof_step(
    Relation(
      lhs=MapApplication(
        map=g_symbol,
        expression=alpha,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    mapped_zero_implies_kernel_membership_inference_rule(
      group_map=group_map,
      map_symbol=f_symbol,
    )
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
    ),
  )

  assert match is None


def test_mapped_zero_implies_kernel_membership_uses_explicit_group_map():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  group_map = GroupMap(
    name="algebra-map-name",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  map_symbol = MapSymbol(
    name="proof-map-symbol",
  )

  alpha = eta(3)

  zero_step = relation_proof_step(
    Relation(
      lhs=MapApplication(
        map=map_symbol,
        expression=alpha,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    mapped_zero_implies_kernel_membership_inference_rule(
      group_map=group_map,
      map_symbol=map_symbol,
    )
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == MembershipStatement(
    element=alpha,
    subgroup=group_map.kernel_subgroup(),
  )


def test_mapped_zero_implies_kernel_membership_preserves_provenance():
  source = make_cyclic_group(
    4,
    "a",
  )

  target = make_cyclic_group(
    2,
    "b",
  )

  group_map = GroupMap(
    name="f",
    source=source,
    target=target,
    matrix=[
      [1],
    ],
  )

  map_symbol = MapSymbol(
    name="f",
  )

  alpha = eta(3)

  zero_step = relation_proof_step(
    Relation(
      lhs=MapApplication(
        map=map_symbol,
        expression=alpha,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = (
    mapped_zero_implies_kernel_membership_inference_rule(
      group_map=group_map,
      map_symbol=map_symbol,
    )
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
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
    zero_step,
  )


def test_exactness_implies_subgroup_equality():
  group = make_cyclic_group(
    4,
    "a",
  )

  suspension_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  hopf_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  exactness_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=suspension_map,
      second_map=hopf_map,
      is_exact=True,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    exactness_implies_subgroup_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      exactness_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    SubgroupEqualityStatement(
      left=suspension_map.image_subgroup(),
      right=hopf_map.kernel_subgroup(),
    )
  )


def test_exactness_implies_subgroup_equality_rejects_nonexact_pair():
  group = make_cyclic_group(
    4,
    "a",
  )

  suspension_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  hopf_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  nonexact_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=suspension_map,
      second_map=hopf_map,
      is_exact=False,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    exactness_implies_subgroup_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      nonexact_step,
    ),
  )

  assert match is None


def test_exactness_implies_subgroup_equality_preserves_provenance():
  group = make_cyclic_group(
    4,
    "a",
  )

  suspension_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  hopf_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  exactness_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=suspension_map,
      second_map=hopf_map,
      is_exact=True,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    exactness_implies_subgroup_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      exactness_step,
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
    exactness_step,
  )


def test_phase14_exactness_image_kernel_membership_integration():
  group = make_cyclic_group(
    4,
    "a",
  )

  suspension_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  hopf_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  hopf_symbol = MapSymbol(
    name="H",
  )

  alpha = eta(3)

  exactness_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=suspension_map,
      second_map=hopf_map,
      is_exact=True,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  mapped_zero_step = relation_proof_step(
    Relation(
      lhs=MapApplication(
        map=hopf_symbol,
        expression=alpha,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  exactness_rule = (
    exactness_implies_subgroup_equality_inference_rule()
  )

  zero_to_kernel_rule = (
    mapped_zero_implies_kernel_membership_inference_rule(
      group_map=hopf_map,
      map_symbol=hopf_symbol,
    )
  )

  membership_equality_rule = (
    subgroup_equality_membership_propagation_inference_rule()
  )

  rules = (
    exactness_rule,
    zero_to_kernel_rule,
    membership_equality_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        exactness_step,
        mapped_zero_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  subgroup_equality = (
    SubgroupEqualityStatement(
      left=suspension_map.image_subgroup(),
      right=hopf_map.kernel_subgroup(),
    )
  )

  kernel_membership = MembershipStatement(
    element=alpha,
    subgroup=hopf_map.kernel_subgroup(),
  )

  image_membership = MembershipStatement(
    element=alpha,
    subgroup=suspension_map.image_subgroup(),
  )

  assert subgroup_equality in conclusions
  assert kernel_membership in conclusions
  assert image_membership in conclusions

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()


def test_image_and_kernel_roles_share_subgroup_value():
  group = make_cyclic_group(
    4,
    "a",
  )

  image_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  kernel_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  image_subgroup = (
    image_map.image_subgroup()
  )

  kernel_subgroup = (
    kernel_map.kernel_subgroup()
  )

  assert image_subgroup == kernel_subgroup

  assert {
    element.coefficients
    for element in image_subgroup.elements
  } == {
    (0,),
    (2,),
  }

  assert {
    element.coefficients
    for element in kernel_subgroup.elements
  } == {
    (0,),
    (2,),
  }


def test_image_and_kernel_membership_roles_collapse_under_equality():
  group = make_cyclic_group(
    4,
    "a",
  )

  image_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  kernel_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  alpha = eta(3)

  image_membership = image_membership_statement(
    element=alpha,
    group_map=image_map,
  )

  kernel_membership = kernel_membership_statement(
    element=alpha,
    group_map=kernel_map,
  )

  assert image_membership == kernel_membership

  assert (
    image_membership.subgroup
    == image_map.image_subgroup()
  )

  assert (
    kernel_membership.subgroup
    == kernel_map.kernel_subgroup()
  )


def test_subgroup_equality_membership_transport_is_duplicate_for_equal_roles():
  group = make_cyclic_group(
    4,
    "a",
  )

  image_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  kernel_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  alpha = eta(3)

  kernel_membership_step = ProofStep(
    conclusion=kernel_membership_statement(
      element=alpha,
      group_map=kernel_map,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  subgroup_equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=image_map.image_subgroup(),
      right=kernel_map.kernel_subgroup(),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_membership_propagation_inference_rule()
  )

  round_result = derive_inference_round_result(
    (
      rule,
    ),
    (
      kernel_membership_step,
      subgroup_equality_step,
    ),
  )

  assert round_result.new_steps == ()

  assert len(
    round_result.candidate_steps
  ) == 1

  assert len(
    round_result.duplicate_rejected_steps
  ) == 1

  candidate_step = (
    round_result.candidate_steps[0]
  )

  assert candidate_step.conclusion == (
    image_membership_statement(
      element=alpha,
      group_map=image_map,
    )
  )

  assert candidate_step.premises == (
    kernel_membership_step,
    subgroup_equality_step,
  )


def test_exactness_subgroup_equality_keeps_provenance_before_membership_collapse():
  group = make_cyclic_group(
    4,
    "a",
  )

  image_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  kernel_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  exactness_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=image_map,
      second_map=kernel_map,
      is_exact=True,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    exactness_implies_subgroup_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      exactness_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    SubgroupEqualityStatement(
      left=image_map.image_subgroup(),
      right=kernel_map.kernel_subgroup(),
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    exactness_step,
  )


def test_image_subgroup_reference():
  group = make_cyclic_group(
    4,
    "a",
  )

  group_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  reference = ImageSubgroupReference(
    group_map=group_map,
  )

  assert reference.group_map == group_map

  assert (
    reference.subgroup
    == group_map.image_subgroup()
  )

  assert {
    element.coefficients
    for element in reference.subgroup.elements
  } == {
    (0,),
    (2,),
  }


def test_kernel_subgroup_reference():
  group = make_cyclic_group(
    4,
    "a",
  )

  group_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  reference = KernelSubgroupReference(
    group_map=group_map,
  )

  assert reference.group_map == group_map

  assert (
    reference.subgroup
    == group_map.kernel_subgroup()
  )

  assert {
    element.coefficients
    for element in reference.subgroup.elements
  } == {
    (0,),
    (2,),
  }


def test_image_and_kernel_references_preserve_distinct_roles():
  group = make_cyclic_group(
    4,
    "a",
  )

  image_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  kernel_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  image_reference = ImageSubgroupReference(
    group_map=image_map,
  )

  kernel_reference = KernelSubgroupReference(
    group_map=kernel_map,
  )

  assert (
    image_reference.subgroup
    == kernel_reference.subgroup
  )

  assert (
    image_reference
    != kernel_reference
  )


def test_role_aware_membership_statements_remain_distinct():
  group = make_cyclic_group(
    4,
    "a",
  )

  image_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  kernel_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  alpha = eta(3)

  image_reference = ImageSubgroupReference(
    group_map=image_map,
  )

  kernel_reference = KernelSubgroupReference(
    group_map=kernel_map,
  )

  image_membership = MembershipStatement(
    element=alpha,
    subgroup=image_reference,
  )

  kernel_membership = MembershipStatement(
    element=alpha,
    subgroup=kernel_reference,
  )

  assert (
    image_reference.subgroup
    == kernel_reference.subgroup
  )

  assert (
    image_membership
    != kernel_membership
  )

  knowledge = (
    ProofStep(
      conclusion=image_membership,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=kernel_membership,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert len(
    {
      repr(step.conclusion)
      for step in knowledge
    }
  ) == 2





