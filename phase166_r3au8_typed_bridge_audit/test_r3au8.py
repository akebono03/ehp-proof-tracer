from phase166_r3au8_typed_bridge_audit.audit import inspect, parse_ids


def test_r3au8_preserves_order_and_master_metadata():
    summary, rows = inspect(
        [{"n": "3", "k": "2", "id": "0", "Element": "8 5", "gen_coe": "1 0"}],
        [{"id": "5", "display": "η", "n": "3"}, {"id": "8", "display": "ν", "n": "4"}],
    )
    assert rows[0]["status"] == "IDS_RESOLVED_TYPING_UNVERIFIED"
    assert '"id": 8' in rows[0]["factor_metadata_json"]
    assert rows[0]["factor_metadata_json"].index('"id": 8') < rows[0]["factor_metadata_json"].index('"id": 5')
    assert rows[0]["composition_typed"] is False
    assert "n" in summary["master_columns"]


def test_r3au8_does_not_treat_generator_blank_as_failure():
    summary, rows = inspect(
        [{"n": "2", "k": "1", "id": "0", "Element": "3", "gen_coe": "1", "generator": ""}],
        [{"id": "3", "display": "η"}],
    )
    assert rows[0]["status"] == "IDS_RESOLVED_TYPING_UNVERIFIED"
    assert summary["typed_expression_certified"] == 0


def test_r3au8_unknown_ids_and_encoding_are_not_certified():
    summary, rows = inspect(
        [{"Element": "99", "gen_coe": "1"}, {"Element": "x", "gen_coe": "0"}],
        [{"id": "3", "display": "η"}],
    )
    assert [r["status"] for r in rows] == ["ID_LOOKUP_REVIEW", "INVALID_ELEMENT_IDS"]
    assert parse_ids("4 2") == [4, 2]
