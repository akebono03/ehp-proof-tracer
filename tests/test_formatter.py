from expression import (
  Composition,
  Multiple,
  Zero,
  eta,
)
from formatter import (
  format_abelian_structure,
  format_expression,
  format_inference_rule,
  format_literature_reference,
  format_proof,
  format_proof_step,
  format_source,
  format_statement,
)
from proof import (
  InferenceRule,
  LiteratureReference,
  Proof,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  ehp_sphere_proof,
  relation_inference_proof,
)
from algebra import AbelianGroupStructure
from ehp import EHPSegment
from pathlib import Path
from repository import (
  RelationRepository,
  SphereRepository,
)

BASE_DIR = Path(__file__).resolve().parent.parent


def test_format_expression_zero():
  assert (
    format_expression(Zero())
    == "0"
  )


def test_format_expression_element():
  assert (
    format_expression(eta(3))
    == "η_3"
  )


def test_format_expression_multiple():
  assert (
    format_expression(
      Multiple(
        2,
        eta(3),
      )
    )
    == "2η_3"
  )


def test_format_expression_composition():
  assert (
    format_expression(
      Composition(
        eta(3),
        eta(4),
      )
    )
    == "η_3η_4"
  )


def test_format_relation():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert (
    format_statement(relation)
    == "2η_3 = 0"
  )


def test_format_abelian_structure_zero():
  structure = AbelianGroupStructure(
    free_rank=0,
    torsion_orders=(),
  )

  assert (
    format_abelian_structure(
      structure
    )
    == "0"
  )


def test_format_abelian_structure_z():
  structure = AbelianGroupStructure(
    free_rank=1,
    torsion_orders=(),
  )

  assert (
    format_abelian_structure(
      structure
    )
    == "Z"
  )


def test_format_abelian_structure_mixed():
  structure = AbelianGroupStructure(
    free_rank=1,
    torsion_orders=(2, 4),
  )

  assert (
    format_abelian_structure(
      structure
    )
    == "Z ⊕ Z/2 ⊕ Z/4"
  )


def test_format_proof_step():
  step = ProofStep(
    conclusion="result",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    format_proof_step(
      step,
      number=1,
    )
    == (
      "1. result\n"
      "   [given]"
    )
  )


def test_format_ehp_sphere_proof():
  repo = SphereRepository(
    BASE_DIR
    / "data"
    / "sphere.csv"
  )

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  proof = ehp_sphere_proof(
    segment
  )

  text = format_proof(
    proof
  )

  assert "Im(E)" in text
  assert "Ker(H)" in text
  assert "[ehp exactness]" in text


def test_format_proof_with_premises():
  step1 = ProofStep(
    conclusion="first result",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  step2 = ProofStep(
    conclusion="second result",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  step3 = ProofStep(
    conclusion="final result",
    premises=(
      step1,
      step2,
    ),
    rule=ProofRule.EXACTNESS,
  )

  proof = Proof(
    conclusion="final result",
    steps=[
      step1,
      step2,
      step3,
    ],
  )

  text = format_proof(
    proof
  )

  assert (
    "Premises: 1, 2"
    in text
  )


def test_format_ehp_sphere_proof_premises():
  repo = SphereRepository(
    BASE_DIR
    / "data"
    / "sphere.csv"
  )

  segment = EHPSegment(
    repo,
    n=3,
    k=5,
  )

  proof = ehp_sphere_proof(
    segment
  )

  text = format_proof(
    proof
  )

  assert (
    "3. Im(E) = Ker(H)"
    in text
  )

  assert (
    "Premises: 1, 2"
    in text
  )


def test_format_relation_inference_proof():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  proof = relation_inference_proof(
    relation,
    "η_3 has order dividing 2",
  )

  text = format_proof(
    proof
  )

  assert (
    "1. 2η_3 = 0"
    in text
  )

  assert (
    "[relation]"
    in text
  )

  assert (
    "2. η_3 has order dividing 2"
    in text
  )

  assert (
    "Premises: 1"
    in text
  )


def test_relation_repository_to_inference_proof():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  repository = RelationRepository([
    relation,
  ])

  relations = repository.find_relations(
    lhs=Multiple(
      2,
      eta(3),
    ),
  )

  proof = relation_inference_proof(
    relations[0],
    "η_3 has order dividing 2",
  )

  assert (
    proof.steps[0].conclusion
    == relation
  )

  assert (
    proof.steps[1].premises
    == (
      proof.steps[0],
    )
  )


def test_format_relation_source():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  text = format_proof_step(
    step,
    number=1,
  )

  assert (
    "Source: Toda"
    in text
  )


def test_format_relation_note():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    note="classical eta relation",
  )

  step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  text = format_proof_step(
    step,
    number=1,
  )

  assert (
    "Relation note: classical eta relation"
    in text
  )


def test_format_proof_step_note():
  step = ProofStep(
    conclusion="result",
    premises=(),
    rule=ProofRule.GIVEN,
    note="derived by a test rule",
  )

  text = format_proof_step(
    step,
    number=1,
  )

  assert (
    "Note: derived by a test rule"
    in text
  )


def test_format_relation_and_proof_step_notes():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
    note="classical eta relation",
  )

  proof = relation_inference_proof(
    relation,
    "η_3 has order dividing 2",
    note="derived from the zero relation",
  )

  text = format_proof(
    proof
  )

  assert (
    "1. 2η_3 = 0"
    in text
  )

  assert (
    "Source: Toda"
    in text
  )

  assert (
    "Relation note: classical eta relation"
    in text
  )

  assert (
    "2. η_3 has order dividing 2"
    in text
  )

  assert (
    "Premises: 1"
    in text
  )

  assert (
    "Note: derived from the zero relation"
    in text
  )


def test_format_literature_reference():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Proposition X",
  )

  assert (
    format_literature_reference(
      reference
    )
    == (
      "Toda — H. Toda, "
      "Composition Methods in "
      "Homotopy Groups of Spheres, "
      "1962 — Proposition X"
    )
  )


def test_format_source_string():
  assert (
    format_source("Toda")
    == "Toda"
  )


def test_format_source_literature_reference():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
  )

  assert (
    format_source(reference)
    == (
      "Toda — H. Toda, "
      "Composition Methods in "
      "Homotopy Groups of Spheres, "
      "1962"
    )
  )


def test_format_relation_structured_source():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Proposition X",
  )

  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source=reference,
  )

  step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  text = format_proof_step(
    step,
    number=1,
  )

  assert (
    "Source: Toda"
    in text
  )

  assert (
    "H. Toda"
    in text
  )

  assert (
    "Composition Methods in "
    "Homotopy Groups of Spheres"
    in text
  )

  assert (
    "1962"
    in text
  )

  assert (
    "Proposition X"
    in text
  )


def test_format_multiple_relation_inference_proof():
  relation1 = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  relation2 = Relation(
    lhs=Multiple(
      2,
      eta(4),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  proof = relation_inference_proof(
    (
      relation1,
      relation2,
    ),
    "combined result",
    note=(
      "derived from two relations"
    ),
  )

  text = format_proof(
    proof
  )

  assert (
    "1. 2η_3 = 0"
    in text
  )

  assert (
    "2. 2η_4 = 0"
    in text
  )

  assert (
    "3. combined result"
    in text
  )

  assert (
    "Premises: 1, 2"
    in text
  )

  assert (
    "Note: derived from two relations"
    in text
  )


def test_format_inference_rule():
  rule = InferenceRule(
    name=(
      "zero relation implies "
      "order bound"
    ),
  )

  assert (
    format_inference_rule(
      rule
    )
    == (
      "zero relation implies "
      "order bound"
    )
  )


def test_format_proof_step_inference_rule():
  rule = InferenceRule(
    name=(
      "zero relation implies "
      "order bound"
    ),
  )

  step = ProofStep(
    conclusion=(
      "η_3 has order dividing 2"
    ),
    premises=(),
    rule=ProofRule.RELATION,
    inference_rule=rule,
  )

  text = format_proof_step(
    step,
    number=1,
  )

  assert (
    "Inference rule: "
    "zero relation implies "
    "order bound"
    in text
  )


def test_format_relation_inference_with_rule():
  relation = Relation(
    lhs=Multiple(
      2,
      eta(3),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  rule = InferenceRule(
    name=(
      "zero relation implies "
      "order bound"
    ),
  )

  proof = relation_inference_proof(
    relation,
    "η_3 has order dividing 2",
    inference_rule=rule,
  )

  text = format_proof(
    proof
  )

  assert (
    "1. 2η_3 = 0"
    in text
  )

  assert (
    "2. η_3 has order dividing 2"
    in text
  )

  assert (
    "Inference rule: "
    "zero relation implies "
    "order bound"
    in text
  )

  assert (
    "Premises: 1"
    in text
  )













