import ast
import csv
import json

import pytest

from phase163_r4_r5_semantic_triage import (
    FIELDS,
    inspect_sources,
    triage_site,
    write_report,
)


def sample(source, name="unknown"):
    tree = ast.parse(source)
    line = next(n.lineno for n in ast.walk(tree)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "InferenceRule")
    return triage_site({"line": line, "name": name}, tree, source)


def test_explicit_reference_is_candidate_not_confirmed():
    row = sample('''def build():
    s = SampleStatement()
    return InferenceRule(name="ref rule", literature_reference=LiteratureReference(locator="(5.7)"))
''')
    assert row["classification"] == "explicit_reference_candidate"
    assert row["reference_locator"] == "(5.7)"
    assert row["confidence"] == "candidate_only"
    assert row["statement_type"] == "SampleStatement"


def test_definition_name_is_only_hint():
    row = sample('''def build_definition():
    return InferenceRule(name="definition example")
''', "definition example")
    assert row["classification"] == "definition_candidate"
    assert row["definition_evidence"] == "name_hint_only"


def test_specialization_name_is_only_hint():
    row = sample('''def build_n():
    return InferenceRule(name="Toda finite-dimensional step")
''', "Toda finite-dimensional step")
    assert row["classification"] == "specialization_candidate"


def test_unresolved_statement_and_rule_are_separate():
    structured = sample('''def build():
    x = GroupStatement()
    return InferenceRule(name="unknown")
''')
    unresolved = sample('''def build():
    return InferenceRule(name="unknown")
''')
    assert structured["classification"] == "structured_rule_unresolved"
    assert unresolved["classification"] == "unresolved_rule"


def test_missing_sources_fails_closed(tmp_path):
    with pytest.raises(FileNotFoundError):
        write_report(tmp_path, tmp_path / "out")


def test_fake_sources_keep_counts_and_csv(tmp_path):
    from phase163_r4_r5_semantic_triage import RULE_FILES
    for name in RULE_FILES:
        content = '''def sample():
    return InferenceRule(name="unmapped")
''' if name == "toda_rules.py" else ""
        (tmp_path / name).write_text(content, encoding="utf-8")
    (tmp_path / "toda_literature_statement_boundary.py").write_text("", encoding="utf-8")
    result = inspect_sources(tmp_path)
    assert result["counts"]["toda_unmapped_sites"] == 1
    out = tmp_path / "output"
    summary = write_report(tmp_path, out)
    assert summary["counts"]["toda_unmapped_sites"] == 1
    with (out / "toda_rule_triage.csv").open(encoding="utf-8-sig", newline="") as f:
        records = list(csv.DictReader(f))
    assert len(records) == 1
    assert tuple(records[0]) == FIELDS
    assert json.loads((out / "summary.json").read_text(encoding="utf-8"))["full_pytest"] == "not_run"


def test_same_rule_name_keeps_distinct_source_sites(tmp_path):
    from phase163_r4_r5_semantic_triage import RULE_FILES
    for name in RULE_FILES:
        content = '''def one():
    return InferenceRule(name="same")
def two():
    return InferenceRule(name="same")
''' if name == "toda_rules.py" else ""
        (tmp_path / name).write_text(content, encoding="utf-8")
    (tmp_path / "toda_literature_statement_boundary.py").write_text("", encoding="utf-8")
    rows = inspect_sources(tmp_path)["rows"]
    assert len(rows) == 2
    assert len({row["site_id"] for row in rows}) == 2
