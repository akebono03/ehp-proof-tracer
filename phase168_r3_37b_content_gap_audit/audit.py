"""Audit registered Reference content and missing typed proof statements."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_12_body_binding import build_narrative_body_lines
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

CASES = ((2, 1), (3, 1), (4, 1))


def inspect_case(n, k):
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise AssertionError(f"Expected one target context for {(n,k)}: {len(contexts)}")
    registry = contexts[0].registry
    model = build_linked_proof_narrative_model(result, contexts[0])
    body = {x.step_index for x in build_narrative_body_lines(result, model)}
    refs = []
    for ref in model.citations:
        contents = []
        for assertion_id in ref.assertion_ids:
            assertion = registry.assertion(assertion_id)
            content = assertion.content
            contents.append({
                "assertion_id": assertion_id,
                "type": type(content).__name__,
                "content": repr(content),
                "origin": assertion.origin.value,
                "dependencies": list(assertion.dependencies),
                "typed_sentence": typed_sentence(content, None),
            })
        refs.append({
            "number": ref.number,
            "locator": ref.reference.locator,
            "contents": contents,
        })
    steps = []
    for index, step in enumerate(model.steps):
        sentence = typed_sentence(step.conclusion, step)
        steps.append({
            "index": index,
            "kind": type(step.conclusion).__name__,
            "rule": step.rule.value,
            "rendered_body_line": index in body,
            "typed_sentence": sentence,
            "repr": repr(step.conclusion),
            "cited_numbers": list(model.step_citation_numbers[index]),
        })
    markdown = render_model_backed_narrative_markdown(result, model)
    return {
        "target": f"pi_{n+k}^{n}",
        "status": result.status.value,
        "reference_count": len(refs),
        "references": refs,
        "steps": steps,
        "markdown": markdown,
    }


def main():
    out = Path(__file__).resolve().parent / "output"
    out.mkdir(exist_ok=True)
    reports = [inspect_case(n, k) for n, k in CASES]
    for report in reports:
        (out / (report["target"].replace("^", "_") + ".md")).write_text(
            report["markdown"], encoding="utf-8"
        )
        print(report["target"], "references=", report["reference_count"])
        for ref in report["references"]:
            print(f'  R{ref["number"]} {ref["locator"]}: '
                  f'assertion_count={len(ref["contents"])} '
                  f'typed_sentences={sum(v["typed_sentence"] is not None for v in ref["contents"])}')
        print("  skipped unrendered typed steps:",
              [(s["index"], s["kind"]) for s in report["steps"]
               if not s["rendered_body_line"] and s["typed_sentence"] is None])
    (out / "audit.json").write_text(
        json.dumps({"mode": "AUDIT_ONLY", "cases": reports},
                   ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("AUDIT_ONLY: no production files modified")
    print("REPORT:", out / "audit.json")


if __name__ == "__main__":
    main()
