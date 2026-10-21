from __future__ import annotations

import json
from pathlib import Path
from dataclasses import fields, is_dataclass

from proof import ProofRule, Relation, RelationType
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r10_step_narrative import ordered_proof_ancestry
from toda_group_proof_narrative_shared_components import _render_generic_narrative_step
from web_group_proof import build_standard_web_group_proof_view

OUT = Path(__file__).resolve().parent


def summary(obj):
    data = {"type": type(obj).__module__ + "." + type(obj).__qualname__, "repr": repr(obj)[:1800]}
    if is_dataclass(obj):
        data["fields"] = {f.name: {"type": type(getattr(obj, f.name)).__name__, "repr": repr(getattr(obj, f.name))[:500]} for f in fields(obj)}
    return data


def main():
    result = search_group_from_registered_goal(n=3, k=1)
    roots = [s for s in result.proven_steps if s.conclusion == result.conclusion]
    if len(roots) != 1:
        raise RuntimeError("Expected one completed pi4^3 proof root")
    steps = ordered_proof_ancestry(roots[0])
    rows = []
    for index, step in enumerate(steps):
        try:
            rendered = _render_generic_narrative_step(step)
        except (TypeError, ValueError) as exc:
            rendered = "ERROR: " + str(exc)
        statement = step.conclusion
        rule = getattr(step.inference_rule, "name", None)
        selected = (
            "eta" in rendered.lower()
            or "\\eta" in rendered
            or "η" in rendered
            or "suspension" in str(rule).lower()
            or type(statement).__name__ in ("GeneratorImage", "GeneratorSuspension")
            or isinstance(statement, Relation) and statement.relation_type is RelationType.EQUALITY
        )
        if selected:
            rows.append({
                "index": index,
                "rule_kind": str(step.rule),
                "rule_name": rule,
                "conclusion": summary(statement),
                "rendered": rendered,
                "premise_indices": [next((j for j, item in enumerate(steps) if item is p), None) for p in step.premises],
            })
    view = build_standard_web_group_proof_view(3, 1, 2, "narrative")
    lines = [line if isinstance(line, str) else str(getattr(line, "prefix", "")) + str(getattr(line, "statement_latex", "") or "") + str(getattr(line, "suffix", "")) for line in view.rendered_lines]
    (OUT / "pi4_3_before.txt").write_text("\n".join(lines), encoding="utf-8")
    report = {"status": str(result.status), "proof_steps": len(steps), "selected_steps": rows, "web_lines": len(lines), "proof_modifications": False}
    (OUT / "typed_equality_audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("PASS: READ-ONLY typed equality audit")
    print("Selected proof steps:", len(rows))
    print("Report:", OUT / "typed_equality_audit.json")


if __name__ == "__main__":
    main()
