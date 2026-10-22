from __future__ import annotations

import functools
import json
from pathlib import Path

import toda_group_proof_narrative_contribution_ordering as ordering
import toda_group_proof_narrative_contribution_renderer as renderer
from web_group_proof import build_standard_web_group_proof_view

OUT = Path("phase167_r4_6_contribution_identity_results")
ORIGINAL = renderer.build_toda_group_proof_narrative_ordered_contributions


def describe_step(step):
    return {
        "step_id": id(step),
        "conclusion_type": type(step.conclusion).__name__,
        "conclusion_repr": repr(step.conclusion)[:1500],
        "rule": str(step.rule),
        "inference_rule": (
            None if step.inference_rule is None else step.inference_rule.name
        ),
        "premises": [
            {
                "step_id": id(p),
                "conclusion_type": type(p.conclusion).__name__,
                "conclusion_repr": repr(p.conclusion)[:700],
            }
            for p in step.premises
        ],
    }


def collect(n, k):
    calls = []

    @functools.wraps(ORIGINAL)
    def traced(*args, **kwargs):
        result = ORIGINAL(*args, **kwargs)
        records = []
        for group in result:
            group_record = []
            for contribution in group:
                record = describe_step(contribution.proof_step)
                record.update({
                    "provider_anchor": contribution.provider_anchor,
                    "provider_keys": repr(contribution.provider_keys),
                    "role": contribution.contribution_role.value,
                    "placement": contribution.placement.value,
                    "distance_to_conclusion": contribution.distance_to_conclusion,
                })
                group_record.append(record)
            records.append(group_record)
        calls.append(records)
        return result

    renderer.build_toda_group_proof_narrative_ordered_contributions = traced
    try:
        view = build_standard_web_group_proof_view(
            n, k, max_depth=2, mode="narrative"
        )
        return {
            "target": f"pi{n+k}_{n}",
            "key": view.key,
            "ordered_contributions": calls,
            "public_line_count": len(view.rendered_lines),
        }
    finally:
        renderer.build_toda_group_proof_narrative_ordered_contributions = ORIGINAL


def main():
    OUT.mkdir(exist_ok=True)
    for n, k in ((2, 1), (3, 1)):
        result = collect(n, k)
        path = OUT / (result["target"] + ".json")
        path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        num = sum(len(group) for call in result["ordered_contributions"] for group in call)
        print(result["target"], "contributions:", num,
              "lines:", result["public_line_count"])
    print("REPORT:", OUT.resolve())
    print("NO_PRODUCTION_CHANGES")


if __name__ == "__main__":
    main()
