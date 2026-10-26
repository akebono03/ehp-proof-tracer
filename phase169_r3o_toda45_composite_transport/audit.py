"""R3O real Web result audit. Does not claim completion without proof verification."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from phase165_r52_partial_proof import ProofSearchStatus
from web_group_proof import build_standard_web_group_proof_view
import phase168_r3_5_model_renderer as model_renderer


def capture(n: int, k: int) -> dict:
    outputs = []
    renderer = model_renderer.render_model_backed_narrative_markdown

    def capture_model(result, model):
        outputs.append((result, model))
        return renderer(result, model)

    with patch.object(model_renderer, "render_model_backed_narrative_markdown",
                      side_effect=capture_model):
        view = build_standard_web_group_proof_view(
            n=n, k=k, mode="narrative", citation_source="model",
        )
    data = {
        "n": n, "k": k,
        "view_key": view.key,
        "partial": bool(view.partial_result),
    }
    if outputs:
        result, model = outputs[-1]
        data["status"] = result.status.value
        data["steps"] = len(model.steps)
        data["citations"] = [c.reference.locator or c.reference.label
                             for c in model.citations]
        data["has_cited_toda45"] = "(4.5)" in data["citations"]
        if result.status is ProofSearchStatus.COMPLETE and model.root_index is not None:
            root = model.steps[model.root_index]
            checked = set()
            names = []
            def visit(step):
                if id(step) in checked:
                    return
                checked.add(id(step))
                if step.inference_rule is not None:
                    names.append(step.inference_rule.name)
                for parent in step.premises:
                    visit(parent)
            visit(root)
            data["root_ancestry_includes_new_rule"] = any(
                name == "cited Toda (4.5) finite-cyclic composite generator transport"
                for name in names
            )
        else:
            data["root_ancestry_includes_new_rule"] = None
    return data


def main() -> None:
    results = [capture(n, 2) for n in (3, 4, 5, 6)]
    path = Path(__file__).resolve().parent / "output" / "r3o_web_audit.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({"phase": "169-R3O", "cases": results},
                               indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for record in results:
        print(f"R3O_WEB_PI_{record['n']+2}_{record['n']}="
              + str(record.get("status", "unknown")))
        print(f"R3O_TODA45_PI_{record['n']+2}_{record['n']}="
              + str(record.get("has_cited_toda45")))
        print(f"R3O_NEW_RULE_IN_ROOT_PI_{record['n']+2}_{record['n']}="
              + str(record.get("root_ancestry_includes_new_rule")))
    print("R3O_REPORT=" + str(path))
    print("R3O_AUDIT_COMPLETE=True")


if __name__ == "__main__":
    main()
