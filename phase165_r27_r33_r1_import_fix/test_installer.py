import ast

import pytest

from apply import apply, patch


BASE = '''from dataclasses import dataclass

@dataclass
class WebGroupProofView:
    n: int
    k: int

def build_standard_web_group_proof_view(n, k, max_depth=2, mode="narrative") -> WebGroupProofView:
    query = TodaGroupQuery(n=n, k=k)
    domain = classify_toda_group_query_domain(query)
    if domain.kind is TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
        from phase165_r52_r5_auto_search import search_group_structure_automatically
        search_group_structure_automatically(n=n, k=k)
    return WebGroupProofView(n, k)
'''


def test_r33_r1_restores_all_required_names():
    result, changed = patch(BASE)
    assert changed
    ast.parse(result)
    assert "from toda_group_query import TodaGroupQuery" in result
    assert "from toda_group_query_semantics import classify_toda_group_query_domain" in result
    assert "from toda_group_query_semantics import TodaGroupQueryDomainKind" in result


def test_r33_r1_keeps_existing_import_aliases_and_functions():
    src = "from toda_group_query import TodaGroupQuery\n" + BASE
    after, changed = patch(src)
    assert changed
    assert after.count("from toda_group_query import TodaGroupQuery") == 1
    assert "class WebGroupProofView" in after


def test_r33_r1_idempotence():
    after, _ = patch(BASE)
    again, changed = patch(after)
    assert not changed
    assert again == after


def test_r33_r1_rejects_legacy_function():
    src = "def build_standard_web_group_proof_view(n, k):\n    return build_standard_toda_report(n, k)\n"
    with pytest.raises(RuntimeError, match="typed search"):
        patch(src)


def test_r33_r1_backup_and_repeat(tmp_path):
    dest = tmp_path / "web_group_proof.py"
    dest.write_text(BASE, encoding="utf-8")
    apply(tmp_path)
    apply(tmp_path)
    assert (tmp_path / "phase165_r27_r33_r1_web_group_proof_backup.py.bak").exists()
    assert "from toda_group_query import TodaGroupQuery" in dest.read_text()
