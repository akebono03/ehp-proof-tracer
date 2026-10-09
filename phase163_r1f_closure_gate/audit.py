from __future__ import annotations

import csv
import json
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open('r', encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def audit(root: Path) -> dict:
    evidence = root / 'phase163_r1e_output' / 'entry_review.csv'
    if not evidence.is_file():
        raise FileNotFoundError('phase163_r1e_output/entry_review.csv が必要です。R1E を先に実行してください。')
    entries = read_rows(evidence)
    if not entries:
        raise ValueError('R1E の Entry 一覧が空です。')
    output = root / 'phase163_r1f_output'
    output.mkdir(exist_ok=True)
    counts = {}
    for entry in entries:
        kind = entry.get('constructor', 'UNKNOWN')
        counts[kind] = counts.get(kind, 0) + 1
    explicit = [entry for entry in entries if entry.get('key_literal', '').strip()]
    without_key = [entry for entry in entries if not entry.get('key_literal', '').strip()]
    gaps = [
        ('runtime_entry_count', 'UNVERIFIED', '静的コンストラクタ出現数と実行時 Entry 数は一致するとは限らない'),
        ('identity_and_deduplication', 'UNVERIFIED', '数式・主張の数学的同一性は AST の一致だけでは決まらない'),
        ('fixed_vs_internal', 'UNVERIFIED', '文献の固定主張と証明内部ステップの区別が必要'),
        ('literature_order', 'UNVERIFIED', '文献上の掲載順・主張順・証明完了位置は未確認'),
        ('indirect_registration', 'UNVERIFIED', 'エイリアス・間接生成・実行時登録の網羅性は未確認'),
        ('registered_statement_total', 'UNVERIFIED', '数学的に異なる登録主張の総数は確定できない'),
    ]
    with (output / 'unresolved_gaps.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['category', 'status', 'reason'])
        writer.writerows(gaps)
    summary = {
        'phase': '163 R1F',
        'status': 'PROVISIONAL_NOT_COMPLETE',
        'entry_constructor_sites': len(entries),
        'entry_types': dict(sorted(counts.items())),
        'explicit_key_sites': len(explicit),
        'sites_without_explicit_key': len(without_key),
        'unresolved_gate_count': len(gaps),
        'mathematical_statement_total': None,
        'scope': 'R1E static evidence reconciliation only; no imports of project application code',
        'next_action': 'Review unresolved evidence against runtime repositories and literature source before declaring R1 complete',
    }
    (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = [
        '# Phase 163 R1F — R1 完了判定',
        '',
        '判定: **暫定（未完了）**。本報告は既存 R1E の静的証拠を照合するもので、数学的命題総数を確定しない。',
        '',
        '## 静的監査の結果',
        '',
        f'- Entry コンストラクタ出現箇所: {len(entries)}',
        f'- 明示的 key を持つ箇所: {len(explicit)}',
        f'- 明示的 key がない箇所: {len(without_key)}',
        '',
        '## R1 完了を妨げる未確認事項',
        '',
    ]
    report.extend(f'- **{item}**: {reason}' for item, _, reason in gaps)
    report.extend([
        '',
        '## Phase 境界',
        '',
        '- 本監査では Registry の型・API・ProofStep・Renderer・Backward Search を変更しない。',
        '- R2 の設計に進む際には、数学的同一性と文献順序が未確認であることを明示する。',
        '- 全命題棚卸し完了という判定は、この報告からはできない。',
        '',
    ])
    (output / 'report.md').write_text('\n'.join(report), encoding='utf-8')
    return summary


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    result = audit(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f'Reports: {root / "phase163_r1f_output"}')
    print('Source unchanged. Full suite not run.')


if __name__ == '__main__':
    main()
