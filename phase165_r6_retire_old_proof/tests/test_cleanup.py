from cleanup import eligible, removable_set

def test_only_historical_proof_errors_eligible():
    assert eligible({"file":"tests/test_phase159_pi4_3_exactness_reason_unification.py", "category":"MISSING_SHARED_TEST_HELPER"})
    assert not eligible({"file":"tests/test_phase164_r4_real_registry_audit.py", "category":"RETIRED_PROBE_RULE"})
    assert not eligible({"file":"tests/test_phase65_pi5_2_eta2_cube.py", "category":"RETIRED_PROBE_RULE"})

def test_dependency_protects_imported_test(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    old = tests / "test_phase159_old.py"
    newer = tests / "test_phase165_current.py"
    old.write_text("def f():\n    return 1\n", encoding="utf8")
    newer.write_text("from tests.test_phase159_old import f\n", encoding="utf8")
    files = {"tests/" + p.name:p for p in [old,newer]}
    remove, _ = removable_set([{"file":"tests/test_phase159_old.py", "category":"MISSING_SHARED_TEST_HELPER"}], files)
    assert not remove

def test_independent_historical_file_can_retire(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    old = tests / "test_phase159_old.py"
    old.write_text("def f():\n    return 1\n", encoding="utf8")
    remove, _ = removable_set([{"file":"tests/test_phase159_old.py", "category":"MISSING_SHARED_TEST_HELPER"}], {"tests/test_phase159_old.py":old})
    assert remove == {"tests/test_phase159_old.py"}
