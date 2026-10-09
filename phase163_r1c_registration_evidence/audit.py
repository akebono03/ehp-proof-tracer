from __future__ import annotations

import ast
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / 'phase163_r1b_output' / 'registration_priority.csv'
OUTPUT = ROOT / 'phase163_r1c_output'
EXCLUDED = {'archive', '.git', '.venv', 'venv', '__pycache__', 'node_modules', '.pytest_cache', 'build', 'dist'}
ENTRY_TYPES = {'ProofRepositoryEntry', 'TheoremFactEntry'}
CONTAINERS = {'ProofRepository', 'TheoremFactRepository'}
REGISTER_METHODS = {'register', 'register_fact', 'register_statement'}


def allowed(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return not any(part in EXCLUDED or part.startswith('phase') for part in rel.parts[:-1])


def dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return dotted(node.value) + '.' + node.attr
    return ''


def static_repr(node: ast.AST | None) -> str:
    if node is None:
        return ''
    try:
        value = ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, RecursionError, MemoryError):
        return ast.unparse(node)[:180]
    return str(value)[:180]


def nearest_owner(tree: ast.AST, target: ast.AST) -> str:
    owner = '<module>'
    def visit(node: ast.AST, current: str) -> None:
        nonlocal owner
        if node is target:
            owner = current
            return
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            current = (current + '.' if current != '<module>' else '') + node.name
        for child in ast.iter_child_nodes(node):
            visit(child, current)
    visit(tree, '<module>')
    return owner


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if not INPUT.is_file():
        raise SystemExit('R1B output missing: ' + str(INPUT))
    OUTPUT.mkdir(exist_ok=True)
    with INPUT.open(encoding='utf-8-sig', newline='') as handle:
        r1b = list(csv.DictReader(handle))
    files = sorted({row['file'] for row in r1b if row['area'] == 'production'})
    rows = []
    issues = []
    for rel in files:
        source = ROOT / rel
        if not source.is_file() or not allowed(source):
            issues.append({'file': rel, 'reason': 'file missing or excluded'})
            continue
        try:
            tree = ast.parse(source.read_text(encoding='utf-8-sig'), filename=rel)
        except (UnicodeError, OSError, SyntaxError) as error:
            issues.append({'file': rel, 'reason': str(error)})
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = dotted(node.func).split('.')[-1]
            if name in ENTRY_TYPES:
                kind = 'entry_instance_site'
            elif name in CONTAINERS:
                kind = 'container_creation_site'
            elif name in REGISTER_METHODS:
                kind = 'registration_invocation_site'
            elif name == 'LiteratureReference':
                kind = 'literature_reference_site'
            else:
                continue
            kws = {kw.arg: static_repr(kw.value) for kw in node.keywords if kw.arg is not None}
            position = f'{rel}:{node.lineno}'
            rows.append({
                'site': position,
                'file': rel,
                'line': node.lineno,
                'owner': nearest_owner(tree, node),
                'kind': kind,
                'constructor': dotted(node.func),
                'key': kws.get('key', ''),
                'theorem': kws.get('theorem', ''),
                'phase': kws.get('phase', ''),
                'statement_expression': kws.get('statement', ''),
                'reference_expression': kws.get('reference', ''),
                'source_expression': kws.get('source', ''),
                'argument_count': len(node.args),
                'keywords': ';'.join(sorted(kws)),
                'provenance_status': 'UNVERIFIED',
                'statement_identity_status': 'UNVERIFIED',
                'runtime_count_status': 'UNVERIFIED',
            })
    rows.sort(key=lambda r: (r['file'], r['line'], r['kind']))
    counts = Counter(row['kind'] for row in rows)
    by_file = defaultdict(Counter)
    for row in rows:
        by_file[row['file']][row['kind']] += 1
    filenames = [{'file': key, **{k: val.get(k, 0) for k in ('entry_instance_site', 'container_creation_site', 'registration_invocation_site', 'literature_reference_site')}} for key, val in sorted(by_file.items())]
    write_csv(OUTPUT / 'registration_sites.csv', rows, ['site','file','line','owner','kind','constructor','key','theorem','phase','statement_expression','reference_expression','source_expression','argument_count','keywords','provenance_status','statement_identity_status','runtime_count_status'])
    write_csv(OUTPUT / 'file_counts.csv', filenames, ['file','entry_instance_site','container_creation_site','registration_invocation_site','literature_reference_site'])
    summary = {
        'scope': 'R1B priority source files; static call sites only',
        'input_priority_rows': len(r1b),
        'inspected_files': len(files),
        'identified_sites': len(rows),
        'by_site_kind': dict(sorted(counts.items())),
        'inspection_errors': issues,
        'not_a_statement_count': True,
        'still_unverified': ['dynamic registration multiplicity', 'statement identity and deduplication', 'reference provenance and order', 'fixed statement versus proof-internal status', 'coverage of registries beyond R1B priority candidates'],
    }
    (OUTPUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 163 R1C — 登録箇所の証拠照合', '', 'この結果は R1B の優先候補に限定した静的な呼び出し箇所の一覧です。登録済み数学命題の確定数ではありません。', '', '## 監査数', '', f'- 対象ファイル: {len(files)}', f'- 検出箇所: {len(rows)}']
    lines += [f'- {k}: {v}' for k,v in sorted(counts.items())]
    lines += ['', '## 未確定事項', '', *('- ' + s for s in summary['still_unverified']), '', '## R2 との境界', '', '今回の処理は既存の ProofStep や Registry を変更しない。数学的な Statement ID や利用可能性規則は設計・導入しない。', '']
    (OUTPUT / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print('Reports:', OUTPUT)


if __name__ == '__main__':
    main()
