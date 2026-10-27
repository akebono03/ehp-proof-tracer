# R10E4R4 — 変更コード全文

対象となる既存関数は次の5件です。**import の追加・変更はありません**。

- `phase169_r10e4_ordered_db_prior/db_prior.py`: `_has_explicit_row()`
- `phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py`: `test_r10e1_prior_citation_and_iso_required_for_direct_sum()`、`test_r10e1_zero_citation_absence_not_inferred_from_db()`、`test_r10e1_existing_finite_cyclic_route_keeps_compatibility()`
- `phase169_r10e2_unpositioned_citation/tests/test_r10e2_unpositioned_citation.py`: `test_r10e2_missing_publication_position_is_not_a_proof_source()`

追加する限定テストは `tests/test_r10e4r4_explicit_rows.py` にあり、新規ファイル全文を同梱しています。R10E4R2 実行時に今回の本番1ファイルの変更前バックアップ・変更関数全文・変更後ファイル全文を出力します。

## 本番関数

```python
def _has_explicit_row(n: int, k: int, path: Path) -> bool:
    """Detect a real group row without accepting malformed nonempty dimensions.

    Separator rows may omit n; every nonempty n/k field is validated before
    returning a match, including fields after a matching row. The scanner
    never uses SphereRepository's stable-range fallback.
    """
    if not path.is_file():
        return False
    try:
        found = False
        with path.open(encoding="utf-8-sig", newline="") as stream:
            rows = csv.DictReader(stream)
            if rows.fieldnames is None or not {"n", "k", "id"}.issubset(rows.fieldnames):
                return False
            for row in rows:
                if not isinstance(row, dict):
                    return False
                raw_n = row.get("n")
                raw_k = row.get("k")
                if raw_n is None or raw_k is None:
                    return False
                raw_n = raw_n.strip()
                raw_k = raw_k.strip()
                if not raw_k:
                    if raw_n:
                        return False
                    continue
                parsed_k = int(raw_k)
                if not raw_n:
                    continue
                parsed_n = int(raw_n)
                if parsed_n == n and parsed_k == k:
                    found = True
        return found
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, csv.Error):
        return False
```

## R10E2 テスト関数

```python
def test_r10e2_missing_publication_position_is_not_a_proof_source(monkeypatch):
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source, positioned=False), goal=goal,
    )
    # A citation without a publication position is not a screened GIVEN.
    assert screened.proof_links == ()
    assert uniquely_screened_prior_sources(screened, goal=goal, source_n=9) == ()
    # R10E4 independently authorizes the real earlier database group result.
    options = expand_prior_general_group_transport(
        goal, (_iso(9, 7, 3),), screened, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals[0] == source
    from phase169_r10e4_ordered_db_prior import db_prior
    monkeypatch.setattr(
        db_prior, "exact_prior_database_result", lambda *args, **kwargs: None,
    )
    # Without either a screened literature source or a real DB prior,
    # the transport candidate must disappear.
    assert expand_prior_general_group_transport(
        goal, (_iso(9, 7, 3),), screened, proof_target=goal,
    ) == ()
```

## R10E1 テスト関数1

```python
def test_r10e1_prior_citation_and_iso_required_for_direct_sum(monkeypatch):
    source, goal = _two_component(10), _two_component(12)
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    monkeypatch.setattr(universal, 'resolve_specialized_goal_citing_id',
                        lambda b, target: 'registered_target')
    calls = []

    def fake_prior(b, *, source_n, source_k, citing_assertion_id):
        calls.append((source_n, source_k, citing_assertion_id))
        if source_n == 10 and source_k == 8:
            return PriorGroupResult(10, 8, source, 'registered_target',
                                    'registered_prior', True, 'prior_fixed_source')
        return PriorGroupResult(source_n, source_k, None, 'registered_target',
                                None, False, 'db_result_missing')

    monkeypatch.setattr(universal, 'resolve_prior_group_result', fake_prior)
    assert universal.expand_prior_general_group_transport(
        goal, (), bridge, proof_target=goal,
    ) == ()
    options = universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=goal,
    )
    assert len(options) == 1
    assert len(options[0].subgoals) == 6
    assert options[0].subgoals[0] == source
    assert calls[0] == (10, 8, 'registered_target')
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=source,
    ) == ()
    monkeypatch.setattr(universal, 'resolve_specialized_goal_citing_id',
                        lambda b, target: None)
    # R10E4 permits an independent, earlier DB group without a target cite.
    db_options = universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=goal,
    )
    assert len(db_options) == 1
    assert db_options[0].subgoals[0] == source
    from phase169_r10e4_ordered_db_prior import db_prior
    monkeypatch.setattr(
        db_prior, 'exact_prior_database_result', lambda *args, **kwargs: None,
    )
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=goal,
    ) == ()
```

## R10E1 テスト関数2

```python
def test_r10e1_zero_citation_absence_not_inferred_from_db(monkeypatch):
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    goal = _zero(8, 4)
    # The real (n=6, k=4) DB zero result may be used even without a
    # separately registered proposition, but only as an adopted DB prior.
    options = universal.expand_prior_general_group_transport(
        goal, (_iso(6, 4, 2),), bridge, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals[0] == _zero(6, 4)
    from phase169_r10e4_ordered_db_prior import db_prior
    monkeypatch.setattr(
        db_prior, 'exact_prior_database_result', lambda *args, **kwargs: None,
    )
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(6, 4, 2),), bridge, proof_target=goal,
    ) == ()
```

## R10E1 テスト関数3

```python
def test_r10e1_existing_finite_cyclic_route_keeps_compatibility(monkeypatch):
    source = _relation(5, 3, FiniteCyclicGroup(8, _element(4, 5)))
    goal = _relation(7, 3, FiniteCyclicGroup(8, _element(4, 7)))
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    import phase169_r7_general_stable_transport.rule as old
    seen = []

    def fake(old_goal, available, old_bridge, *, proof_target):
        seen.append((old_goal, proof_target))
        return ()

    monkeypatch.setattr(old, 'expand_prior_general_stable_transport', fake)
    # R7 is still tried first; when it offers nothing, the authorized
    # R10E4 DB prior may supply the identical typed source obligation.
    options = universal.expand_prior_general_group_transport(
        goal, (_iso(5, 3, 2),), bridge, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals[0] == source
    assert seen == [(goal, goal)]
    from phase169_r10e4_ordered_db_prior import db_prior
    monkeypatch.setattr(
        db_prior, 'exact_prior_database_result', lambda *args, **kwargs: None,
    )
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(5, 3, 2),), bridge, proof_target=goal,
    ) == ()
    assert seen == [(goal, goal), (goal, goal)]
```

## 追加テスト（新規ファイル全文）

```python
"""R10E4R4 targeted checks for fail-closed CSV scanning."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from phase169_r10e4_ordered_db_prior.db_prior import _has_explicit_row


def _write(path: Path, rows: tuple[dict, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("n", "k", "id"))
        writer.writeheader()
        writer.writerows(rows)


@pytest.mark.parametrize("invalid,at_start", (
    ({"n": "bad", "k": "7", "id": "3"}, True),
    ({"n": "bad", "k": "7", "id": "3"}, False),
    ({"n": "3", "k": "bad", "id": "3"}, True),
    ({"n": "3", "k": "bad", "id": "3"}, False),
))
def test_r10e4r4_rejects_malformed_nonempty_dimensions_anywhere(
    tmp_path: Path, invalid: dict, at_start: bool,
) -> None:
    row = {"n": "9", "k": "7", "id": "0"}
    ordered = (invalid, row) if at_start else (row, invalid)
    path = tmp_path / "sphere.csv"
    _write(path, ordered)
    assert not _has_explicit_row(9, 7, path)


def test_r10e4r4_valid_separator_and_valid_match(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    _write(path, (
        {"n": "", "k": "6", "id": ""},
        {"n": "9", "k": "7", "id": "0"},
        {"n": "", "k": "8", "id": "2"},
    ))
    assert _has_explicit_row(9, 7, path)
    assert not _has_explicit_row(10, 7, path)
```
