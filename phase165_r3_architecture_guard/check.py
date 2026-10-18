"""Capture the unchanged public narrative and Web outputs for two fixed queries."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase165_r55_nk_only_goal import search_group_from_registered_goal

OUTPUT = Path("phase165_r3_architecture_guard_results")
OUTPUT.mkdir(exist_ok=True)


def snapshot(n: int, k: int, name: str, suffix: str) -> dict:
    result = search_group_from_registered_goal(n=n, k=k)
    assert result.status.value == "complete", (name, result.status, result.diagnostics)
    markdown = render_partial_proof_markdown(result)
    view = build_partial_web_group_proof_view(result, max_depth=2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert view.rendered_lines and len(view.steps) == len(result.proven_steps)
    (OUTPUT / f"{name}_{suffix}.md").write_text(markdown, encoding="utf-8")
    summary = {
        "status": result.status.value,
        "markdown_sha256": hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
        "step_count": len(view.steps),
        "rendered_line_count": len(view.rendered_lines),
        "view_key": view.key,
        "mode": view.mode,
    }
    (OUTPUT / f"{name}_{suffix}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    before = {name: snapshot(n, k, name, "before") for n, k, name in ((2, 1, "pi3_2"), (3, 1, "pi4_3"))}
    after = {name: snapshot(n, k, name, "after") for n, k, name in ((2, 1, "pi3_2"), (3, 1, "pi4_3"))}
    assert before == after, "public outputs changed within the same unchanged source run"
    pi43 = (OUTPUT / "pi4_3_after.md").read_text(encoding="utf-8")
    assert pi43.count(r"\ker E") == 1, "pi4_3 kernel missing or duplicated"
    assert pi43.count("第一同型定理") == 1, "pi4_3 quotient proof missing or duplicated"
    assert pi43.index(r"\operatorname{Im}\Delta") < pi43.index(r"\ker E") < pi43.index("第一同型定理")
    report = {"phase": "165 R3", "checks": "PASS", "before": before, "after": after, "full_pytest_run": False}
    (OUTPUT / "audit_result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("R3 PASS: unchanged public narratives, consistent view and architecture guard")
    print("Report:", (OUTPUT / "audit_result.json").resolve())


if __name__ == "__main__":
    main()
