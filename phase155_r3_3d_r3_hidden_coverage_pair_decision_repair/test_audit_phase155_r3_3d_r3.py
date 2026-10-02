
from __future__ import annotations

import ast

import audit_phase155_r3_3d_r3 as audit


def test_split_test_id():
  assert audit._split_test_id(
    r"tests\test_a.py::test_b"
  ) == (
    "tests/test_a.py",
    "test_b",
  )


def test_assertion_dumps_extracts_asserts():
  node = ast.parse(
    "def test_x():\n"
    "  assert a == b\n"
    "  assert c\n"
  ).body[0]

  assertions = audit._assertion_dumps(
    node
  )

  assert len(assertions) == 2


def test_semantic_relation_detects_containment():
  older = {
    "assertions": [
      "A",
    ],
    "calls": [
      "C1",
    ],
  }
  newer = {
    "assertions": [
      "A",
      "B",
    ],
    "calls": [
      "C1",
      "C2",
    ],
  }

  relation = audit._semantic_relation(
    older,
    newer,
  )

  assert (
    relation["older_assertions_subset_newer"]
    is True
  )
  assert (
    relation["older_calls_subset_newer"]
    is True
  )


def test_semantic_relation_detects_missing_old_assertion():
  older = {
    "assertions": [
      "A",
      "C",
    ],
    "calls": [
      "C1",
    ],
  }
  newer = {
    "assertions": [
      "A",
      "B",
    ],
    "calls": [
      "C1",
    ],
  }

  relation = audit._semantic_relation(
    older,
    newer,
  )

  assert (
    relation["older_assertions_subset_newer"]
    is False
  )
  assert relation["older_only_assertions"] == [
    "C"
  ]


def test_module_level_test_coverage_marks_last_definition_runtime(
  tmp_path,
):
  tests_dir = tmp_path / "tests"
  tests_dir.mkdir()
  path = tests_dir / "test_x.py"
  path.write_text(
    "def test_a():\n"
    "  assert True\n"
    "\n"
    "def test_a():\n"
    "  assert False\n",
    encoding="utf-8",
  )

  coverage = audit._all_assertion_coverage(
    tmp_path
  )

  runtime_flags = sorted(
    location["is_runtime_definition"]
    for locations in coverage.values()
    for location in locations
  )

  assert runtime_flags == [
    False,
    True,
  ]
