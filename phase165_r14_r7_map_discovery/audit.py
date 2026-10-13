import json
from pathlib import Path
from hopf_facts import ETA_2
from homotopy_groups import TodaPrimaryGroup, FreeCyclicGroup
from proof import Relation
from phase165_r14_r7_map_discovery import audit_hopf_discovery


def main():
    goal = Relation(lhs=TodaPrimaryGroup(3, 2), rhs=FreeCyclicGroup(ETA_2))
    report = audit_hopf_discovery(goal)
    output = Path('phase165_r14_r7_output')
    output.mkdir(exist_ok=True)
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
