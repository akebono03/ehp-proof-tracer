from phase158_r5_5a_public_depth2_audit_parity_repair.audit_phase158_r5_5a import (
  MAX_DEPTH,
  audit_target,
  normalize_visible_text,
)


def test_phase158_r5_5a_reference_prefix_is_removed_before_mapping():
  assert (
    normalize_visible_text(
      "[R2]を用いて, $\\nu_{4}$ の分解を用いる."
    )
    == "$\\nu_{4}$ の分解を用いる"
  )


def test_phase158_r5_5a_public_scope_is_actual_depth2_web_narrative():
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


def test_phase158_r5_5a_pi7_4_detects_visible_derivation_order():
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
    in kinds
  )


def test_phase158_r5_5a_pi15_8_detects_visible_derivation_order():
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
    in kinds
  )
