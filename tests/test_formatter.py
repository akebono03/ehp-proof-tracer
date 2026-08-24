from expression import (
  Composition,
  Multiple,
  Zero,
  eta,
)
from formatter import (
  format_abelian_structure,
  format_expression,
  format_proof,
  format_proof_step,
  format_statement,
)
from proof import (
  Proof,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  ehp_sphere_proof,
)
from algebra import AbelianGroupStructure
from ehp import EHPSegment
from pathlib import Path
from repository import SphereRepository


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







