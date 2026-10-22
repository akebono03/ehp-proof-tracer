from __future__ import annotations

import functools
import json
from pathlib import Path

import toda_group_proof_narrative_contribution_renderer as contribution
import toda_group_proof_narrative_renderer as renderer
from web_group_proof import build_standard_web_group_proof_view

OUTPUT = Path("phase167_r4_6_route_trace_results")
METHODS = (
    (contribution, "link_toda_group_proof_narrative_reference_body_consumers"),
    (contribution, "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown"),
    (renderer, "_phase159_r1_6d_finalize_reference_and_linkage"),
    (renderer, "_phase159_r1_7c_preexisting_render_toda_group_proof_narrative_markdown"),
)


def matching_lines(markdown: str) -> list[str]:
    markers = (r"\pi_{n}^{n}", r"\pi_{5}^{5}", r"\pi_{1}^{1}", r"\pi_{2}^{2}", r"\pi_{3}^{3}")
    return [line for line in markdown.splitlines() if any(marker in line for marker in markers)]


def run_one(n: int, k: int) -> dict:
    events: list[dict] = []
    replacements = []
    for module, name in METHODS:
        original = getattr(module, name)
        @functools.wraps(original)
        def wrapper(*args, __original=original, __name=name, **kwargs):
            before = [matching_lines(a) for a in args if isinstance(a, str)]
            result = __original(*args, **kwargs)
            after = matching_lines(result) if isinstance(result, str) else []
            events.append({
                "function": __name,
                "before_matching_lines": before,
                "after_matching_lines": after,
                "changed_text": isinstance(result, str) and any(
                    isinstance(a, str) and a != result for a in args
                ),
            })
            return result
        setattr(module, name, wrapper)
        replacements.append((module, name, original))
    try:
        view = build_standard_web_group_proof_view(n, k, max_depth=2, mode="narrative")
        lines = [
            {"index": i, "prefix": line.prefix,
             "latex": line.statement_latex, "suffix": line.suffix}
            for i, line in enumerate(view.rendered_lines, 1)
        ]
        return {"target": f"pi{n+k}_{n}", "key": view.key, "events": events, "lines": lines}
    finally:
        for module, name, original in reversed(replacements):
            setattr(module, name, original)


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    for n, k in ((2, 1), (3, 1)):
        result = run_one(n, k)
        target = result["target"]
        (OUTPUT / (target + ".json")).write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(target, "events:", len(result["events"]), "lines:", len(result["lines"]))
    print("No production code modified.")
    print("Trace output:", OUTPUT.resolve())


if __name__ == "__main__":
    main()
