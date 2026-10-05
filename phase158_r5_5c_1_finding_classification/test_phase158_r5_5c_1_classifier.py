from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

PHASE_DIR = Path(__file__).resolve().parent
if str(PHASE_DIR) not in sys.path:
  sys.path.insert(0, str(PHASE_DIR))

from audit_phase158_r5_5c_1 import classify_public_connector


@dataclass(frozen=True)
class Segment:
  kind: str
  value: str


@dataclass(frozen=True)
class Line:
  statement_latex: str | None = None
  segments: tuple[Segment, ...] = ()


def _lines(*items: tuple[str | None, str]):
  result = []
  for math, text in items:
    result.append((Line(statement_latex=math), text))
  return result


def test_phase158_r5_5c_1_classifies_untagged_immediate_math_target_without_bug():
  result = classify_public_connector(
    n=4,
    k=3,
    connector="(1) より,",
    lines=_lines(
      (r"a=b\tag{1}", r"a=b\tag{1}"),
      (None, "(1) より,"),
      (r"a=c", r"a=c"),
    ),
  )

  assert result.classification == "CONNECTOR_TARGET_NOT_TAGGED"
  assert result.production_bug == "NO"


def test_phase158_r5_5c_1_classifies_missing_source_as_real_ordering_defect():
  result = classify_public_connector(
    n=5,
    k=5,
    connector="(1) より,",
    lines=_lines(
      (None, "(1) より,"),
      (r"a=c\tag{2}", r"a=c\tag{2}"),
    ),
  )

  assert result.classification == "REAL_ORDERING_DEFECT"
  assert result.production_bug == "YES"


def test_phase158_r5_5c_1_classifies_tagged_immediate_target_as_harness_false_positive():
  result = classify_public_connector(
    n=6,
    k=6,
    connector="(1) と (2) より,",
    lines=_lines(
      (r"a=b\tag{1}", r"a=b\tag{1}"),
      (r"b=c\tag{2}", r"b=c\tag{2}"),
      (None, "(1) と (2) より,"),
      (r"a=c\tag{3}", r"a=c\tag{3}"),
    ),
  )

  assert result.classification == "AUDIT_HARNESS_FALSE_POSITIVE"
  assert result.production_bug == "NO"
