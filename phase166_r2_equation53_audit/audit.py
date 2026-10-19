"""Read-only Phase 166 R2 inspection of the Toda (5.3) CSV rows and registry components."""
from __future__ import annotations
import csv
import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase166_r1_source_registry_audit.audit import classify


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def classify_53_row(row: dict[str, str]) -> str:
    left = row.get("composition", "").strip()
    right = row.get("rep_linear", "").strip()
    if left == r"\eta3^3" and right == r"2\nu'":
        return "EXACT_DISPLAY_PAIR_NOT_TYPED"
    if left and right:
        return "OTHER_DISPLAY_PAIR_NOT_TYPED"
    if left or right:
        return "INCOMPLETE_DISPLAY_PAIR"
    return "NO_DISPLAY_PAIR"


def inspect(rows: list[dict[str, str]], components: tuple) -> tuple[list[dict], dict]:
    selected = []
    for line, row in enumerate(rows, start=2):
        _category, locator = classify(row.get("reference", ""))
        if locator != "(5.3)":
            continue
        selected.append({
            "csv_line": line,
            "n": row.get("n", ""),
            "k": row.get("k", ""),
            "composition": row.get("composition", ""),
            "rep_linear": row.get("rep_linear", ""),
            "reference": row.get("reference", ""),
            "display_class": classify_53_row(row),
            "component_candidates": [getattr(c, "component_key") for c in components],
            "mathematical_identity_confirmed": False,
            "generator_typing_confirmed": False,
            "proof_permission_granted": False,
        })
    pairs = Counter((x["n"], x["k"], x["composition"], x["rep_linear"]) for x in selected)
    for x in selected:
        x["duplicate_display_count"] = pairs[(x["n"], x["k"], x["composition"], x["rep_linear"])]
    summary = {
        "phase": "166 R2 equation (5.3) inspection",
        "mode": "read_only",
        "selected_rows": len(selected),
        "display_classes": dict(sorted(Counter(x["display_class"] for x in selected).items())),
        "distinct_display_signatures": len(pairs),
        "component_keys": [c.component_key for c in components],
        "component_roles": {c.component_key: c.statement_role.value for c in components},
        "mathematical_identity_confirmed": 0,
        "proof_permission_granted": 0,
        "production_code_modified": False,
        "full_pytest_run": False,
    }
    return selected, summary


def main() -> int:
    from toda_literature_statement_boundary import _FIXED_COMPONENTS_BY_REFERENCE
    from phase165_r4_production_connection import discover_production_registry
    registry = discover_production_registry().bridge.registry
    components = _FIXED_COMPONENTS_BY_REFERENCE["(5.3)"]
    assert len(registry.assertions_for("toda:(5.3)")) == len(components), "Registry/component mismatch"
    paths = (ROOT / "sphere_relation2.csv", ROOT / "phase166_r1_source_registry_audit" / "sphere_relation2.csv")
    source = next((path for path in paths if path.is_file()), None)
    if source is None:
        raise FileNotFoundError("sphere_relation2.csv is absent")
    rows = load_rows(source)
    if len(rows) != 687:
        raise ValueError(f"Expected 687 rows, found {len(rows)}")
    details, summary = inspect(rows, components)
    if len(details) != 4:
        raise ValueError(f"Expected 4 Toda (5.3) rows, found {len(details)}")
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    with (out / "equation53_rows.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(details[0].keys()))
        writer.writeheader()
        for row in details:
            writer.writerow({key: json.dumps(val, ensure_ascii=False) if isinstance(val, list) else val for key, val in row.items()})
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
