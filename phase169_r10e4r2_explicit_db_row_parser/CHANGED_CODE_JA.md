# 変更関数の全文

対象：`phase169_r10e4_ordered_db_prior/db_prior.py` の `_has_explicit_row()`。

変更後 import：**変更なし**。

```python
def _has_explicit_row(n: int, k: int, path: Path) -> bool:
    """Find an actual (n,k) row; skip the CSV's empty dimension separators.

    A row with a missing n/k is not a DB group. Malformed nonempty dimension
    fields fail closed rather than silently authorizing an unrelated result.
    This check does not use SphereRepository's stable-range fallback.
    """
    if not path.is_file():
        return False
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            rows = csv.DictReader(stream)
            if rows.fieldnames is None or not {"n", "k", "id"}.issubset(rows.fieldnames):
                return False
            for row in rows:
                raw_n = (row.get("n") or "").strip()
                raw_k = (row.get("k") or "").strip()
                if not raw_n or not raw_k:
                    continue
                if int(raw_n) == n and int(raw_k) == k:
                    return True
            return False
    except (OSError, UnicodeError, ValueError, TypeError, KeyError):
        return False
```

新規テストファイル全体は `tests/test_r10e4r2_db_separators.py` に収録。
