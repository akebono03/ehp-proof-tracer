from pathlib import Path
from tempfile import TemporaryDirectory

from audit import SITES, audit, report


def test_eight_sites_have_stable_classifications():
    assert len(SITES) == 8
    assert sum(category == "fixed_literature_special_path_exception" for _, _, category in SITES) == 2
    assert sum(category == "shared_resolver_implementation" for _, _, category in SITES) == 2


def test_missing_sources_fail_closed():
    with TemporaryDirectory() as tmp:
        result = audit(Path(tmp))
    assert result["r7_status"] == "NOT_CLOSED"
    assert "site_inventory_drift" in result["blockers"]
    assert "unguarded_standard_entrypoint" in result["blockers"]


def test_report_marks_special_route_as_unclosed():
    with TemporaryDirectory() as tmp:
        output = report(audit(Path(tmp)))
    assert "NOT_CLOSED" in output
    assert "R7-R8" in output
