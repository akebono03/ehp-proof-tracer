from pathlib import Path

from phase166_r3au11_public_connection_audit.audit import audit


def test_registered_selector_calls_db_typed_goal():
    data = audit(Path(__file__).resolve().parent.parent)
    assert data["checks"]["selector_calls_structured_db_goal"]
    assert data["checks"]["selector_uses_structured_for_k_ge_2"]


def test_search_entry_uses_registered_selector():
    data = audit(Path(__file__).resolve().parent.parent)
    assert data["checks"]["search_calls_registered_selector"]
    assert data["checks"]["search_uses_shared_goal_search"]


def test_existing_generator_combinations_render():
    data = audit(Path(__file__).resolve().parent.parent)
    example = next(row for row in data["examples"] if (row["n"], row["k"]) == (10, 18))
    assert example["candidate_count"] == 1
    assert example["rendered"]
    assert r"\xi" in example["latex"]
