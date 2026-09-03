from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
)
from generator_facts import (
  GENERATOR_FACT_REPOSITORY,
)
from hopf_facts import (
  ETA_2,
  ETA_2_HOPF_INVARIANT_FACT,
  IOTA_3,
  TODA_PROP_5_1_REFERENCE,
)
from hopf_rules import (
  HopfInvariantStatement,
  hopf_invariant_proof_step,
  hopf_invariant_statement_to_ehp_h_equality_inference_rule,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  LiteratureReference,
  ProofRule,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)


def test_phase35_1_iota_1_identity_is_representable_with_explicit_typing():
  iota_1_generator = GeneratorSymbol(
    family="ι",
    index=1,
  )

  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=iota_1_generator,
  )

  assert iota_1.generator == (
    iota_1_generator
  )

  assert iota_1.source == 1
  assert iota_1.target == 1


def test_phase35_1_iota_2_identity_is_representable_with_explicit_typing():
  iota_2_generator = GeneratorSymbol(
    family="ι",
    index=2,
  )

  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=iota_2_generator,
  )

  assert iota_2.generator == (
    iota_2_generator
  )

  assert iota_2.source == 2
  assert iota_2.target == 2


def test_phase35_1_iota_3_identity_is_representable_with_explicit_typing():
  iota_3_generator = GeneratorSymbol(
    family="ι",
    index=3,
  )

  iota_3 = HomotopyElement(
    name="ι₃",
    dimension=3,
    source=3,
    target=3,
    generator=iota_3_generator,
  )

  assert iota_3.generator == (
    iota_3_generator
  )

  assert iota_3.source == 3
  assert iota_3.target == 3


def test_phase35_1_eta_2_is_representable_with_explicit_typing():
  eta_2_generator = GeneratorSymbol(
    family="η",
    index=2,
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=eta_2_generator,
  )

  assert eta_2.generator == (
    eta_2_generator
  )

  assert eta_2.source == 3
  assert eta_2.target == 2


def test_phase35_1_two_iota_1_is_representable_as_multiple():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  assert two_iota_1 == Multiple(
    coefficient=2,
    expression=iota_1,
  )

  assert two_iota_1.coefficient == 2
  assert two_iota_1.expression == iota_1


def test_phase35_1_two_iota_2_is_representable_as_multiple():
  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  two_iota_2 = Multiple(
    coefficient=2,
    expression=iota_2,
  )

  assert two_iota_2 == Multiple(
    coefficient=2,
    expression=iota_2,
  )

  assert two_iota_2.coefficient == 2
  assert two_iota_2.expression == iota_2


def test_phase35_1_actual_generators_are_structurally_distinct():
  iota_1 = GeneratorSymbol(
    family="ι",
    index=1,
  )

  iota_2 = GeneratorSymbol(
    family="ι",
    index=2,
  )

  iota_3 = GeneratorSymbol(
    family="ι",
    index=3,
  )

  eta_2 = GeneratorSymbol(
    family="η",
    index=2,
  )

  assert iota_1 != iota_2
  assert iota_2 != iota_3
  assert iota_2 != eta_2


def test_phase35_1_current_generator_repository_does_not_yet_type_iota_1():
  iota_1_generator = GeneratorSymbol(
    family="ι",
    index=1,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      iota_1_generator
    )
    is None
  )


def test_phase35_1_current_generator_repository_does_not_yet_type_iota_2():
  iota_2_generator = GeneratorSymbol(
    family="ι",
    index=2,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      iota_2_generator
    )
    is None
  )


def test_phase35_1_current_generator_repository_does_not_yet_type_iota_3():
  iota_3_generator = GeneratorSymbol(
    family="ι",
    index=3,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      iota_3_generator
    )
    is None
  )


def test_phase35_1_current_generator_repository_does_not_yet_type_eta_2():
  eta_2_generator = GeneratorSymbol(
    family="η",
    index=2,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      eta_2_generator
    )
    is None
  )


def test_phase35_1_generator_notation_does_not_implicitly_add_typing():
  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  assert eta_2.source is None
  assert eta_2.target is None


def test_phase35_1_representative_actual_elements_need_no_new_expression_type():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  iota_3 = HomotopyElement(
    name="ι₃",
    dimension=3,
    source=3,
    target=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  two_iota_2 = Multiple(
    coefficient=2,
    expression=iota_2,
  )

  assert isinstance(
    iota_1,
    HomotopyElement,
  )

  assert isinstance(
    iota_2,
    HomotopyElement,
  )

  assert isinstance(
    iota_3,
    HomotopyElement,
  )

  assert isinstance(
    eta_2,
    HomotopyElement,
  )

  assert isinstance(
    two_iota_1,
    Multiple,
  )

  assert isinstance(
    two_iota_2,
    Multiple,
  )

  assert two_iota_1.expression == (
    iota_1
  )

  assert two_iota_2.expression == (
    iota_2
  )


def test_phase35_2_toda_prop_5_1_reference_is_structured_literature_reference():
  assert isinstance(
    TODA_PROP_5_1_REFERENCE,
    LiteratureReference,
  )

  assert (
    TODA_PROP_5_1_REFERENCE.label
    == "Toda Prop.5.1"
  )

  assert (
    TODA_PROP_5_1_REFERENCE.author
    == "H. Toda"
  )

  assert (
    TODA_PROP_5_1_REFERENCE.title
    == (
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    )
  )

  assert (
    TODA_PROP_5_1_REFERENCE.year
    == 1962
  )

  assert (
    TODA_PROP_5_1_REFERENCE.locator
    == "Proposition 5.1"
  )


def test_phase35_2_eta_2_hopf_fact_represents_h_eta_2_equals_iota_3():
  assert isinstance(
    ETA_2_HOPF_INVARIANT_FACT,
    HopfInvariantStatement,
  )

  assert (
    ETA_2_HOPF_INVARIANT_FACT.expression
    == ETA_2
  )

  assert (
    ETA_2_HOPF_INVARIANT_FACT.value
    == IOTA_3
  )

  assert ETA_2.source == 3
  assert ETA_2.target == 2

  assert IOTA_3.source == 3
  assert IOTA_3.target == 3


def test_phase35_2_eta_2_hopf_fact_preserves_toda_prop_5_1_provenance():
  assert (
    ETA_2_HOPF_INVARIANT_FACT.source
    == TODA_PROP_5_1_REFERENCE
  )

  assert (
    ETA_2_HOPF_INVARIANT_FACT.note
    == (
      "Toda Prop.5.1 "
      "H(η₂)=ι₃."
    )
  )


def test_phase35_2_eta_2_hopf_fact_materializes_as_given_proof_step():
  step = hopf_invariant_proof_step(
    ETA_2_HOPF_INVARIANT_FACT
  )

  assert step.conclusion == (
    ETA_2_HOPF_INVARIANT_FACT
  )

  assert step.rule == ProofRule.GIVEN
  assert step.premises == ()
  assert step.inference_rule is None

  assert (
    step.conclusion.source
    == TODA_PROP_5_1_REFERENCE
  )


def test_phase35_2_eta_2_hopf_fact_bridges_to_actual_ehp_h_equality():
  hopf_step = hopf_invariant_proof_step(
    ETA_2_HOPF_INVARIANT_FACT
  )

  rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=ETA_2,
    ),
    rhs=IOTA_3,
    relation_type=RelationType.EQUALITY,
  )

  assert (
    step.conclusion.lhs.map
    is EHP_H_MAP
  )


def test_phase35_2_actual_h_equality_preserves_fact_provenance_through_premise():
  hopf_step = hopf_invariant_proof_step(
    ETA_2_HOPF_INVARIANT_FACT
  )

  rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule == rule

  assert step.premises == (
    hopf_step,
  )

  assert (
    step.premises[0]
    .conclusion
    .source
    == TODA_PROP_5_1_REFERENCE
  )

  assert (
    step.premises[0]
    .conclusion
    .note
    == (
      "Toda Prop.5.1 "
      "H(η₂)=ι₃."
    )
  )






