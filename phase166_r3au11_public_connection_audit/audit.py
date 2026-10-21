"""Read-only runtime/source checks for the existing DB-goal-to-public path."""
from __future__ import annotations

import argparse
import inspect
import json
import sys
from pathlib import Path


def audit(repo: Path) -> dict:
    sys.path.insert(0, str(repo))
    import phase165_r55_nk_only_goal as selector
    from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
    from toda_human_readable_renderer import render_toda_public_group_relation_latex

    selector_source = inspect.getsource(selector.registered_group_goal_candidates)
    search_source = inspect.getsource(selector.search_group_from_registered_goal)
    checks = {
        "selector_calls_structured_db_goal": "database_structured_group_goal_candidates(n=n, k=k)" in selector_source,
        "selector_uses_structured_for_k_ge_2": "if k >= 2:" in selector_source,
        "search_calls_registered_selector": "registered_group_goal_candidates(bridge, n=n, k=k)" in search_source,
        "search_uses_shared_goal_search": "search_shared_group_goal(**search_kwargs)" in search_source,
        "search_checks_citing_id": "resolve_specialized_goal_citing_id(bridge, candidate)" in search_source,
    }
    examples = []
    for n, k in ((10, 18), (11, 25), (4, 3), (3, 2)):
        row = {"n": n, "k": k, "candidate_count": 0, "rendered": False, "latex": "", "exception": ""}
        try:
            candidates = database_structured_group_goal_candidates(n=n, k=k)
            row["candidate_count"] = len(candidates)
            if len(candidates) == 1:
                row["latex"] = render_toda_public_group_relation_latex(candidates[0])
                row["rendered"] = True
        except Exception as error:
            row["exception"] = f"{type(error).__name__}: {error}"
        examples.append(row)
    return {
        "phase": "166 R3-AU-11",
        "checks": checks,
        "examples": examples,
        "runtime_web_view_invoked": False,
        "proof_completion_certified": False,
        "public_web_connection_certified": False,
        "production_code_modified": False,
        "full_pytest_run": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    result = audit(args.repo.resolve())
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    (output / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not all(result["checks"].values()):
        raise SystemExit("Existing expected connection missing; see summary.json")


if __name__ == "__main__":
    main()
