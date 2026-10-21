"""Read-only comparison of simple typed generator Goals with Element IDs."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re

import pandas as pd

from expression import HomotopyElement
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase166_r3af_goal_adapter import database_group_goal_candidates, database_zero_group_goal_candidates
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from repository import SphereRepository

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "results"
SIMPLE_LABEL = re.compile(r"^(η|ν|σ|ι)_?\{?(\d+)\}?(?:\^\{?([23])\}?)?$")
FAMILIES = {"η": 1, "ν": 3, "σ": 7, "ι": 0}


def selected_source(n: int, k: int) -> str:
    if database_zero_group_goal_candidates(n=n, k=k):
        return "zero"
    if k >= 2 and database_structured_group_goal_candidates(n=n, k=k):
        return "structured"
    if database_group_goal_candidates(n=n, k=k):
        return "simple"
    return "missing"


def compare_simple_component(*, n, k, component, generator_rows, typed_generator, source_n=None):
    """Return checked equality only for a fully recognized generator pattern."""
    result = {
        "db_name": component.generator,
        "element_ids": component.element,
        "typed_name": getattr(typed_generator, "name", None),
        "status": "unverifiable",
        "reason": None,
    }
    if not isinstance(typed_generator, HomotopyElement):
        result["reason"] = "typed_generator_not_atomic"
        return result
    if source_n is None:
        source_n = n if n <= k + 2 else k + 2
    match = SIMPLE_LABEL.fullmatch(component.generator.strip())
    if match is None:
        result["reason"] = "db_generator_label_not_simple"
        return result
    family, base_index, power = match.groups()
    if int(base_index) != source_n:
        result["status"] = "mismatch"
        result["reason"] = "db_index_not_source_dimension"
        return result
    exponent = int(power) if power else 1
    if power and family != "η":
        result["reason"] = "non_eta_power_not_supported"
        return result
    expected_ids = component.element
    if not expected_ids:
        result["reason"] = "missing_element_ids"
        return result
    if len(expected_ids) != exponent:
        result["status"] = "mismatch"
        result["reason"] = "factor_count_differs_from_label_exponent"
        return result
    cursor = n
    for identifier in expected_ids:
        if identifier not in generator_rows.index:
            result["status"] = "mismatch"
            result["reason"] = "unknown_element_id"
            return result
        row = generator_rows.loc[identifier]
        if not isinstance(row, pd.Series):
            result["reason"] = "duplicate_element_id"
            return result
        if (str(row["display"]).strip() != family or int(row["kinds"]) != 0
                or int(row["k"]) != FAMILIES[family] or cursor < int(row["n"])):
            result["status"] = "mismatch"
            result["reason"] = "element_id_family_or_degree_mismatch"
            return result
        cursor += int(row["k"])
    if cursor != n + k:
        result["status"] = "mismatch"
        result["reason"] = "total_stem_mismatch"
        return result
    expected_name = family + "_" + str(n) + ("^" + str(exponent) if exponent > 1 else "")
    if typed_generator.generator is not None:
        typed_ok = (exponent == 1 and typed_generator.generator.family == family
                    and typed_generator.generator.index == n
                    and typed_generator.generator.decoration is None)
    else:
        typed_ok = typed_generator.name == expected_name or (
            family == "η" and n == 2 and exponent == 1 and typed_generator.name == "η₂"
        )
    if (not typed_ok or typed_generator.source != n + k or typed_generator.target != n
            or typed_generator.dimension != n):
        result["status"] = "mismatch"
        result["reason"] = "typed_generator_identity_or_dimensions_mismatch"
        return result
    result["status"] = "confirmed"
    result["reason"] = "exact_family_factor_ids_dimensions_and_typed_identity"
    return result


def run():
    repo = SphereRepository(ROOT / "data" / "sphere.csv")
    gen = pd.read_csv(ROOT / "data" / "HyoujiGen.csv").set_index("id")
    records = []
    for n in range(2, 16):
        for k in range(8):
            if selected_source(n, k) != "simple":
                continue
            candidates = database_group_goal_candidates(n=n, k=k)
            components = repo.get_group(n, k).components
            direct_rows = repo.df[(repo.df["n"] == n) & (repo.df["k"] == k)]
            source_n = n if not direct_rows.empty else k + 2
            parts = ()
            if len(candidates) == 1:
                rhs = candidates[0].rhs
                parts = rhs.summands if isinstance(rhs, DirectSumGroup) else (rhs,)
            checks = []
            if len(parts) != len(components):
                status = "mismatch"
                checks.append({"status": "mismatch", "reason": "component_count_mismatch"})
            else:
                for component, part in zip(components, parts):
                    if not isinstance(part, (FiniteCyclicGroup, FreeCyclicGroup)):
                        checks.append({"status": "unverifiable", "reason": "unsupported_typed_component"})
                        continue
                    check = compare_simple_component(
                        n=n, k=k, component=component,
                        generator_rows=gen, typed_generator=part.generator, source_n=source_n,
                    )
                    checks.append(check)
                status = ("mismatch" if any(c["status"] == "mismatch" for c in checks)
                          else "confirmed" if all(c["status"] == "confirmed" for c in checks)
                          else "unverifiable")
            records.append({"n": n, "k": k, "status": status, "components": checks})
    summary = {
        "phase": "166-r3ap-simple-identity-audit",
        "simple_group_count": len(records),
        "status_counts": dict(Counter(record["status"] for record in records)),
        "component_status_counts": dict(Counter(check["status"] for record in records for check in record["components"])),
        "production_code_modified": False,
        "proof_search_executed": False,
        "scope": "strict simple-name identity against Element IDs and HyoujiGen rows; no ungrounded equivalence",
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "report.json").write_text(json.dumps({"summary": summary, "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Phase 166 R3-AP 単純生成元の同一性監査", "", "## 集計", "", "```json", json.dumps(summary, ensure_ascii=False, indent=2), "```", "", "## 28群の結果", ""]
    for record in records:
        lines.extend([f"### n={record['n']}, k={record['k']}: {record['status']}", ""])
        for check in record["components"]:
            lines.append(f"- {check.get('db_name', '?')} / IDs={check.get('element_ids', [])}: {check['status']} ({check['reason']})")
        lines.append("")
    (OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
    print("REPORT:", OUT / "report.json")
