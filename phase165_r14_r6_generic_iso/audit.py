import json
from pathlib import Path
from hopf_facts import ETA_2
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation
from phase165_r14_r6_generic_iso import audit_generic_iso


def main():
    goal = Relation(
        lhs=TodaPrimaryGroup(3, 2),
        rhs=FreeCyclicGroup(ETA_2),
    )
    report = audit_generic_iso(goal)
    output = Path("phase165_r14_r6_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output / "report.md").write_text(
        "# Phase 165 R14-R6 — 一般同型規則の監査\n\n" +
        "\n".join(f"- {key}: {value}" for key, value in report.items()) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
