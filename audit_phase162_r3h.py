"""Generate Phase 162 R3-H per-inference and grouped audit reports."""

import json
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3h_reason_inventory import build_phase162_r3h_inventory


def main() -> None:
    _, presentation = build_r3b_presentation()
    entries, summary = build_phase162_r3h_inventory(presentation)
    grouped = defaultdict(list)
    for entry in entries:
        grouped[(entry.category, entry.statement_type, entry.inference_rule)].append(entry.index)
    groups = [
        {
            'category': key[0],
            'statement_type': key[1],
            'inference_rule': key[2],
            'count': len(indices),
            'step_indices': indices,
        }
        for key, indices in sorted(grouped.items(), key=lambda pair: (pair[0][0], pair[0][1], pair[0][2] or ''))
    ]
    output = Path('phase162_r3h_output')
    output.mkdir(exist_ok=True)
    (output / 'unexplained_step_inventory.json').write_text(
        json.dumps([asdict(entry) for entry in entries], ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    (output / 'reason_inventory_groups.json').write_text(
        json.dumps(groups, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    (output / 'reason_inventory_audit.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print('Inventory:', (output / 'unexplained_step_inventory.json').resolve())
    print('Groups:', (output / 'reason_inventory_groups.json').resolve())
    print('Summary:', (output / 'reason_inventory_audit.json').resolve())


if __name__ == '__main__':
    main()
