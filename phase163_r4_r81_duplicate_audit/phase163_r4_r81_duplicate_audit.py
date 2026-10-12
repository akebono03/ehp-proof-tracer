"""R81: inspect existing live literature-boundary identities before registration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

OWNERS = {
    "prop:1-6": ("Proposition 1.6", "proposition"),
    "thm:2.4": ("Theorem 2.4", "theorem"),
    "prop:2.5": ("Proposition 2.5", "proposition"),
    "prop:4.2": ("Proposition 4.2", "proposition"),
}
ALIASES = {"prop:4.2": ["(4.4)"]}


def audit(preflight: dict, catalog: dict, bridge) -> dict:
    if preflight.get("phase") != "163 R4-R80":
        raise ValueError("R80 preflight input required")
    rows = preflight.get("records")
    if not isinstance(rows, list) or len(rows) != 8:
        raise ValueError("eight R80 records required")
    if preflight.get("production_registry_modified") is not False:
        raise ValueError("R80 input unexpectedly reports production changes")
    by_owner = {}
    for row in rows:
        owner = row["owner"]
        if owner not in OWNERS or row.get("registration_allowed") is not False:
            raise ValueError("unexpected owner or registration flag")
        if row.get("permanent_id_allocated") is not False:
            raise ValueError("unexpected permanent ID")
        by_owner.setdefault(owner, []).append(row)
    if set(by_owner) != set(OWNERS):
        raise ValueError("missing owner")
    results = []
    for owner, (locator, kind) in OWNERS.items():
        items = sorted(by_owner[owner], key=lambda r: r["component_position"])
        if [r["component_position"] for r in items] != list(range(1, len(items) + 1)):
            raise ValueError("invalid component order")
        try:
            current = bridge.registry.reference("toda:" + locator)
        except KeyError:
            current = None
        existing_components = catalog.get(locator, ())
        alias_details = []
        for alias in ALIASES.get(owner, ()):
            alias_details.append({"locator": alias, "existing_boundary_component_count": len(catalog.get(alias, ())),
                                  "embedded_in_reference": locator, "requires_alias_reconciliation": True})
        results.append({
            "owner": owner, "locator": locator, "kind": kind,
            "proposed_assertion_count": len(items),
            "proposed_component_positions": [r["component_position"] for r in items],
            "existing_boundary_component_count": len(existing_components),
            "live_bridge_reference_found": current is not None,
            "existing_bridge_assertion_count": len(bridge.registry.assertions_for("toda:" + locator)) if current is not None else 0,
            "alias_review": alias_details,
            "scope_or_boundary_issue_count": sum(len(r.get("boundary_issues", ())) for r in items),
            "duplicate_conclusion": "LOCATOR_ALREADY_PRESENT" if current is not None else "NO_EXACT_LOCATOR_IN_BOUNDARY_BRIDGE",
            "semantic_nonduplication_verified": False,
            "registration_allowed": False,
        })
    return {
        "phase": "163 R4-R81", "mode": "READ_ONLY_LIVE_BOUNDARY_BRIDGE_DUPLICATE_AUDIT",
        "reference_candidate_count": len(results), "fixed_statement_candidate_count": len(rows),
        "exact_locator_overlap_count": sum(r["live_bridge_reference_found"] for r in results),
        "embedded_equation_alias_review_count": sum(len(r["alias_review"]) for r in results),
        "semantic_duplicate_verification_count": 0,
        "semantic_registration_allowed_count": 0, "original_edition_verified": False,
        "production_registry_modified": False, "production_ids_allocated": False,
        "proof_search_connected": False, "full_suite_run": False, "records": results,
    }


def run(root: Path, output: Path) -> dict:
    import sys
    sys.path.insert(0, str(root))
    from phase163_r4_registry_bridge import build_registry_bridge
    from toda_literature_statement_boundary import _FIXED_COMPONENTS_BY_REFERENCE
    from theorem_facts import THEOREM_FACT_REPOSITORY
    source = root / "phase163_r4_r80_output" / "registration_preflight.json"
    preflight = json.loads(source.read_text(encoding="utf-8-sig"))
    bridge = build_registry_bridge(
        components_by_reference=_FIXED_COMPONENTS_BY_REFERENCE,
        theorem_facts=THEOREM_FACT_REPOSITORY,
    )
    result = audit(preflight, _FIXED_COMPONENTS_BY_REFERENCE, bridge)
    output.mkdir(parents=True, exist_ok=True)
    (output / "duplicate_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R81：既存境界台帳との重複照合", "",
             "現行の文献境界台帳と Registry Bridge の実体を使用した読み取り専用照合。", "",
             "| Reference | 本文候補 | 既存の同一 locator | 別名確認 |", "|---|---:|---|---|"]
    for row in result["records"]:
        lines.append(f'| {row["locator"]} | {row["proposed_assertion_count"]} | {"あり" if row["live_bridge_reference_found"] else "なし"} | {", ".join(x["locator"] for x in row["alias_review"]) or "—"} |')
    lines.extend(["", "locator の不一致は数学的非重複の証明ではない。", "既存 rule・proof repository・他の未移行候補との意味的照合は残る。", "正式 ID・Registry・証明探索への変更なし。全体 pytest 未実施。"])
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("phase163_r4_r81_output"))
    args = parser.parse_args()
    result = run(args.root, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, ensure_ascii=False, indent=2))
    print("R81 live duplicate audit complete. Full pytest not run.")


if __name__ == "__main__":
    main()
