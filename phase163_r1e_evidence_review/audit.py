from __future__ import annotations

import ast
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open('r', encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def inspect_assignments(path: Path, line_numbers: set[int]) -> dict[int, str]:
    try:
        tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    except (OSError, UnicodeError, SyntaxError):
        return {}
    labels: dict[int, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names = []
            for target in targets:
                names.extend(child.id for child in ast.walk(target) if isinstance(child, ast.Name))
            for call in ast.walk(node.value) if node.value is not None else []:
                if isinstance(call, ast.Call) and call.lineno in line_numbers:
                    labels[call.lineno] = ', '.join(sorted(set(names)))
    return labels


def audit(root: Path) -> dict:
    source = root / 'phase163_r1d_output'
    output = root / 'phase163_r1e_output'
    if not (source / 'registration_sites.csv').exists():
        raise FileNotFoundError('R1D の registration_sites.csv が見つかりません。R1D を先に実行してください。')
    records = read_csv(source / 'registration_sites.csv')
    output.mkdir(parents=True, exist_ok=True)
    files: dict[str, set[int]] = defaultdict(set)
    for row in records:
        if row['kind'] == 'entry_constructor':
            files[row['file']].add(int(row['line']))
    labels = {name: inspect_assignments(root / name, lines) for name, lines in files.items()}
    entries = []
    for row in records:
        if row['kind'] != 'entry_constructor':
            continue
        name = row['file']
        line = int(row['line'])
        key = row['key_literal']
        theorem = row['theorem_literal']
        entries.append({
            'file': name, 'line': str(line), 'owner': row['owner'],
            'constructor': row['called'], 'assignment_names': labels[name].get(line, ''),
            'key_literal': key, 'theorem_literal': theorem,
            'statement_expression': row['statement_expression'],
            'reference_expression': row['reference_expression'],
            'first_argument': row['first_argument'],
            'id_evidence': 'EXPLICIT_KEY' if key else 'NO_EXPLICIT_KEY',
            'statement_identity': 'UNVERIFIED', 'runtime_multiplicity': 'UNVERIFIED',
            'fixed_or_internal': 'UNVERIFIED', 'literature_order': 'UNVERIFIED',
        })
    fields = list(entries[0]) if entries else ['file','line','owner','constructor','assignment_names','key_literal','theorem_literal','statement_expression','reference_expression','first_argument','id_evidence','statement_identity','runtime_multiplicity','fixed_or_internal','literature_order']
    write_csv(output / 'entry_review.csv', entries, fields)
    rows_by_hash: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in records:
        if row['kind'] == 'entry_constructor':
            rows_by_hash[row['signature_sha256']].append(row)
    repetitions = []
    for hash_, matched in rows_by_hash.items():
        if len(matched) > 1:
            for row in matched:
                repetitions.append({'signature_sha256':hash_, 'file':row['file'], 'line':row['line'], 'key_literal':row['key_literal'], 'statement_expression':row['statement_expression'], 'status':'REVIEW_REQUIRED'})
    write_csv(output / 'repeated_expression_review.csv', repetitions, ['signature_sha256','file','line','key_literal','statement_expression','status'])
    by_source = Counter(r['file'] for r in entries)
    source_rows = [{'file':k,'entry_constructor_sites':str(v)} for k,v in sorted(by_source.items())]
    write_csv(output / 'entry_files.csv',source_rows,['file','entry_constructor_sites'])
    missing = [e for e in entries if not e['key_literal']]
    summary = {
        'scope':'R1D static entry constructor evidence; no imports, no runtime instantiation',
        'entry_constructor_sites':len(entries),
        'entry_files':len(by_source),
        'explicit_key_sites':len(entries)-len(missing),
        'sites_without_explicit_key':len(missing),
        'repeated_expression_rows_to_review':len(repetitions),
        'kind_counts':dict(Counter(r['constructor'] for r in entries)),
        'status':'R1 INVENTORY PROVISIONAL; mathematical statement totals remain unknown',
        'R2_boundary':'No registry schema or backward search changes',
    }
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines = ['# Phase 163 R1E — Entry 実体の確認用一覧','','R1D の静的結果から Entry 生成箇所を抽出した。数学的命題の総数ではない。','','## 確認済みの規模','']
    lines.extend(f'- {k}: {v}' for k,v in summary.items() if isinstance(v,int))
    lines += ['', '## R1 で確定していない事項','', '- 動的生成された Entry の実数', '- 同じ Statement の数学的同一性', '- 固定文献主張と内部証明ステップの境界', '- 文献上の主張順・証明完了位置', '- Entry コンストラクタ以外で登録される仕組み', '', 'CSV は人手確認用の入力であり、未確認欄を推測で埋めない。', '']
    (output/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    return summary


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    print(json.dumps(audit(root), ensure_ascii=False, indent=2))
    print('R1E read-only review generated; project source unchanged; full pytest not run.')


if __name__ == '__main__':
    main()
