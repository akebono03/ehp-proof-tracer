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
