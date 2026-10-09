from __future__ import annotations

import ast
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

EXCLUDE = {'.git', '.venv', 'venv', 'archive', '__pycache__', 'node_modules', '.pytest_cache', 'build', 'dist'}
ENTRY = {'ProofRepositoryEntry', 'TheoremFactEntry'}
CONTAINER = {'ProofRepository', 'TheoremFactRepository'}
REGISTER = {'register', 'register_fact', 'register_statement'}
REFERENCE = {'LiteratureReference'}


def permitted(path: Path, root: Path) -> bool:
    parts = path.relative_to(root).parts
    return not any(p in EXCLUDE or p.startswith('phase') for p in parts[:-1]) and not path.name.startswith('test_') and 'tests' not in parts[:-1]


def name_of(expr: ast.AST) -> str:
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return name_of(expr.value) + '.' + expr.attr
    return ''


def expression(expr: ast.AST | None) -> str:
    if expr is None:
        return ''
    try:
        return ast.unparse(expr)[:600]
    except (ValueError, TypeError):
        return ''


def literal(expr: ast.AST | None) -> str:
    if expr is None:
        return ''
    try:
        value = ast.literal_eval(expr)
    except (ValueError, TypeError, SyntaxError, RecursionError):
        return ''
    return value if isinstance(value, str) else repr(value)


def owner_map(tree: ast.AST) -> dict[int, str]:
    owners = {}
    def visit(node: ast.AST, path: str) -> None:
        owners[id(node)] = path
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            path = (path + '.' if path else '') + node.name
        for child in ast.iter_child_nodes(node):
            visit(child, path)
    visit(tree, '')
    return owners


def collect(root: Path) -> tuple[list[dict], list[dict], list[dict]]:
    records = []
    errors = []
    definitions = []
    for path in sorted(root.rglob('*.py')):
        if not permitted(path, root):
            continue
        rel = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=rel)
        except (OSError, UnicodeError, SyntaxError) as exc:
            errors.append({'file': rel, 'error': str(exc)})
            continue
        owners = owner_map(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and ('Statement' in node.name or 'Repository' in node.name or 'Registry' in node.name):
                definitions.append({'file': rel, 'line': node.lineno, 'class': node.name, 'category': 'statement_type' if 'Statement' in node.name else 'container_type'})
            if not isinstance(node, ast.Call):
                continue
            called = name_of(node.func)
            short = called.rsplit('.', 1)[-1]
            if short in ENTRY:
                kind = 'entry_constructor'
            elif short in CONTAINER:
                kind = 'container_constructor'
            elif short in REGISTER:
                kind = 'registration_call'
            elif short in REFERENCE:
                kind = 'reference_constructor'
            else:
                continue
            kwargs = {k.arg: k.value for k in node.keywords if k.arg is not None}
            key = literal(kwargs.get('key'))
            theorem = literal(kwargs.get('theorem'))
            statement = expression(kwargs.get('statement'))
            reference = expression(kwargs.get('reference'))
            signature = '|'.join([short, key, theorem, statement, reference])
            records.append({
                'file': rel, 'line': node.lineno, 'owner': owners[id(node)] or '<module>',
                'kind': kind, 'called': called, 'key_literal': key,
                'theorem_literal': theorem, 'statement_expression': statement,
                'reference_expression': reference,
                'first_argument': expression(node.args[0]) if node.args else '',
                'signature_sha256': hashlib.sha256(signature.encode('utf-8')).hexdigest(),
                'identity_status': 'UNVERIFIED', 'provenance_status': 'UNVERIFIED',
                'runtime_multiplicity': 'UNVERIFIED',
            })
    return sorted(records, key=lambda r: (r['file'], r['line'], r['kind'])), errors, sorted(definitions, key=lambda r:(r['file'],r['line']))


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def report(root: Path, out: Path) -> dict:
    records, errors, definitions = collect(root)
    out.mkdir(parents=True, exist_ok=True)
    keys = defaultdict(list)
    signatures = defaultdict(list)
    for row in records:
        if row['kind'] == 'entry_constructor' and row['key_literal']:
            keys[row['key_literal']].append(f"{row['file']}:{row['line']}")
        if row['kind'] == 'entry_constructor':
            signatures[row['signature_sha256']].append(f"{row['file']}:{row['line']}")
    duplicates = [{'key': k, 'sites': '; '.join(v), 'site_count': len(v)} for k,v in sorted(keys.items()) if len(v)>1]
    repetition = [{'signature_sha256': k, 'sites': '; '.join(v), 'site_count': len(v)} for k,v in sorted(signatures.items()) if len(v)>1]
    write_csv(out/'registration_sites.csv', records, list(records[0]) if records else ['file','line','owner','kind','called','key_literal','theorem_literal','statement_expression','reference_expression','first_argument','signature_sha256','identity_status','provenance_status','runtime_multiplicity'])
    write_csv(out/'statement_type_definitions.csv', definitions, ['file','line','class','category'])
    write_csv(out/'duplicate_key_candidates.csv', duplicates, ['key','sites','site_count'])
    write_csv(out/'repeated_expression_candidates.csv', repetition, ['signature_sha256','sites','site_count'])
    counts = Counter(r['kind'] for r in records)
    summary = {
        'scope': 'All canonical production Python files, static syntax only',
        'inspected_registration_files': len({r['file'] for r in records}),
        'registration_sites': len(records), 'by_kind': dict(sorted(counts.items())),
        'statement_type_definition_sites': sum(d['category']=='statement_type' for d in definitions),
        'literal_entry_keys': len(keys), 'duplicate_literal_key_candidates': len(duplicates),
        'repeated_entry_expression_candidates': len(repetition),
        'parse_errors': errors,
        'important_limits': ['A constructor site is not a mathematical statement count', 'Same signature hash is not a proof of mathematical identity', 'Dynamic registration and runtime instances not counted', 'Literature publication order and availability not checked', 'Fixed statements and proof-internal steps not yet validated', 'AST call detection can miss indirect or aliased constructors'],
    }
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines = ['# Phase 163 R1D — 登録実体と重複候補の横断監査', '', '既存コードへの変更・import 実行を行わない静的監査。集計は数学的に異なる命題の数ではない。', '', '## 集計', '']
    lines += [f'- {k}: {v}' for k,v in summary.items() if isinstance(v,int)]
    lines += [f'- {k}: {v}' for k,v in sorted(counts.items())]
    lines += ['', '## 解釈上の注意', ''] + [f'- {s}' for s in summary['important_limits']]
    lines += ['', 'R1 完了には、登録候補の実体・数学的同一性・追加の登録方式を確認する必要がある。R2 の新規 Registry は実装しない。', '']
    (out/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    return summary


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    summary = report(root, root/'phase163_r1d_output')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print('Phase 163 R1D read-only audit complete. No full pytest suite executed.')


if __name__ == '__main__':
    main()
