from audit import report

def test_non_mutating_stage_audit():
    output=report()
    assert output["sources_modified"] is False
    assert output["full_pytest_run"] is False

def test_three_exactness_inferences_visible():
    output=report()
    assert len(output["exactness_proofsteps"])==3

def test_stage_data_preserved():
    output=report()
    assert "linked" in output["stages"]
    assert "final" in output["stages"]
    assert "final_relinked" in output["stages"]
