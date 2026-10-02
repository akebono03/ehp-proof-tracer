from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(
  __file__
).resolve().parent

SPEC = importlib.util.spec_from_file_location(
  "phase155_r2b_r1_installer",
  HERE
  / "install_phase155_closure_r2b_r1.py",
)

assert SPEC is not None
assert SPEC.loader is not None

MODULE = importlib.util.module_from_spec(
  SPEC
)
SPEC.loader.exec_module(
  MODULE
)


def test_boundary_block_has_explicit_opt_in_option():
  assert (
    "--include-phase155-audits"
    in MODULE.BLOCK
  )


def test_boundary_block_deselects_by_exact_nodeid():
  assert (
    "normalized_nodeid"
    in MODULE.BLOCK
  )
  assert (
    "PHASE155_AUDIT_ONLY_NODEIDS"
    in MODULE.BLOCK
  )
  assert (
    "pytest_deselected"
    in MODULE.BLOCK
  )


def test_boundary_block_has_no_pytest_import():
  assert (
    "import pytest"
    not in MODULE.BLOCK
  )


def test_boundary_test_is_lightweight_and_count_based():
  assert (
    "23"
    in MODULE.BOUNDARY_TEST
  )
  assert (
    "test_phase144_"
    in MODULE.BOUNDARY_TEST
  )


def test_install_is_marker_idempotent():
  assert (
    MODULE.START
    in MODULE.BLOCK
  )
  assert (
    MODULE.END
    in MODULE.BLOCK
  )
