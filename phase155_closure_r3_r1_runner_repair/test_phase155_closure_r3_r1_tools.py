import ast
from pathlib import Path

from phase155_closure_r3_r1_validate import (
  main as validate_main,
)


def test_fixed_runner_parses_as_python():
  path = (
    Path(
      __file__
    ).parent
    / "run_phase155_closure_r3_fixed.py"
  )

  ast.parse(
    path.read_text(
      encoding="utf-8"
    )
  )


def test_fixed_runner_has_timeout_exception_handler():
  path = (
    Path(
      __file__
    ).parent
    / "run_phase155_closure_r3_fixed.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  assert (
    "except subprocess.TimeoutExpired:"
    in text
  )


def test_fixed_runner_keeps_checkpoint_skip():
  path = (
    Path(
      __file__
    ).parent
    / "run_phase155_closure_r3_fixed.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  assert "already PASS, skipping." in text
  assert 'checkpoint.json' in text


def test_fixed_runner_keeps_ten_minute_default():
  path = (
    Path(
      __file__
    ).parent
    / "run_phase155_closure_r3_fixed.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  assert "default=600" in text


def test_plugin_excludes_audit_only_manifest():
  path = (
    Path(
      __file__
    ).parent
    / "phase155_shard_plugin.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  assert "phase155_audit_only_nodeids.txt" in text
  assert "pytest_deselected" in text
