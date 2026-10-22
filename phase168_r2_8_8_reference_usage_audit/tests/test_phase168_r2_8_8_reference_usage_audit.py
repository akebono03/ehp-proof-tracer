from phase168_r2_8_8_reference_usage_audit.audit import entry_records, inspect


def test_entry_records_empty():
    assert entry_records(()) == []


def test_usage_audit_preserves_complete_root_and_reference_stages():
    report = inspect()
    assert report["search_status"] == "complete"
    assert len(report["raw_entries"]) >= 2
    assert len(report["fixed_entries"]) >= 2
    assert report["read_only"] is True


def test_empty_used_ids_eliminates_all_entries():
    report = inspect()
    assert report["empty_used_entries"] == []
