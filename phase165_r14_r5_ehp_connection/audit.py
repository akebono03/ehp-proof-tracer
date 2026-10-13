import json
from pathlib import Path

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r5_ehp_connection import audit_ehp_connection
from hopf_facts import ETA_2
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType


def main():
    bridge, _ = build_phase165_r5_manifest_bridge()
    goal = Relation(
        lhs=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2),
        rhs=FreeCyclicGroup(generator=ETA_2),
        relation_type=RelationType.EQUALITY,
    )
    report = audit_ehp_connection(goal, bridge)
    output = Path("phase165_r14_r5_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    (output / "report.md").write_text(
        "# Phase 165 R14-R5 EHP 接続監査\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in report.items()) + "\n",
        encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
