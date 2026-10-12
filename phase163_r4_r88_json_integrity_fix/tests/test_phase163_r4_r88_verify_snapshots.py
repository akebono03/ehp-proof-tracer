import json
from pathlib import Path

import pytest

from phase163_r4_r88_verify_snapshots import validate_snapshot


def test_snapshot_accepts_formatting_difference(tmp_path):
    actual = tmp_path / "actual.json"
    snapshot = tmp_path / "snapshot.json"
    actual.write_text('{"records":[{"id":"x","n":1}],"phase":"R86"}\n', encoding="utf-8")
    snapshot.write_text(json.dumps({"phase": "R86", "records": [{"n": 1, "id": "x"}]}, indent=2), encoding="utf-8")
    validate_snapshot(actual, snapshot)


def test_snapshot_rejects_changed_field(tmp_path):
    actual = tmp_path / "actual.json"
    snapshot = tmp_path / "snapshot.json"
    actual.write_text('{"phase":"R87","proof_eligible":true}', encoding="utf-8")
    snapshot.write_text('{"phase":"R87","proof_eligible":false}', encoding="utf-8")
    with pytest.raises(ValueError, match="data mismatch"):
        validate_snapshot(actual, snapshot)


def test_snapshot_rejects_removed_record(tmp_path):
    actual = tmp_path / "actual.json"
    snapshot = tmp_path / "snapshot.json"
    actual.write_text('{"records":[]}', encoding="utf-8")
    snapshot.write_text('{"records":[{"id":"x"}]}', encoding="utf-8")
    with pytest.raises(ValueError, match="data mismatch"):
        validate_snapshot(actual, snapshot)


def test_snapshot_rejects_invalid_json(tmp_path):
    actual = tmp_path / "actual.json"
    snapshot = tmp_path / "snapshot.json"
    actual.write_text('{broken}', encoding="utf-8")
    snapshot.write_text('{}', encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        validate_snapshot(actual, snapshot)
