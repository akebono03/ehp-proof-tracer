from phase166_r3t_specialization_connection.audit import inspect


def test_general_toda45_source_is_present():
    report=inspect()
    assert report["symbolic_toda45_given_count"] >= 1
    assert not report["production_code_modified"]


def test_concrete_specialization_is_real_inference_candidate():
    report=inspect()
    assert report["concrete_iso_specialization_candidates"] >= 1
    assert not report["concrete_iso_is_given"]
    assert any(entry["bindings"] is not None
               for entry in report["source_binding_results"])


def test_no_unjustified_named_eta_generator_transport():
    report=inspect()
    assert report["named_eta_transport_requires_separate_generator_proof"]
    assert not report["full_pytest_run"]
