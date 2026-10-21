"""Phase 166 R3-AN: read-only generator notation audit over 112 targets."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import re

from repository import SphereRepository
from phase166_r3af_goal_adapter import database_group_goal_candidates, database_zero_group_goal_candidates
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from toda_human_readable_renderer import render_toda_public_group_relation_latex
from expression import Composition, HomotopyElement, IteratedSuspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "results"
E_ONE = re.compile(r"E\^\{?1\}?")


def _components(expression):
    if isinstance(expression, DirectSumGroup):
        return tuple(expression.summands)
    return (expression,)


def _generator(component):
    if isinstance(component, (FiniteCyclicGroup, FreeCyclicGroup)):
        return component.generator
    return None


def _nodes(expression):
    if isinstance(expression, Composition):
        yield from _nodes(expression.left)
        yield from _nodes(expression.right)
    else:
        yield expression


def _database_goal(n, k):
    zero = database_zero_group_goal_candidates(n=n, k=k)
    if zero:
        return "zero", zero[0]
    if k >= 2:
        structured = database_structured_group_goal_candidates(n=n, k=k)
        if structured:
            return "structured", structured[0]
    simple = database_group_goal_candidates(n=n, k=k)
    if simple:
        return "simple", simple[0]
    return "missing", None


def run():
    repo = SphereRepository(ROOT / "data" / "sphere.csv")
    records = []
    for n in range(2, 16):
        for k in range(8):
            source, statement = _database_goal(n, k)
            issues = []
            latex = None
            if statement is None:
                issues.append("missing_typed_goal")
            else:
                latex = render_toda_public_group_relation_latex(statement)
                if not latex:
                    issues.append("missing_latex")
                else:
                    if not latex.startswith(r"\pi_{" + str(n+k) + "}^{" + str(n) + "} ="):
                        issues.append("wrong_target")
                    if E_ONE.search(latex):
                        issues.append("unnecessary_E_power_one")
                    if "\\" not in latex:
                        issues.append("unescaped_math")
            rows = repo._rows(n, k)
            ids = []
            labels = []
            if not rows.empty:
                for _, row in rows.iterrows():
                    ids.append(repo._parse_int_list(row["Element"]))
                    labels.append(repo._parse_text(row["generator"]))
            kinds = Counter()
            if source != "zero" and statement is not None and hasattr(statement, "rhs"):
                for component in _components(statement.rhs):
                    gen = _generator(component)
                    if gen is None:
                        issues.append("unrecognized_group_component")
                        continue
                    for node in _nodes(gen):
                        if isinstance(node, IteratedSuspension):
                            kinds["suspension"] += 1
                        elif isinstance(node, HomotopyElement):
                            kinds["atomic"] += 1
                        else:
                            kinds["other"] += 1
                    if isinstance(gen, Composition):
                        kinds["composition"] += 1
            # Legacy relation2.py generated stable ordinary generators from
            # HyoujiGen rows and dimension offsets. This is a structural
            # audit; it does not treat CSV generator labels as proof evidence.
            if source == "structured" and any(not ids_one for ids_one in ids):
                issues.append("structured_without_element_ids")
            records.append({
                "n": n, "k": k, "source": source, "latex": latex,
                "db_generators": labels, "element_ids": ids,
                "expression_kinds": dict(kinds), "issues": issues,
            })
    source_counts = dict(Counter(r["source"] for r in records))
    issue_counts = dict(Counter(issue for r in records for issue in r["issues"]))
    summary = {
        "phase": "166-r3an-generator-notation-audit",
        "count": len(records), "source_counts": source_counts,
        "issue_counts": issue_counts,
        "pass": sum(not r["issues"] for r in records),
        "production_code_modified": False,
        "proof_search_executed": False,
        "scope": "structural consistency and LaTeX output; not full mathematical equivalence or browser rendering",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "report.json").write_text(json.dumps({"summary": summary, "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Phase 166 R3-AN 生成元表記監査", "", "## 集計", "", "```json", json.dumps(summary, ensure_ascii=False, indent=2), "```", "", "## 個別表示", ""]
    for r in records:
        issues = ", ".join(r["issues"]) if r["issues"] else "OK"
        lines.extend([f"### n={r['n']}, k={r['k']} — {r['source']} / {issues}", "", f"DB: `{r['db_generators']}`", "", "```tex", r["latex"] or "(missing)", "```", ""])
    (OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
    print("REPORT:", OUT / "report.json")
