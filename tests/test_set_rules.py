from algebra import (
  GroupElement,
  GroupMap,
  Subgroup,
  generated_subgroup_elements,
)
from expression import (
  MapApplication,
  MapSymbol,
  Multiple,
  Sum,
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
  Coset,
  ImageSubgroupReference,
  KernelSubgroupReference,
  MembershipStatement,
  ModuloStatement,
  SubgroupEqualityStatement,
  SubsetStatement,
  difference_membership_implies_modulo_inference_rule,
  exactness_implies_subgroup_equality_inference_rule,
  image_membership_statement,
  kernel_membership_implies_mapped_zero_inference_rule,
  kernel_membership_statement,
  mapped_zero_implies_kernel_membership_inference_rule,
  membership_subset_propagation_inference_rule,
  modulo_implies_difference_membership_inference_rule,
  mutual_subset_implies_subgroup_equality_inference_rule,
  subgroup_equality_implies_subset_inference_rule,
  subgroup_equality_membership_propagation_inference_rule,
  subgroup_equality_symmetry_inference_rule,
  subgroup_equality_transitivity_inference_rule,
  subset_transitivity_inference_rule,
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
      left=ImageSubgroupReference(
        group_map=suspension_map,
      ),
      right=KernelSubgroupReference(
        group_map=hopf_map,
      ),
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


def test_phase14_exactness_bridges_role_aware_kernel_membership_to_image_membership():
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
      left=ImageSubgroupReference(
        group_map=suspension_map,
      ),
      right=KernelSubgroupReference(
        group_map=hopf_map,
      ),
    )
  )

  kernel_membership = (
    kernel_membership_statement(
      element=alpha,
      group_map=hopf_map,
    )
  )

  image_membership = (
    image_membership_statement(
      element=alpha,
      group_map=suspension_map,
    )
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


def test_legacy_image_and_kernel_membership_values_collapse_under_equality():
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

  image_membership = MembershipStatement(
    element=alpha,
    subgroup=image_map.image_subgroup(),
  )

  kernel_membership = MembershipStatement(
    element=alpha,
    subgroup=kernel_map.kernel_subgroup(),
  )

  assert (
    image_membership
    == kernel_membership
  )


def test_legacy_subgroup_equality_membership_transport_is_duplicate_for_equal_values():
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

  kernel_membership = MembershipStatement(
    element=alpha,
    subgroup=kernel_map.kernel_subgroup(),
  )

  image_membership = MembershipStatement(
    element=alpha,
    subgroup=image_map.image_subgroup(),
  )

  kernel_membership_step = ProofStep(
    conclusion=kernel_membership,
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

  assert (
    candidate_step.conclusion
    == image_membership
  )

  assert candidate_step.premises == (
    kernel_membership_step,
    subgroup_equality_step,
  )


def test_exactness_role_aware_subgroup_equality_preserves_provenance():
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
      left=ImageSubgroupReference(
        group_map=image_map,
      ),
      right=KernelSubgroupReference(
        group_map=kernel_map,
      ),
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
    subgroup=KernelSubgroupReference(
      group_map=f,
    ),
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

  assert isinstance(
    statement.subgroup,
    KernelSubgroupReference,
  )

  assert statement.subgroup.group_map == f

  assert (
    statement.subgroup.subgroup
    == expected_kernel
  )

  assert (
    statement.subgroup.subgroup.ambient_group
    == source
  )

  assert {
    element.coefficients
    for element
    in statement.subgroup.subgroup.elements
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

  assert (
    f_statement.subgroup.subgroup
    != g_statement.subgroup.subgroup
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
    subgroup=ImageSubgroupReference(
      group_map=f,
    ),
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

  assert isinstance(
    statement.subgroup,
    ImageSubgroupReference,
  )

  assert statement.subgroup.group_map == f

  assert (
    statement.subgroup.subgroup
    == expected_image
  )

  assert (
    statement.subgroup.subgroup.ambient_group
    == target
  )

  assert {
    element.coefficients
    for element
    in statement.subgroup.subgroup.elements
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

  assert (
    f_statement.subgroup.subgroup
    != g_statement.subgroup.subgroup
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

  assert derived_step.conclusion == (
    kernel_membership_statement(
      element=alpha,
      group_map=group_map,
    )
  )


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

  assert derived_step.conclusion == (
    kernel_membership_statement(
      element=alpha,
      group_map=group_map,
    )
  )


def test_role_aware_membership_helpers_keep_image_and_kernel_roles_distinct():
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

  image_membership = (
    image_membership_statement(
      element=alpha,
      group_map=image_map,
    )
  )

  kernel_membership = (
    kernel_membership_statement(
      element=alpha,
      group_map=kernel_map,
    )
  )

  assert (
    image_membership.subgroup.subgroup
    == kernel_membership.subgroup.subgroup
  )

  assert (
    image_membership
    != kernel_membership
  )

  assert isinstance(
    image_membership.subgroup,
    ImageSubgroupReference,
  )

  assert isinstance(
    kernel_membership.subgroup,
    KernelSubgroupReference,
  )


def test_subset_statement_accepts_role_aware_subgroup_terms():
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

  statement = SubsetStatement(
    subset=kernel_reference,
    superset=image_reference,
  )

  assert statement.subset == kernel_reference
  assert statement.superset == image_reference

  assert (
    statement.subset.subgroup
    == statement.superset.subgroup
  )

  assert (
    statement.subset
    != statement.superset
  )


def test_subgroup_equality_statement_accepts_role_aware_subgroup_terms():
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

  statement = SubgroupEqualityStatement(
    left=image_reference,
    right=kernel_reference,
  )

  assert statement.left == image_reference
  assert statement.right == kernel_reference

  assert (
    statement.left.subgroup
    == statement.right.subgroup
  )

  assert (
    statement.left
    != statement.right
  )


def test_role_aware_membership_subset_propagation():
  group = make_cyclic_group(
    4,
    "a",
  )

  kernel_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  image_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  alpha = eta(3)

  kernel_reference = KernelSubgroupReference(
    group_map=kernel_map,
  )

  image_reference = ImageSubgroupReference(
    group_map=image_map,
  )

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=kernel_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=kernel_reference,
      superset=image_reference,
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

  assert derived_step.conclusion == (
    MembershipStatement(
      element=alpha,
      subgroup=image_reference,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    membership_step,
    subset_step,
  )


def test_role_aware_membership_subset_propagation_rejects_same_value_different_role():
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

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  alpha = eta(3)

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

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=image_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=kernel_reference,
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

  assert match is None


def test_role_aware_subgroup_equality_membership_propagation():
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

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=kernel_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=image_reference,
      right=kernel_reference,
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

  assert derived_step.conclusion == (
    MembershipStatement(
      element=alpha,
      subgroup=image_reference,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    membership_step,
    equality_step,
  )


def test_role_aware_subgroup_equality_membership_propagation_rejects_same_value_different_role():
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

  whole_group = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  alpha = eta(3)

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

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=image_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=kernel_reference,
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


def test_subgroup_equality_symmetry():
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

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=image_reference,
      right=kernel_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_symmetry_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    SubgroupEqualityStatement(
      left=kernel_reference,
      right=image_reference,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    equality_step,
  )


def test_subgroup_equality_transitivity():
  group = make_cyclic_group(
    4,
    "a",
  )

  first_map = GroupMap(
    name="E",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  second_map = GroupMap(
    name="H",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  third_map = GroupMap(
    name="P",
    source=group,
    target=group,
    matrix=[
      [2],
    ],
  )

  first = ImageSubgroupReference(
    group_map=first_map,
  )

  middle = KernelSubgroupReference(
    group_map=second_map,
  )

  right = ImageSubgroupReference(
    group_map=third_map,
  )

  first_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=first,
      right=middle,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=middle,
      right=right,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_transitivity_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_step,
      second_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    SubgroupEqualityStatement(
      left=first,
      right=right,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    first_step,
    second_step,
  )


def test_subgroup_equality_transitivity_rejects_same_value_different_middle_role():
  group = make_cyclic_group(
    4,
    "a",
  )

  first_map = GroupMap(
    name="first",
    source=group,
    target=group,
    matrix=[
      [1],
    ],
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

  last_map = GroupMap(
    name="last",
    source=group,
    target=group,
    matrix=[
      [1],
    ],
  )

  first = ImageSubgroupReference(
    group_map=first_map,
  )

  image_middle = ImageSubgroupReference(
    group_map=image_map,
  )

  kernel_middle = KernelSubgroupReference(
    group_map=kernel_map,
  )

  last = KernelSubgroupReference(
    group_map=last_map,
  )

  assert (
    image_middle.subgroup
    == kernel_middle.subgroup
  )

  assert (
    image_middle
    != kernel_middle
  )

  first_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=first,
      right=image_middle,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=kernel_middle,
      right=last,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_transitivity_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_step,
      second_step,
    ),
  )

  assert match is None


def test_subset_transitivity():
  group = make_cyclic_group(
    8,
    "a",
  )

  small = make_subgroup(
    group,
    [
      (4,),
    ],
  )

  middle = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  whole = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  first_step = ProofStep(
    conclusion=SubsetStatement(
      subset=small,
      superset=middle,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion=SubsetStatement(
      subset=middle,
      superset=whole,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subset_transitivity_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_step,
      second_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    SubsetStatement(
      subset=small,
      superset=whole,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    first_step,
    second_step,
  )


def test_subset_transitivity_rejects_same_value_different_middle_role():
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

  trivial = make_subgroup(
    group,
    [],
  )

  whole = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  image_middle = ImageSubgroupReference(
    group_map=image_map,
  )

  kernel_middle = KernelSubgroupReference(
    group_map=kernel_map,
  )

  assert (
    image_middle.subgroup
    == kernel_middle.subgroup
  )

  assert (
    image_middle
    != kernel_middle
  )

  first_step = ProofStep(
    conclusion=SubsetStatement(
      subset=trivial,
      superset=image_middle,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion=SubsetStatement(
      subset=kernel_middle,
      superset=whole,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subset_transitivity_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_step,
      second_step,
    ),
  )

  assert match is None


def test_phase14_subgroup_relation_closure_reaches_fixed_point():
  group = make_cyclic_group(
    8,
    "a",
  )

  first = make_subgroup(
    group,
    [
      (4,),
    ],
  )

  middle = make_subgroup(
    group,
    [
      (2,),
    ],
  )

  last = make_subgroup(
    group,
    [
      (1,),
    ],
  )

  equality_first_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=first,
      right=middle,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equality_second_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=middle,
      right=last,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  subset_first_step = ProofStep(
    conclusion=SubsetStatement(
      subset=first,
      superset=middle,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  subset_second_step = ProofStep(
    conclusion=SubsetStatement(
      subset=middle,
      superset=last,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equality_symmetry_rule = (
    subgroup_equality_symmetry_inference_rule()
  )

  equality_transitivity_rule = (
    subgroup_equality_transitivity_inference_rule()
  )

  subset_transitivity_rule = (
    subset_transitivity_inference_rule()
  )

  rules = (
    equality_symmetry_rule,
    equality_transitivity_rule,
    subset_transitivity_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        equality_first_step,
        equality_second_step,
        subset_first_step,
        subset_second_step,
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

  assert SubgroupEqualityStatement(
    left=middle,
    right=first,
  ) in conclusions

  assert SubgroupEqualityStatement(
    left=last,
    right=middle,
  ) in conclusions

  assert SubgroupEqualityStatement(
    left=first,
    right=last,
  ) in conclusions

  assert SubgroupEqualityStatement(
    left=last,
    right=first,
  ) in conclusions

  assert SubsetStatement(
    subset=first,
    superset=last,
  ) in conclusions

  transitive_equality_step = next(
    step
    for step in result.steps
    if step.conclusion
    == SubgroupEqualityStatement(
      left=first,
      right=last,
    )
  )

  assert transitive_equality_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    transitive_equality_step.inference_rule
    == equality_transitivity_rule
  )

  assert transitive_equality_step.premises == (
    equality_first_step,
    equality_second_step,
  )

  transitive_subset_step = next(
    step
    for step in result.steps
    if step.conclusion
    == SubsetStatement(
      subset=first,
      superset=last,
    )
  )

  assert transitive_subset_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    transitive_subset_step.inference_rule
    == subset_transitivity_rule
  )

  assert transitive_subset_step.premises == (
    subset_first_step,
    subset_second_step,
  )

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()


def test_subgroup_equality_implies_subset():
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

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=image_reference,
      right=kernel_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_implies_subset_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    SubsetStatement(
      subset=image_reference,
      superset=kernel_reference,
    )
  )


def test_subgroup_equality_implies_subset_preserves_provenance():
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

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=image_reference,
      right=kernel_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    subgroup_equality_implies_subset_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
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
    equality_step,
  )


def test_subgroup_equality_implies_subsets_in_both_directions_with_symmetry():
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

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=image_reference,
      right=kernel_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  symmetry_rule = (
    subgroup_equality_symmetry_inference_rule()
  )

  equality_to_subset_rule = (
    subgroup_equality_implies_subset_inference_rule()
  )

  rules = (
    symmetry_rule,
    equality_to_subset_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        equality_step,
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

  assert SubsetStatement(
    subset=image_reference,
    superset=kernel_reference,
  ) in conclusions

  assert SubsetStatement(
    subset=kernel_reference,
    superset=image_reference,
  ) in conclusions

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()


def test_mutual_subset_implies_subgroup_equality():
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

  forward_subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=image_reference,
      superset=kernel_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  reverse_subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=kernel_reference,
      superset=image_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    mutual_subset_implies_subgroup_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      forward_subset_step,
      reverse_subset_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    SubgroupEqualityStatement(
      left=image_reference,
      right=kernel_reference,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    forward_subset_step,
    reverse_subset_step,
  )


def test_mutual_subset_rejects_same_value_different_role_binding():
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

  whole_group = make_subgroup(
    group,
    [
      (1,),
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

  first_subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=image_reference,
      superset=whole_group,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_subset_step = ProofStep(
    conclusion=SubsetStatement(
      subset=whole_group,
      superset=kernel_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    mutual_subset_implies_subgroup_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_subset_step,
      second_subset_step,
    ),
  )

  assert match is None


def test_phase14_equality_subset_interconnection_reaches_fixed_point():
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

  equality_step = ProofStep(
    conclusion=SubgroupEqualityStatement(
      left=image_reference,
      right=kernel_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  equality_symmetry_rule = (
    subgroup_equality_symmetry_inference_rule()
  )

  equality_transitivity_rule = (
    subgroup_equality_transitivity_inference_rule()
  )

  subset_transitivity_rule = (
    subset_transitivity_inference_rule()
  )

  equality_to_subset_rule = (
    subgroup_equality_implies_subset_inference_rule()
  )

  mutual_subset_to_equality_rule = (
    mutual_subset_implies_subgroup_equality_inference_rule()
  )

  rules = (
    equality_symmetry_rule,
    equality_transitivity_rule,
    subset_transitivity_rule,
    equality_to_subset_rule,
    mutual_subset_to_equality_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        equality_step,
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

  reverse_equality = (
    SubgroupEqualityStatement(
      left=kernel_reference,
      right=image_reference,
    )
  )

  forward_subset = (
    SubsetStatement(
      subset=image_reference,
      superset=kernel_reference,
    )
  )

  reverse_subset = (
    SubsetStatement(
      subset=kernel_reference,
      superset=image_reference,
    )
  )

  assert reverse_equality in conclusions
  assert forward_subset in conclusions
  assert reverse_subset in conclusions

  forward_subset_step = next(
    step
    for step in result.steps
    if step.conclusion == forward_subset
  )

  assert forward_subset_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    forward_subset_step.inference_rule
    == equality_to_subset_rule
  )

  assert forward_subset_step.premises == (
    equality_step,
  )

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()


def test_phase14_representative_exactness_membership_relation_closure():
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

  membership_subset_rule = (
    membership_subset_propagation_inference_rule()
  )

  equality_symmetry_rule = (
    subgroup_equality_symmetry_inference_rule()
  )

  equality_transitivity_rule = (
    subgroup_equality_transitivity_inference_rule()
  )

  subset_transitivity_rule = (
    subset_transitivity_inference_rule()
  )

  equality_to_subset_rule = (
    subgroup_equality_implies_subset_inference_rule()
  )

  mutual_subset_to_equality_rule = (
    mutual_subset_implies_subgroup_equality_inference_rule()
  )

  rules = (
    exactness_rule,
    zero_to_kernel_rule,
    membership_equality_rule,
    membership_subset_rule,
    equality_symmetry_rule,
    equality_transitivity_rule,
    subset_transitivity_rule,
    equality_to_subset_rule,
    mutual_subset_to_equality_rule,
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

  image_reference = ImageSubgroupReference(
    group_map=suspension_map,
  )

  kernel_reference = KernelSubgroupReference(
    group_map=hopf_map,
  )

  subgroup_equality = (
    SubgroupEqualityStatement(
      left=image_reference,
      right=kernel_reference,
    )
  )

  reverse_subgroup_equality = (
    SubgroupEqualityStatement(
      left=kernel_reference,
      right=image_reference,
    )
  )

  kernel_membership = (
    kernel_membership_statement(
      element=alpha,
      group_map=hopf_map,
    )
  )

  image_membership = (
    image_membership_statement(
      element=alpha,
      group_map=suspension_map,
    )
  )

  image_subset_kernel = (
    SubsetStatement(
      subset=image_reference,
      superset=kernel_reference,
    )
  )

  kernel_subset_image = (
    SubsetStatement(
      subset=kernel_reference,
      superset=image_reference,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert subgroup_equality in conclusions
  assert reverse_subgroup_equality in conclusions
  assert kernel_membership in conclusions
  assert image_membership in conclusions
  assert image_subset_kernel in conclusions
  assert kernel_subset_image in conclusions

  exactness_equality_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == subgroup_equality
    )
  )

  assert exactness_equality_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    exactness_equality_step.inference_rule
    == exactness_rule
  )

  assert exactness_equality_step.premises == (
    exactness_step,
  )

  derived_kernel_membership_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == kernel_membership
    )
  )

  assert (
    derived_kernel_membership_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    derived_kernel_membership_step.inference_rule
    == zero_to_kernel_rule
  )

  assert derived_kernel_membership_step.premises == (
    mapped_zero_step,
  )

  derived_image_membership_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == image_membership
    )
  )

  assert (
    derived_image_membership_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    derived_image_membership_step.inference_rule
    == membership_equality_rule
  )

  assert derived_image_membership_step.premises == (
    derived_kernel_membership_step,
    exactness_equality_step,
  )

  image_subset_kernel_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == image_subset_kernel
    )
  )

  assert (
    image_subset_kernel_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    image_subset_kernel_step.inference_rule
    == equality_to_subset_rule
  )

  assert image_subset_kernel_step.premises == (
    exactness_equality_step,
  )

  reverse_equality_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == reverse_subgroup_equality
    )
  )

  kernel_subset_image_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == kernel_subset_image
    )
  )

  assert (
    kernel_subset_image_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    kernel_subset_image_step.inference_rule
    == equality_to_subset_rule
  )

  assert kernel_subset_image_step.premises == (
    reverse_equality_step,
  )

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()


def test_phase14_representative_requires_explicit_role_bridge():
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

  image_reference = ImageSubgroupReference(
    group_map=suspension_map,
  )

  kernel_reference = KernelSubgroupReference(
    group_map=hopf_map,
  )

  assert (
    image_reference.subgroup
    == kernel_reference.subgroup
  )

  assert (
    image_reference
    != kernel_reference
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

  zero_to_kernel_rule = (
    mapped_zero_implies_kernel_membership_inference_rule(
      group_map=hopf_map,
      map_symbol=hopf_symbol,
    )
  )

  membership_equality_rule = (
    subgroup_equality_membership_propagation_inference_rule()
  )

  membership_subset_rule = (
    membership_subset_propagation_inference_rule()
  )

  equality_symmetry_rule = (
    subgroup_equality_symmetry_inference_rule()
  )

  equality_transitivity_rule = (
    subgroup_equality_transitivity_inference_rule()
  )

  subset_transitivity_rule = (
    subset_transitivity_inference_rule()
  )

  equality_to_subset_rule = (
    subgroup_equality_implies_subset_inference_rule()
  )

  mutual_subset_to_equality_rule = (
    mutual_subset_implies_subgroup_equality_inference_rule()
  )

  rules = (
    zero_to_kernel_rule,
    membership_equality_rule,
    membership_subset_rule,
    equality_symmetry_rule,
    equality_transitivity_rule,
    subset_transitivity_rule,
    equality_to_subset_rule,
    mutual_subset_to_equality_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
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

  kernel_membership = (
    kernel_membership_statement(
      element=alpha,
      group_map=hopf_map,
    )
  )

  image_membership = (
    image_membership_statement(
      element=alpha,
      group_map=suspension_map,
    )
  )

  subgroup_equality = (
    SubgroupEqualityStatement(
      left=image_reference,
      right=kernel_reference,
    )
  )

  assert kernel_membership in conclusions

  assert image_membership not in conclusions

  assert subgroup_equality not in conclusions

  assert SubsetStatement(
    subset=image_reference,
    superset=kernel_reference,
  ) not in conclusions

  assert SubsetStatement(
    subset=kernel_reference,
    superset=image_reference,
  ) not in conclusions

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()


def test_coset():
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

  coset = Coset(
    representative=alpha,
    subgroup=subgroup,
  )

  assert coset.representative == alpha
  assert coset.subgroup == subgroup


def test_coset_has_structural_equality_and_distinguishes_representative():
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

  alpha_coset = Coset(
    representative=alpha,
    subgroup=subgroup,
  )

  same_alpha_coset = Coset(
    representative=alpha,
    subgroup=subgroup,
  )

  beta_coset = Coset(
    representative=beta,
    subgroup=subgroup,
  )

  assert alpha_coset == same_alpha_coset
  assert alpha_coset != beta_coset


def test_coset_preserves_role_aware_subgroup_term():
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

  assert (
    image_reference.subgroup
    == kernel_reference.subgroup
  )

  image_coset = Coset(
    representative=alpha,
    subgroup=image_reference,
  )

  kernel_coset = Coset(
    representative=alpha,
    subgroup=kernel_reference,
  )

  assert image_coset.subgroup == image_reference
  assert kernel_coset.subgroup == kernel_reference

  assert image_coset != kernel_coset


def test_modulo_statement():
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

  statement = ModuloStatement(
    left=alpha,
    right=beta,
    modulus=subgroup,
  )

  assert statement.left == alpha
  assert statement.right == beta
  assert statement.modulus == subgroup


def test_modulo_statement_has_structural_equality():
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

  first = ModuloStatement(
    left=alpha,
    right=beta,
    modulus=subgroup,
  )

  second = ModuloStatement(
    left=alpha,
    right=beta,
    modulus=subgroup,
  )

  assert first == second


def test_modulo_statement_distinguishes_left_and_right():
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

  forward = ModuloStatement(
    left=alpha,
    right=beta,
    modulus=subgroup,
  )

  reverse = ModuloStatement(
    left=beta,
    right=alpha,
    modulus=subgroup,
  )

  assert forward != reverse


def test_modulo_statement_preserves_role_aware_modulus():
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
  beta = nu(4)

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

  modulo_image = ModuloStatement(
    left=alpha,
    right=beta,
    modulus=image_reference,
  )

  modulo_kernel = ModuloStatement(
    left=alpha,
    right=beta,
    modulus=kernel_reference,
  )

  assert (
    modulo_image.modulus
    == image_reference
  )

  assert (
    modulo_kernel.modulus
    == kernel_reference
  )

  assert (
    modulo_image
    != modulo_kernel
  )


def test_modulo_implies_difference_membership():
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

  modulo_step = ProofStep(
    conclusion=ModuloStatement(
      left=alpha,
      right=beta,
      modulus=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    modulo_implies_difference_membership_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      modulo_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    MembershipStatement(
      element=Sum(
        left=alpha,
        right=Multiple(
          coefficient=-1,
          expression=beta,
        ),
      ),
      subgroup=subgroup,
    )
  )


def test_modulo_implies_difference_membership_preserves_provenance():
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

  modulo_step = ProofStep(
    conclusion=ModuloStatement(
      left=alpha,
      right=beta,
      modulus=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    modulo_implies_difference_membership_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      modulo_step,
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
    modulo_step,
  )


def test_difference_membership_implies_modulo():
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

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=Sum(
        left=alpha,
        right=Multiple(
          coefficient=-1,
          expression=beta,
        ),
      ),
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    difference_membership_implies_modulo_inference_rule()
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

  assert derived_step.conclusion == (
    ModuloStatement(
      left=alpha,
      right=beta,
      modulus=subgroup,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    membership_step,
  )


def test_difference_membership_implies_modulo_rejects_plain_membership():
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

  membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=alpha,
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    difference_membership_implies_modulo_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      membership_step,
    ),
  )

  assert match is None


def test_difference_membership_implies_modulo_requires_negative_one_multiple():
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

  positive_membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=Sum(
        left=alpha,
        right=Multiple(
          coefficient=1,
          expression=beta,
        ),
      ),
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  double_membership_step = ProofStep(
    conclusion=MembershipStatement(
      element=Sum(
        left=alpha,
        right=Multiple(
          coefficient=2,
          expression=beta,
        ),
      ),
      subgroup=subgroup,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    difference_membership_implies_modulo_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      positive_membership_step,
    ),
  ) is None

  assert find_inference_match(
    rule,
    (
      double_membership_step,
    ),
  ) is None


def test_phase15_modulo_membership_bridge_reaches_fixed_point():
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

  alpha = eta(3)
  beta = nu(4)

  image_reference = ImageSubgroupReference(
    group_map=image_map,
  )

  modulo_step = ProofStep(
    conclusion=ModuloStatement(
      left=alpha,
      right=beta,
      modulus=image_reference,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  modulo_to_membership_rule = (
    modulo_implies_difference_membership_inference_rule()
  )

  membership_to_modulo_rule = (
    difference_membership_implies_modulo_inference_rule()
  )

  rules = (
    modulo_to_membership_rule,
    membership_to_modulo_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        modulo_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  difference_membership = (
    MembershipStatement(
      element=Sum(
        left=alpha,
        right=Multiple(
          coefficient=-1,
          expression=beta,
        ),
      ),
      subgroup=image_reference,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert modulo_step.conclusion in conclusions
  assert difference_membership in conclusions

  assert len(
    tuple(
      conclusion
      for conclusion in conclusions
      if isinstance(
        conclusion,
        ModuloStatement,
      )
    )
  ) == 1

  assert len(
    tuple(
      conclusion
      for conclusion in conclusions
      if isinstance(
        conclusion,
        MembershipStatement,
      )
    )
  ) == 1

  derived_membership_step = next(
    step
    for step in result.steps
    if step.conclusion
    == difference_membership
  )

  assert derived_membership_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    derived_membership_step.inference_rule
    == modulo_to_membership_rule
  )

  assert derived_membership_step.premises == (
    modulo_step,
  )

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()




