"""R3-36D narrow audit contract checks."""
import json
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / "output" / "audit.json"


def test_report_is_observational():
    result = json.loads(REPORT.read_text(encoding="utf-8"))
    assert result["mode"] == "AUDIT_ONLY"
    assert result["goal"] == "pi_5^4"
    assert isinstance(result["given_steps"], list)


def test_report_provides_both_link_views():
    result = json.loads(REPORT.read_text(encoding="utf-8"))
    for step in result["given_steps"]:
        assert isinstance(step["original_links"], list)
        assert isinstance(step["screened_links"], list)
        assert isinstance(step["original_citations"], list)
        assert isinstance(step["screened_citations"], list)
        assert all(link["relation"] in ("exact", "same_conclusion")
                   for link in step["screened_links"])
