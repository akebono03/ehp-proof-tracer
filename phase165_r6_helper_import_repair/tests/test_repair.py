from repair import analyze_candidate, remove_unused_import


def test_unused_retired_import_can_be_removed():
    source = 'from toda_calculation_facade import build_standard_toda_report\n\ndef _method_evidence_data():\n    return 1\n'
    new, reason = remove_unused_import(source)
    assert new == '\ndef _method_evidence_data():\n    return 1\n'
    assert 'unused' in reason


def test_active_retired_call_must_not_be_rewritten():
    source = 'from toda_calculation_facade import build_standard_toda_report\n\ndef _method_evidence_data():\n    return build_standard_toda_report(3, 1)\n'
    new, reason = remove_unused_import(source)
    assert new is None
    assert 'actively referenced' in reason


def test_candidate_analysis_reports_call_sites():
    source = 'from toda_calculation_facade import build_standard_toda_report\n\ndef _method_evidence_data():\n    return build_standard_toda_report(3, 1)\n'
    details = analyze_candidate(source)
    assert details['old_calls'] == [4]
    assert details['helper_exists']
