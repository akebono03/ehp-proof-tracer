from __future__ import annotations

import sys
from pathlib import Path


REPOSITORY_ROOT = Path(
  __file__
).resolve().parents[
  1
]

if str(
  REPOSITORY_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from phase158_r5_5c_cross_group_generic_order_audit.audit_phase158_r5_5c import (
  equation_chain_defects,
)


def test_phase158_r5_5c_valid_numbered_chain_has_no_finding():
  proof_lines = (
    r"a=b\tag{1}.",
    r"b=c\tag{2}.",
    "(1) と (2) より,",
    r"a=c\tag{3}.",
    "□",
  )

  assert equation_chain_defects(
    proof_lines
  ) == []


def test_phase158_r5_5c_connector_without_tagged_target_is_found():
  proof_lines = (
    r"a=b\tag{1}.",
    r"b=c\tag{2}.",
    "(1) と (2) より,",
    r"a=c.",
    "□",
  )

  defects = equation_chain_defects(
    proof_lines
  )

  assert len(
    defects
  ) == 1
  assert (
    defects[
      0
    ][
      "next_has_tag"
    ]
    is False
  )
