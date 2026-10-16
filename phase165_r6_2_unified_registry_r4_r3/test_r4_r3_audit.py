from dataclasses import dataclass

from phase165_r6_2_unified_registry_r4_r3.r4_r3_audit import fingerprint, enumerate_proposals, markdown


@dataclass(frozen=True)
class FakeRule:
    name: str


@dataclass(frozen=True)
class FakeExpansion:
    rule: FakeRule
    subgoals: tuple


@dataclass(frozen=True)
class FakeStep:
    conclusion: object


def test_fingerprint_is_stable():
    e = FakeExpansion(FakeRule("r"), (1,))
    assert fingerprint(e) == ("r", "(1,)")


def test_provenance_records_provider():
    e = FakeExpansion(FakeRule("r"), (1,))
    rows, errors = enumerate_proposals((2,), (("P", lambda _: (e,)),), (), {})
    assert rows[0]["provider_id"] == "P" and errors == []


def test_rule_id_without_registry_is_unresolved():
    e = FakeExpansion(FakeRule("r"), (1,))
    rows, _ = enumerate_proposals((2,), (("P", lambda _: (e,)),), (), {})
    assert rows[0]["rule_id_status"] == "UNRESOLVED"


def test_rule_id_from_registry_identity():
    r = FakeRule("r")
    rows, _ = enumerate_proposals((2,), (("P", lambda _: (FakeExpansion(r, (1,)),)),), (), {id(r): "m.factory"})
    assert rows[0]["rule_id"] == "m.factory"


def test_cited_premise_is_only_possible_witness():
    e = FakeExpansion(FakeRule("r"), (1,))
    rows, _ = enumerate_proposals((2,), (("SEEDED", lambda _: (e,)),), (("a", FakeStep(1)),), {})
    assert rows[0]["matching_cited_premise_ids"] == ["a"]
    assert rows[0]["witness_usage_status"] != "PROVEN_USED"


def test_overlap_is_goal_scoped():
    e = FakeExpansion(FakeRule("r"), (1,))
    rows, _ = enumerate_proposals((2, 3), (("A", lambda _: (e,)), ("B", lambda _: (e,))), (), {})
    assert len(rows) == 4
    assert all(len(row["overlap_providers"]) == 1 for row in rows)


def test_different_subgoals_do_not_overlap():
    rows, _ = enumerate_proposals((2,), (("A", lambda _: (FakeExpansion(FakeRule("r"), (1,)),)),
                                               ("B", lambda _: (FakeExpansion(FakeRule("r"), (3,)),))), (), {})
    assert all(not row["overlap_providers"] for row in rows)


def test_error_is_isolated():
    def bad(_):
        raise ValueError("probe")
    rows, errors = enumerate_proposals((2,), (("BAD", bad), ("GOOD", lambda _: ())), (), {})
    assert rows == [] and errors == [{"provider_id": "BAD", "error": "ValueError", "count": 1}]


def test_rejects_non_tuple_provider():
    _, errors = enumerate_proposals((2,), (("P", lambda _: []),), (), {})
    assert errors[0]["error"] == "TypeError"


def test_markdown_contains_status():
    assert "PROVENANCE_AUDITED" in markdown({"status": "PROVENANCE_AUDITED"})
