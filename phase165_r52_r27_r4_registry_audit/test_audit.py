"""Focused read-only R27-R4 audit tests."""
from pathlib import Path
import ast

from audit import LOCATORS, EXPECTED_IDS, _matches


def test_r4_expected_literature_locators_are_distinct():
    assert LOCATORS == ("Proposition 4.4", "(5.2)")
    assert EXPECTED_IDS[LOCATORS[0]] != EXPECTED_IDS[LOCATORS[1]]


def test_r4_locator_matching_is_explicit():
    assert _matches("Toda Proposition 4.4", "Proposition 4.4")
    assert _matches("Toda (5.2)", "(5.2)")
    assert not _matches("Proposition 5.1", "Proposition 4.4")


def test_r4_read_only_audit_does_not_write_production_source():
    source = Path(__file__).with_name("audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    writes = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ("write_text", "write_bytes")]
    assert len(writes) == 2
    assert '"audit_output"' in source


def test_r4_provider_is_not_claimed_verified():
    source = Path(__file__).with_name("audit.py").read_text(encoding="utf-8")
    assert '"actual_backward_expansion_verified": False' in source
    assert '"reference_identity_semantically_verified": False' in source
