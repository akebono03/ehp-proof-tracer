from __future__ import annotations

import ast

from phase155_closure_r2a_r1_replacements import (
  REPLACEMENTS,
)
from repair_phase155_closure_r2a_r1 import (
  _replace_function,
)


def test_exactly_five_repository_tests_are_targeted():
  assert sum(
    len(
      functions
    )
    for functions in REPLACEMENTS.values()
  ) == 5


def test_only_expected_phase132_133_files_are_targeted():
  assert set(
    REPLACEMENTS
  ) == {
    "tests/test_phase132_8_group_proof_narrative_dedup.py",
    "tests/test_phase133_10_sigma_label_wording.py",
    "tests/test_phase133_6_group_proof_narrative_labels.py",
    "tests/test_phase133_9_group_proof_narrative_labels.py",
  }


def test_replacements_do_not_freeze_lemma_514_or_513():
  joined = "\n".join(
    replacement
    for functions in REPLACEMENTS.values()
    for replacement in functions.values()
  )

  assert (
    'assert "Lemma 5.14" in'
    not in joined
  )
  assert (
    'assert "Lemma 5.13" in'
    not in joined
  )


def test_replacements_keep_reference_and_group_contracts():
  joined = "\n".join(
    replacement
    for functions in REPLACEMENTS.values()
    for replacement in functions.values()
  )

  assert 'assert "[R1]" in' in joined
  assert r'\pi_{16}^{9}' in joined
  assert r'\pi_{12}^{5}' in joined


def test_whole_function_replacement_parses():
  source = (
    "def target():\n"
    "  assert False\n\n"
    "def untouched():\n"
    "  return 1\n"
  )

  updated = _replace_function(
    source,
    "target",
    (
      "def target():\n"
      "  assert True\n"
    ),
  )

  ast.parse(
    updated
  )
  assert "assert False" not in updated
  assert "def untouched():" in updated
