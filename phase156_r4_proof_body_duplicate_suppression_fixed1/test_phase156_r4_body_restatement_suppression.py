from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_reference_body_restatements,
)


def test_phase156_r4_removes_standalone_reference_restatement():
  statement = r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
  body = (
    statement
    + "\n\n"
    + "次に進む."
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_restatements(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert rendered == "次に進む."


def test_phase156_r4_replaces_plain_restatement_with_reference_marker():
  statement = r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
  body = (
    "まず, "
    + statement
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_restatements(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert rendered == "まず, [R2]を用いる."


def test_phase156_r4_preserves_derivation_sentence():
  statement = r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
  body = (
    "このことから, "
    + statement
    + "を得る."
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_restatements(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert rendered == body


def test_phase156_r4_preserves_calculation_context():
  statement = r"$E\eta_{2}\eta_{3} = \eta_{3}^{2}$"
  body = (
    "計算すると, "
    + statement
    + "を得る."
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_restatements(
      body,
      {
        1: (
          statement,
        ),
      },
    )
  )

  assert rendered == body
