"""Phase 166 R2: read-only group/individual assertion correspondence."""
from __future__ import annotations
import csv
import json
from pathlib import Path

FOCUS = (
    (2, 1, "Proposition 5.1", "pi3_2_group_relation", "pi_3^2"),
    (3, 1, "Proposition 5.1", "higher_eta_group_relation", "pi_4^3"),
    (3, 2, "Proposition 5.3", "pi5_3_group_relation", "pi_5^3"),
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def inspect(sphere_rows: list[dict[str, str]], generator_rows: list[dict[str, str]], bridge: object) -> dict:
    ids = {str(row["id"]): row for row in generator_rows}
    results = []
    for n, k, locator, component_key, goal in FOCUS:
        rows = [row for row in sphere_rows if row.get("n") == str(n) and row.get("k") == str(k)]
        if not rows:
            raise ValueError(f"missing sphere rows for {goal}")
        assertion_id = f"boundary:{locator}:{component_key}"
        assertion = bridge.registry.assertion(assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        component = assertion.content
        if (getattr(component, "component_key", None) != component_key
                or getattr(component, "reference_locator", None) != locator
                or reference.locator != locator):
            raise ValueError("inconsistent registry component identity")
        components = []
        for row in rows:
            raw_ids = row.get("Element", "").split()
            if any(i not in ids for i in raw_ids):
                raise ValueError(f"unknown generator ID in {goal}")
            components.append({
                "component_id": row.get("id"),
                "order_as_recorded": row.get("orders"),
                "generator_as_recorded": row.get("generator"),
                "element_ids": raw_ids,
                "base_generator_display": [ids[i].get("display", "") for i in raw_ids],
            })
        results.append({
            "goal": goal, "n": n, "k": k,
            "assertion_id": assertion_id,
            "registry_content_type": type(component).__name__,
            "reference_locator": reference.locator,
            "statement_role": getattr(getattr(component, "statement_role", None), "value", None),
            "component_count": len(components), "components": components,
            "correspondence": "METADATA_COMPONENT_CANDIDATE_ONLY",
            "group_identity_confirmed": False,
            "proof_permission_granted": False,
        })
    return {
        "phase": "166 R2 three group correspondence",
        "read_only": True,
        "source_rows": len(sphere_rows),
        "generator_rows": len(generator_rows),
        "target_count": len(results),
        "targets": results,
        "mathematical_identity_confirmed": 0,
        "proof_permission_granted": 0,
        "proof_links_created": 0,
        "production_code_modified": False,
        "full_pytest_run": False,
    }


def main() -> None:
    from phase165_r4_production_connection import discover_production_registry
    root = Path(__file__).resolve().parent
    repo = root.parent
    def locate(name: str) -> Path:
        for candidate in (repo / name, repo / "data" / name, root / "data" / name):
            if candidate.is_file():
                print(f"INPUT {name}: {candidate}")
                return candidate
        raise FileNotFoundError(f"cannot find {name}")
    bridge = discover_production_registry().bridge
    result = inspect(read_rows(locate("sphere(3).csv")), read_rows(locate("HyoujiGen.csv")), bridge)
    folder = root / "results"
    folder.mkdir(exist_ok=True)
    (folder / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
