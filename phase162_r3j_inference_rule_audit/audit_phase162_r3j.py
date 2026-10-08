"""Write Phase 162 R3-J read-only audit of previously unmatched inference rules."""
import json
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3j_inference_rule_audit import build_phase162_r3j_inference_rule_audit


def main() -> None:
    _, presentation = build_r3b_presentation()
    entries, report = build_phase162_r3j_inference_rule_audit(presentation)
    output = Path('phase162_r3j_output')
    output.mkdir(exist_ok=True)
    grouped = defaultdict(list)
    for entry in entries:
        key = (entry.classification, entry.statement_type, entry.inference_rule_name)
        grouped[key].append(entry.index)
    groups = [
        {
            'classification': key[0],
            'statement_type': key[1],
            'inference_rule_name': key[2],
            'count': len(indices),
            'step_indices': indices,
        }
        for key, indices in sorted(grouped.items(), key=lambda pair: (pair[0][0], pair[0][1], pair[0][2] or ''))
    ]
    for name, payload in (
        ('inference_rule_entries.json', [asdict(entry) for entry in entries]),
        ('inference_rule_groups.json', groups),
        ('inference_rule_audit.json', report),
    ):
        (output / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('Output:', output.resolve())


if __name__ == '__main__':
    main()
