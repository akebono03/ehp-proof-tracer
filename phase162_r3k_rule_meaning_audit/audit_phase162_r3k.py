"""Read-only Phase 162 R3-K rule description and proof-step structure audit."""
import json
from dataclasses import asdict
from pathlib import Path

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3k_rule_meaning_audit import (
    build_phase162_r3k_rule_meaning_audit,
    render_phase162_r3k_rule_meaning_markdown,
)


def main() -> None:
    _, presentation = build_r3b_presentation()
    entries, groups, report = build_phase162_r3k_rule_meaning_audit(presentation)
    output = Path('phase162_r3k_output')
    output.mkdir(exist_ok=True)
    payloads = (
        ('rule_meaning_entries.json', [asdict(entry) for entry in entries]),
        ('rule_meaning_groups.json', groups),
        ('rule_meaning_audit.json', report),
    )
    for filename, payload in payloads:
        (output / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'rule_explanation_drafts.md').write_text(
        render_phase162_r3k_rule_meaning_markdown(entries), encoding='utf-8'
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('Output:', output.resolve())


if __name__ == '__main__':
    main()
