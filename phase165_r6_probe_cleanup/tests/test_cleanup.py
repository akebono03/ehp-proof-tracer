import importlib.util
from pathlib import Path


def module_under_test():
    path = Path(__file__).resolve().parents[1] / "cleanup.py"
    spec = importlib.util.spec_from_file_location("r6_probe_cleanup", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_removes_unreferenced_failed_direct_probe_only(tmp_path):
    code = module_under_test()
    tests = tmp_path / "tests"
    tests.mkdir()
    candidate = tests / "test_phase50_probe.py"
    candidate.write_text("from probes.probe_phase50_capabilities import build\n", encoding="utf-8")
    untouched = tests / "test_other.py"
    untouched.write_text("def test_something(): pass\n", encoding="utf-8")
    triage = {"records": [{"test_path": "tests/test_phase50_probe.py", "detail": "toda_pi4_3_delta_image_free_cyclic_inference_rule"}]}
    plan = code.plan_cleanup(tmp_path, triage)
    assert plan["decisions"][0]["decision"] == "QUARANTINE"
    backup = tmp_path / "backup"
    code.perform(tmp_path, plan, backup)
    assert not candidate.exists()
    assert (backup / "tests/test_phase50_probe.py").exists()
    assert untouched.exists()


def test_keeps_imported_probe(tmp_path):
    code = module_under_test()
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_phase50_probe.py").write_text("from probes.probe_phase50_capabilities import build\n", encoding="utf-8")
    (tests / "test_active.py").write_text("from test_phase50_probe import build\n", encoding="utf-8")
    triage = {"records": [{"test_path": "tests/test_phase50_probe.py", "detail": "toda_pi4_3_delta_image_free_cyclic_inference_rule"}]}
    plan = code.plan_cleanup(tmp_path, triage)
    assert plan["decisions"][0]["decision"] == "KEEP"
    assert "IMPORTED_BY_OTHER_TESTS" in plan["decisions"][0]["reasons"]


def test_keeps_on_unparseable_test(tmp_path):
    code = module_under_test()
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_phase50_probe.py").write_text("from probes.probe_phase50_capabilities import build\n", encoding="utf-8")
    (tests / "test_corrupt.py").write_text("def broken(\n", encoding="utf-8")
    triage = {"records": [{"test_path": "tests/test_phase50_probe.py", "detail": "toda_pi4_3_delta_image_free_cyclic_inference_rule"}]}
    plan = code.plan_cleanup(tmp_path, triage)
    assert plan["decisions"][0]["decision"] == "KEEP"
