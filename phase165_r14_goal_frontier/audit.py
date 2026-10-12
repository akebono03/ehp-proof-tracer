"""Run a read-only, fail-closed check of the first Toda goal."""
import json
from pathlib import Path

from hopf_facts import ETA_2
from phase165_r14_goal_frontier import inspect_free_cyclic_goal


def main() -> None:
    frontier = inspect_free_cyclic_goal(2, 1, ETA_2)
    report = {
        "phase": "165 R14-R1",
        "target": "pi_3^2 = Z{eta_2}",
        "typed_goal": repr(frontier.goal),
        "source_assertions": frontier.source_assertions,
        "newly_mathematically_typed": frontier.typed_assertions,
        "newly_proof_eligible": frontier.eligible_assertions,
        "exact_registered_goal_matches": frontier.exact_registered_goal_matches,
        "status": frontier.status,
        "blocker": frontier.blocker,
        "legacy_proof_used": False,
        "full_pytest_run": False,
    }
    output = Path("phase165_r14_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "report.md").write_text(
        "# Phase 165 R14-R1 — 初期 Goal 監査\n\n"
        + "\n".join(f"- {key}: {value}" for key, value in report.items()) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
