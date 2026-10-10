"""Phase 163 R4-R4: conservative, read-only classification of rule sites.

All categories are evidence classes, not claims of mathematical equivalence.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path



FIELDS = ("file", "line", "rule_name", "mapping_status", "role_candidate",
          "evidence", "manual_review_required")


def classify_site(site: dict[str, object]) -> dict[str, object]:
    filename = str(site["file"])
    name = site.get("name")
    status = str(site["status"])
    if status == "listed_in_boundary_mapping":
        role = "literature_mapping_candidate"
        evidence = "rule name explicitly listed in boundary mapping"
    elif name is None or not str(name).strip():
        role = "dynamic_rule_name_unverified"
        evidence = "literal inference-rule name unavailable"
    elif filename == "toda_rules.py":
        role = "toda_rule_unclassified"
        evidence = "Toda rule name absent from boundary mapping"
    else:
        role = "general_inference_candidate"
        evidence = "non-Toda rule name absent from boundary mapping"
    return {"file": filename, "line": int(site["line"]),
            "rule_name": "" if name is None else str(name),
            "mapping_status": status, "role_candidate": role,
            "evidence": evidence, "manual_review_required": "yes"}


def classify_unlinked(component: dict[str, object]) -> dict[str, object]:
    return {"locator": str(component["locator"]),
            "component_key": str(component["key"]),
            "statement_role": str(component["role"]),
            "status": "unlinked_by_literal_name",
            "next_check": "inspect rule builders, structural statements and aliases",
            "mathematical_equivalence_confirmed": "no"}


def build_classification(mapping: dict[str, object]) -> dict[str, object]:
    sites = [classify_site(site) for site in mapping["rule_sites"]]
    unlinked = [classify_unlinked(item) for item in mapping["unlinked_components"]]
    names = {s["rule_name"] for s in sites if s["rule_name"]}
    todo = [s for s in sites if s["file"] == "toda_rules.py"
            and s["mapping_status"] == "not_listed_in_boundary_mapping"]
    return {"sites": sites, "unlinked": unlinked, "toda_unmapped": todo,
            "counts": {"total_sites": len(sites),
                       "role_candidates": dict(sorted(Counter(s["role_candidate"] for s in sites).items())),
                       "toda_unmapped_literal_sites": len(todo),
                       "unlinked_components": len(unlinked),
                       "distinct_literal_rule_names": len(names)}}


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_audit(root: Path, output: Path) -> dict[str, object]:
    """Use the checked-in R4-R3 scanner, not a copied heuristic."""
    boundary_path = root / "toda_literature_statement_boundary.py"
    rule_names = ("toda_rules.py", "hopf_rules.py", "stable_rules.py",
                  "ehp_rules.py", "scalar_rules.py", "relation_rules.py", "set_rules.py")
    missing = [name for name in ("toda_literature_statement_boundary.py", *rule_names)
               if not (root / name).is_file()]
    if missing:
        raise FileNotFoundError("required source files absent: " + ", ".join(missing))
    import phase163_r4_r3_statement_mapping as prior
    sources = {name: (root / name).read_text(encoding="utf-8-sig") for name in rule_names}
    mapping = prior.analyze(boundary_path.read_text(encoding="utf-8-sig"), sources)
    result = build_classification(mapping)
    output.mkdir(parents=True, exist_ok=True)
    _write_csv(output / "role_candidates.csv", FIELDS, result["sites"])
    _write_csv(output / "toda_unmapped.csv", FIELDS, result["toda_unmapped"])
    _write_csv(output / "unlinked_review.csv",
               ("locator", "component_key", "statement_role", "status", "next_check",
                "mathematical_equivalence_confirmed"), result["unlinked"])
    summary = {"audit": "Phase 163 R4-R4 conservative role classification",
               "counts": result["counts"], "source_files": list(rule_names),
               "missing_sources": missing,
               "limitations": [
                   "Role labels are candidates only, not verified theorem identities.",
                   "A constructor site is not an instantiated rule or a unique statement.",
                   "A non-Toda rule is not necessarily generic mathematics.",
                   "Unlisted Toda rules can be fixed statements, specializations, or helper rules.",
                   "No automatic conversion into Unified Statement Registry is performed.",
                   "Definitions and runtime registrations are not exhaustively audited.",
                   "Publication and proof-completion order remain unknown.",
                   "No proof search, renderer, or existing API is modified.",
               ]}
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R4 — 数学的役割候補の分類監査", "",
             "## 候補数（命題数ではない）", "",
             f"- InferenceRule 生成箇所: {result['counts']['total_sites']}",
             f"- toda_rules.py の未掲載候補: {result['counts']['toda_unmapped_literal_sites']}",
             f"- 明示規則名への対応がない文献 component: {result['counts']['unlinked_components']}", "",
             "## 分類", ""]
    lines.extend(f"- {k}: {v}" for k, v in result["counts"]["role_candidates"].items())
    lines.extend(["", "## 制約", ""])
    lines.extend(f"- {s}" for s in summary["limitations"])
    lines.extend(["", "**全命題の統合・数学的同一性検証は未完了。**", "全体 pytest は未実施。", ""])
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path.cwd() / "phase163_r4_r4_output")
    args = parser.parse_args()
    summary = write_audit(args.root, args.output)
    print("Phase 163 R4-R4 read-only role classification:", summary["counts"])
    print("Saved:", args.output / "report.md")
    print("No existing source changes; full pytest suite not run.")


if __name__ == "__main__":
    main()
