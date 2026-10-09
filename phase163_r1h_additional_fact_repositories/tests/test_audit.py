from types import SimpleNamespace

from phase163_r1h_additional_fact_repositories.audit import inspect_fact_repositories, write_report


def test_inspect_fact_repositories_counts_collections():
    modules = {
        "map_facts": SimpleNamespace(MAP_ISOMORPHISM_FACT_REPOSITORY=SimpleNamespace(facts=("a",))),
        "generator_facts": SimpleNamespace(GENERATOR_FACT_REPOSITORY=SimpleNamespace(typing_facts=("b", "c"), ambient_group_facts=("d",))),
    }
    rows, errors = inspect_fact_repositories(lambda name: modules[name])
    assert errors == []
    assert len(rows) == 4
    assert {row["collection"] for row in rows} == {"facts", "typing_facts", "ambient_group_facts"}


def test_write_report_records_counts(tmp_path):
    rows = [{"module": "map_facts", "repository": "MAP_ISOMORPHISM_FACT_REPOSITORY", "collection": "facts", "index": 0, "entry_type": "str", "entry_repr": "'a'"}]
    summary = write_report(tmp_path, rows, [])
    assert summary["counts_of_fact_instances"]["MAP_ISOMORPHISM_FACT_REPOSITORY.facts"] == 1
    assert (tmp_path / "fact_entries.csv").exists()
    assert "数学的命題の総数ではありません" in (tmp_path / "report.md").read_text(encoding="utf-8")
