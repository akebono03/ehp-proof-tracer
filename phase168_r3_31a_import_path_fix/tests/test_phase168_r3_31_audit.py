from pathlib import Path
import importlib.util

AUDIT = Path(__file__).resolve().parents[1] / "audit.py"
spec = importlib.util.spec_from_file_location("phase168_r3_31_audit", AUDIT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_standard_entry_builds_model_and_calls_model_renderer():
    result = module.static_route_check()
    assert result["standard_entry_builds_linked_model"]
    assert result["model_renderer_called_by_adapter"]


def test_compatibility_routes_are_explicit_and_accounted_for():
    result = module.static_route_check()
    assert result["compatibility_path_still_present"]
    assert result["trace_path_uses_compatibility"]
    assert result["model_missing_uses_partial_markdown"]
