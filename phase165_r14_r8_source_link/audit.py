from pathlib import Path
import json
from hopf_facts import ETA_2
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r8_source_link import audit_source_link
from proof import Relation


def main():
    bridge, _ = build_phase165_r5_manifest_bridge()
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    report = audit_source_link(goal, bridge)
    folder = Path('phase165_r14_r8_output')
    folder.mkdir(exist_ok=True)
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (folder / 'report.md').write_text('# Phase 165 R14-R8 監査\n\n' + '\n'.join(f'- {k}: {v}' for k,v in report.items()) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
