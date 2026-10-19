from phase165_r6_error_triage.triage import build_report, parse_collection_log


def test_parse_collection_error_with_path():
    log = "___ ERROR collecting tests/test_example.py ___\nE   ModuleNotFoundError: No module named 'repository_inference'\n"
    assert parse_collection_log(log) == [{"test_path": "tests/test_example.py", "exception_type": "ModuleNotFoundError", "detail": "No module named 'repository_inference'"}]


def test_classification_keeps_each_failure():
    log = "___ ERROR collecting tests/test_a.py ___\nE   ModuleNotFoundError: No module named 'repository_inference'\n___ ERROR collecting tests/test_b.py ___\nE   ImportError: cannot import name 'toda_pi4_3_delta_image_free_cyclic_inference_rule' from 'toda_rules'\n"
    report = build_report(log)
    assert report["total_collection_errors"] == 2
    assert sum(group["count"] for group in report["summary"]) == 2
    assert report["status"] == "CLASSIFIED_NOT_RESOLVED"
