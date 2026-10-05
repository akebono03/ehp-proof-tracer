from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

from phase158_r5_5c_2_audit_harness_invariant_repair.audit_phase158_r5_5c_2 import (
  audit_equation_chain,
)


def _line(
  text: str,
  *,
  math: bool,
):
  if math:
    segment = SimpleNamespace(
      kind="inline_math",
      value=text,
    )
    return (
      SimpleNamespace(
        statement_latex=None,
        segments=(segment,),
      ),
      text,
    )

  return (
    SimpleNamespace(
      statement_latex=None,
      segments=(),
    ),
    text,
  )


def test_phase158_r5_5c_2_accepts_untagged_visible_target():
  lines = [
    _line(r"a=b\tag{1}", math=True),
    _line("(1) より,", math=False),
    _line("a=c", math=True),
  ]

  assert audit_equation_chain(n=5, k=5, lines=lines) == ()


def test_phase158_r5_5c_2_accepts_tagged_visible_target():
  lines = [
    _line(r"a=b\tag{1}", math=True),
    _line(r"b=c\tag{2}", math=True),
    _line("(1) と (2) より,", math=False),
    _line(r"a=c\tag{3}", math=True),
  ]

  assert audit_equation_chain(n=3, k=3, lines=lines) == ()


def test_phase158_r5_5c_2_rejects_missing_or_late_source():
  lines = [
    _line("(1) より,", math=False),
    _line(r"a=b\tag{1}", math=True),
  ]

  defects = audit_equation_chain(n=9, k=1, lines=lines)

  assert len(defects) == 1
  assert defects[0].defect_kind == "MISSING_OR_LATE_SOURCE"


def test_phase158_r5_5c_2_rejects_nonmathematical_target():
  lines = [
    _line(r"a=b\tag{1}", math=True),
    _line("(1) より,", math=False),
    _line("therefore", math=False),
  ]

  defects = audit_equation_chain(n=9, k=2, lines=lines)

  assert len(defects) == 1
  assert defects[0].defect_kind == "MISSING_VISIBLE_TARGET"
