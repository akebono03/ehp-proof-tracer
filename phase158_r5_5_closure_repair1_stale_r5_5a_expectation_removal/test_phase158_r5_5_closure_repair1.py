from __future__ import annotations

from phase158_r5_5a_public_depth2_audit_parity_repair.audit_phase158_r5_5a import (
  MAX_DEPTH,
  audit_target,
  normalize_visible_text,
)

from audit_phase158_r5_5_closure import (
  _canonical_visible_text,
  _connector_findings,
)


def test_phase158_r5_5_closure_repair1_keeps_r5_5a_normalization_contract():
  assert (
    normalize_visible_text(
      "[R2]を用いて, $\\nu_{4}$ の分解を用いる."
    )
    == "$\\nu_{4}$ の分解を用いる"
  )


def test_phase158_r5_5_closure_repair1_keeps_public_depth2_contract():
  target = audit_target(
    "pi16_9_generic",
    9,
    7,
  )

  assert target[
    "view"
  ].mode == "narrative"

  assert (
    target[
      "view"
    ].max_depth
    == MAX_DEPTH
    == 2
  )


def test_phase158_r5_5_closure_repair1_pi7_4_has_no_out_of_order_derivation():
  target = audit_target(
    "pi7_4_former_legacy",
    4,
    3,
  )

  kinds = tuple(
    item.kind
    for item in target[
      "derivations"
    ]
  )

  assert (
    "OUT_OF_ORDER_DERIVATION"
    not in kinds
  )


def test_phase158_r5_5_closure_repair1_pi15_8_has_no_out_of_order_derivation():
  target = audit_target(
    "pi15_8_former_dedicated",
    8,
    7,
  )

  kinds = tuple(
    item.kind
    for item in target[
      "derivations"
    ]
  )

  assert (
    "OUT_OF_ORDER_DERIVATION"
    not in kinds
  )


def test_phase158_r5_5_closure_repair1_canonical_visible_text():
  assert (
    _canonical_visible_text(
      r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    )
    ==
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
  )


def test_phase158_r5_5_closure_repair1_connector_accepts_tagged_target():
  findings, count, tagged, untagged = (
    _connector_findings(
      (
        r"A=B\tag{1}",
        "(1) より,",
        r"A=C\tag{2}",
      )
    )
  )

  assert findings == ()
  assert count == 1
  assert tagged == 1
  assert untagged == 0


def test_phase158_r5_5_closure_repair1_connector_accepts_untagged_target():
  findings, count, tagged, untagged = (
    _connector_findings(
      (
        r"A=B\tag{1}",
        "(1) より,",
        r"A=C",
      )
    )
  )

  assert findings == ()
  assert count == 1
  assert tagged == 0
  assert untagged == 1


def test_phase158_r5_5_closure_repair1_connector_rejects_late_source():
  findings, count, tagged, untagged = (
    _connector_findings(
      (
        "(1) より,",
        r"A=C",
        r"A=B\tag{1}",
      )
    )
  )

  assert count == 1
  assert tagged == 0
  assert untagged == 0
  assert len(
    findings
  ) == 1
  assert findings[
    0
  ][
    1
  ] == "MISSING_OR_LATE_SOURCE"
