"""Write read-only per-step and grouped Phase 162 R3-I inventory reports."""
import json
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3i_semantic_sidecar_audit import build_phase162_r3i_sidecar_audit


def main() -> None:
    _, presentation = build_r3b_presentation()
    entries, report = build_phase162_r3i_sidecar_audit(presentation)
    output = Path('phase162_r3i_output')
    output.mkdir(exist_ok=True)
    grouped = defaultdict(list)
    for entry in entries:
        grouped[(entry.category, entry.statement_type, entry.inference_rule)].append(entry.index)
    groups = [
        {'category': key[0], 'statement_type': key[1], 'inference_rule': key[2],
         'count': len(indices), 'step_indices': indices}
        for key, indices in sorted(grouped.items(), key=lambda pair: (pair[0][0], pair[0][1], pair[0][2] or ''))
    ]
    for name, data in (
        ('semantic_sidecar_entries.json', [asdict(entry) for entry in entries]),
        ('semantic_sidecar_groups.json', groups),
        ('semantic_sidecar_audit.json', report),
    ):
        (output / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('Output:', output.resolve())


if __name__ == '__main__':
    main()
