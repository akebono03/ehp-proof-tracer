from __future__ import annotations

import json
from pathlib import Path

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r3_source_scope import collect_toda51_scope


def main() -> None:
    bridge, _ = build_phase165_r5_manifest_bridge()
    report = collect_toda51_scope(bridge)
    dest = Path("phase165_r14_r3_output")
    dest.mkdir(exist_ok=True)
    (dest / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (dest / "report.md").write_text(
        "# Phase 165 R14-R3 — Toda (5.1) の出典範囲\n\n"
        + "\n".join(f"- {key}: {value}" for key, value in report.items()
                    if key not in ("numbered_source", "adjacent_source", "clauses"))
        + "\n\n## 出典に属する主張\n\n"
        + "\n".join(f"- `{c['key']}`: `${c['tex']}$" for c in report["clauses"])
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        k: report[k] for k in (
            "phase", "reference_scope", "source_clause_count",
            "typed_schema_count", "adjacent_source_status",
            "new_proof_eligible", "proof_steps_created", "status",
            "full_pytest_run",
        )
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
