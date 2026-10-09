from __future__ import annotations
import ast
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'phase163_r1b_output'
SKIP_DIRS = {'archive', '.git', '.venv', 'venv', '__pycache__', 'node_modules', '.pytest_cache', 'build', 'dist'}
SCOPE_WORDS = ('registry', 'repository', 'theorem', 'statement', 'literature', 'reference', 'fact', 'rule')
ENTRY_CALLS = ('ProofRepositoryEntry', 'TheoremFactEntry')
CONTAINER_CALLS = ('ProofRepository', 'TheoremFactRepository')


def permitted(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return not any(part in SKIP_DIRS or (part.lower().startswith('phase') and part != relative.name) for part in relative.parts[:-1])


def qualified(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except (TypeError, ValueError):
        return ''


def classify(node: ast.AST) -> str | None:
    if isinstance(node, ast.Call):
        name = qualified(node.func).split('.')[-1]
        if name in ENTRY_CALLS:
            return 'explicit_entry_constructor'
        if name in CONTAINER_CALLS:
            return 'repository_constructor'
        if name in ('register', 'register_fact', 'register_statement'):
            return 'registration_call_candidate'
        if name == 'LiteratureReference':
            return 'literature_reference_candidate'
        return None
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        name = node.name.lower()
        if 'statement' in name and isinstance(node, ast.ClassDef):
            return 'statement_class_candidate'
        if 'rule' in name and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return 'rule_function_candidate'
        if any(token in name for token in ('repository', 'registry', 'theorem_fact')):
            return 'api_or_container_definition'
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        names = [n.id for target in targets for n in ast.walk(target) if isinstance(n, ast.Name)]
        if any(any(word in name.upper() for word in ('REPOSITORY', 'REGISTRY', 'FACTS', 'ENTRIES')) for name in names):
            return 'named_container_assignment'
    return None


def collect(root: Path) -> tuple[list[dict], list[dict]]:
    records = []
    errors = []
    for path in sorted(root.rglob('*.py')):
        if not permitted(path, root):
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith('phase163_r1b_classification/'):
            continue
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=rel)
        except (OSError, UnicodeError, SyntaxError) as error:
            errors.append({'file': rel, 'error': str(error)})
            continue
        part = 'test' if rel.startswith('tests/') or path.name.startswith('test_') else 'production'
        for node in ast.walk(tree):
            kind = classify(node)
            if kind is None:
                continue
            symbol = node.name if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) else qualified(node.func) if isinstance(node, ast.Call) else qualified(node.targets[0] if isinstance(node, ast.Assign) else node.target)
            records.append({'file': rel, 'line': node.lineno, 'area': part, 'classification': kind, 'symbol': symbol, 'snippet': qualified(node)[:240] if isinstance(node, (ast.Call, ast.Assign, ast.AnnAssign)) else ''})
    return records, errors


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    records, errors = collect(ROOT)
    by_kind = Counter(row['classification'] for row in records if row['area'] == 'production')
    by_area = Counter(row['area'] for row in records)
    sources = sorted({row['file'] for row in records if row['area'] == 'production'})
    prioritized = [row for row in records if row['area'] == 'production' and row['classification'] in ('explicit_entry_constructor', 'repository_constructor', 'registration_call_candidate', 'literature_reference_candidate')]
    summary = {'scope': 'static candidates in canonical Python sources, not unique mathematical statements', 'source_root': str(ROOT), 'production_candidates': by_area['production'], 'test_candidates': by_area['test'], 'production_files_with_candidates': len(sources), 'priority_candidates': len(prioritized), 'production_by_classification': dict(sorted(by_kind.items())), 'parse_errors': errors, 'not_yet_verified': ['actual registered statement totals', 'runtime-created registrations', 'literature ordering and availability', 'fixed statements versus internal proof steps', 'exact distinctness of references and statement instances']}
    write_csv(OUTPUT / 'classified_candidates.csv', records, ['file', 'line', 'area', 'classification', 'symbol', 'snippet'])
    write_csv(OUTPUT / 'registration_priority.csv', prioritized, ['file', 'line', 'area', 'classification', 'symbol', 'snippet'])
    write_csv(OUTPUT / 'production_files.csv', [{'file': f, 'candidate_count': sum(r['file'] == f for r in records)} for f in sources], ['file', 'candidate_count'])
    (OUTPUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Phase 163 R1B 登録候補の分類', '', '本報告は静的解析結果であり、実在する文献命題の確定件数ではありません。', '', '## 件数', '', f"- 本体候補: {by_area['production']}", f"- テスト候補: {by_area['test']}", f"- 登録・出典関連の優先候補: {len(prioritized)}", f"- 構文解析エラー: {len(errors)}", '', '## 本体分類（各候補は重複する命題を含み得る）', '']
    lines.extend(f'- {name}: {count}' for name, count in sorted(by_kind.items()))
    lines.extend(['', '## R1 完了前に必要な確認', '', '- 登録先ごとに実行時の登録件数を確認する', '- Statement 型と固定された文献主張を分ける', '- 文献位置が不明なら未確認と記録する', '- ProofStep と固定文献主張の重複を照合する', '- R2 のデータ構造はここでは追加しない'])
    (OUTPUT / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print('Reports:', OUTPUT)


if __name__ == '__main__':
    main()
