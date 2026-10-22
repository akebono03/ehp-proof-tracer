from __future__ import annotations

import functools
import json
from pathlib import Path

import toda_group_proof_narrative_contribution_renderer as contribution
import toda_group_proof_narrative_renderer as renderer
from web_group_proof import build_standard_web_group_proof_view

OUT = Path("phase167_r4_6_stage_origin_results")
WATCHED = (
    "render_toda_group_proof_narrative_multi_argument_markdown",
    "_insert_toda_group_proof_narrative_argument_contributions",
    "insert_toda_group_proof_narrative_reason_prose",
    "suppress_toda_group_proof_narrative_reference_internal_body",
    "link_toda_group_proof_narrative_reference_body_consumers",
    "order_toda_group_proof_narrative_visible_step_dependencies",
    "order_toda_group_proof_narrative_visible_relation_dependencies",
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
)
MARKERS = (
    r"\pi_{n}^{n} = ",
    r"\pi_{5}^{5} = ",
    r"\pi_{1}^{1} = ",
    r"\pi_{2}^{2} = ",
    r"\pi_{3}^{3} = ",
)


def relevant_lines(markdown: str) -> list[str]:
    return [line for line in markdown.splitlines() if any(m in line for m in MARKERS)]


def record_stages(n: int, k: int) -> dict:
    events: list[dict] = []
    originals: list[tuple[object, str, object]] = []

    def wrap(module: object, name: str) -> None:
        original = getattr(module, name, None)
        if not callable(original):
            return

        @functools.wraps(original)
        def traced(*args, **kwargs):
            inputs = [
                relevant_lines(arg)
                for arg in args if isinstance(arg, str)
            ]
            output = original(*args, **kwargs)
            if isinstance(output, str):
                events.append({
                    "stage": name,
                    "module": module.__name__,
                    "input_relevant_lines": inputs,
                    "output_relevant_lines": relevant_lines(output),
                    "output_char_count": len(output),
                })
            return output

        originals.append((module, name, original))
        setattr(module, name, traced)

    try:
        for name in WATCHED:
            wrap(contribution, name)
        # Imported function aliases are held in renderer's module namespace.
        for name in WATCHED:
            if name in renderer.__dict__:
                wrap(renderer, name)

        view = build_standard_web_group_proof_view(
            n, k, max_depth=2, mode="narrative"
        )
        public_lines = [
            {
                "line": i,
                "prefix": line.prefix,
                "latex": line.statement_latex,
                "suffix": line.suffix,
            }
            for i, line in enumerate(view.rendered_lines, 1)
        ]
        return {
            "target": f"pi{n+k}_{n}",
            "view_key": view.key,
            "events": events,
            "public_lines": public_lines,
        }
    finally:
        for module, name, original in reversed(originals):
            setattr(module, name, original)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for n, k in ((2, 1), (3, 1)):
        report = record_stages(n, k)
        target = report["target"]
        path = OUT / (target + ".json")
        path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(
            target,
            "stages:",
            len(report["events"]),
            "public_lines:",
            len(report["public_lines"]),
        )
    print("OUTPUT:", OUT.resolve())
    print("NO_PRODUCTION_CHANGES")


if __name__ == "__main__":
    main()
