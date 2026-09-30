import pytest

from phase148_rc2_4_post_repair_six_group_cross_group_audit.audit_phase148_rc2_4_post_repair_six_group import (
  CASES,
  _case_data,
)


@pytest.mark.parametrize(
  "label,n,k",
  CASES,
)
def test_phase148_rc2_4_post_repair_closure_does_not_restore_complete_replay(
  label,
  n,
  k,
):
  record = _case_data(
    label,
    n,
    k,
  )

  assert (
    record[
      "closure_nodes"
    ]
    <= record[
      "complete_nodes"
    ]
  )

  if (
    record[
      "complete_nodes"
    ]
    > record[
      "input_nodes"
    ]
  ):
    assert (
      record[
        "closure_nodes"
      ]
      < record[
        "complete_nodes"
      ]
    )


@pytest.mark.parametrize(
  "label,n,k",
  CASES,
)
def test_phase148_rc2_4_post_repair_calculation_closure_adds_no_exactness_steps(
  label,
  n,
  k,
):
  record = _case_data(
    label,
    n,
    k,
  )

  assert (
    record[
      "added_exactness"
    ]
    == ()
  )


@pytest.mark.parametrize(
  "label,n,k",
  CASES,
)
def test_phase148_rc2_4_post_repair_web_narrative_has_no_raw_exactness_phrases(
  label,
  n,
  k,
):
  record = _case_data(
    label,
    n,
    k,
  )

  assert (
    record[
      "raw_exactness_phrases"
    ]
    == 0
  )


@pytest.mark.parametrize(
  "label,n,k",
  CASES,
)
def test_phase148_rc2_4_post_repair_has_no_ambiguous_relevant_exposure(
  label,
  n,
  k,
):
  record = _case_data(
    label,
    n,
    k,
  )

  assert (
    record[
      "exposure_counts"
    ].get(
      "ambiguous_relevant",
      0,
    )
    == 0
  )


def test_phase148_rc2_4_post_repair_pi6_3_retains_numbered_calculation_chain():
  record = _case_data(
    "pi_6^3",
    3,
    3,
  )
  rendered = record[
    "rendered"
  ]

  assert r"\tag{1}" in rendered
  assert r"\tag{2}" in rendered
  assert r"\tag{3}" in rendered
  assert "(1) と (2) より、" in rendered


def test_phase148_rc2_4_post_repair_pi6_3_retains_group_result_and_short_exact_sequence():
  record = _case_data(
    "pi_6^3",
    3,
    3,
  )
  rendered = record[
    "rendered"
  ]

  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    in rendered
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    in rendered
  )
  assert (
    r"\xrightarrow{E} \pi_{6}^{3}"
    in rendered
  )
  assert (
    r"\xrightarrow{H} \pi_{6}^{5}"
    in rendered
  )
  assert (
    r"\longrightarrow 0"
    in rendered
  )
