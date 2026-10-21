"""Phase 166 R3-AU-12: public proof route runtime observation (read-only)."""
from __future__ import annotations

import argparse
import inspect
import json
from pathlib import Path


def source_checks() -> dict[str, bool]:
    from web_group_proof import build_standard_web_group_proof_view
    from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    a = inspect.getsource(build_standard_web_group_proof_view)
    b = inspect.getsource(build_group_proof_progress_view)
    c = inspect.getsource(build_partial_web_group_proof_view)
    d = inspect.getsource(search_group_from_registered_goal)
    return {
        "standard_calls_search": "search_group_from_registered_goal(" in a,
        "flask_bridge_calls_search": "search_group_from_registered_goal(" in b,
        "standard_calls_adapter": "build_partial_web_group_proof_view(" in a,
        "flask_bridge_calls_adapter": "build_partial_web_group_proof_view(" in b,
        "adapter_uses_conclusion_if_complete": "result.conclusion" in c,
        "adapter_uses_open_goals_if_partial": "result.open_goals" in c,
        "adapter_uses_markdown_renderer": "render_partial_proof_markdown(result)" in c,
        "adapter_proof_complete_status": "ProofSearchStatus.COMPLETE" in c,
        "search_uses_shared_goal_search": "search_shared_group_goal(" in d,
    }


def inspect_view(n: int, k: int, entry: str) -> dict:
    from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
    from web_group_proof import build_standard_web_group_proof_view
    from web_group_proof_common import WebGroupProofView
    out = {"n": n, "k": k, "entry": entry, "invoked": True}
    try:
        if entry == "flask":
            view = build_group_proof_progress_view(n=n, k=k, max_depth=2)
        else:
            view = build_standard_web_group_proof_view(n=n, k=k, max_depth=2, mode="narrative")
        out.update({
            "web_view_type_verified": isinstance(view, WebGroupProofView),
            "key": view.key,
            "partial_result": view.partial_result,
            "conclusion_latex": view.conclusion_latex,
            "rendered_line_count": len(view.rendered_lines),
            "proven_step_count": len(view.steps),
            "mode": view.mode,
            "error": "",
        })
    except Exception as exc:
        out.update({"web_view_type_verified": False, "error": type(exc).__name__ + ": " + str(exc)})
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--entry", choices=("flask", "standard"), default="flask")
    args = parser.parse_args()
    checks = source_checks()
    observation = inspect_view(args.n, args.k, args.entry)
    summary = {
        "phase": "166 R3-AU-12",
        "source_checks": checks,
        "runtime_web_view": observation,
        "goal_render_success_not_proof_certification": True,
        "production_code_modified": False,
        "full_pytest_run": False,
    }
    folder = Path(__file__).resolve().parent / "results"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if observation["error"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
