from pathlib import Path
import importlib.util


AUDIT_PATH = Path(
  "phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit"
) / "audit_phase148_rc2_4_repair_r4_1.py"


def _load_audit_module():
  spec = (
    importlib.util.spec_from_file_location(
      "phase148_r4_1_audit",
      AUDIT_PATH,
    )
  )
  assert spec is not None
  assert spec.loader is not None

  module = (
    importlib.util.module_from_spec(
      spec
    )
  )
  spec.loader.exec_module(
    module
  )
  return module


