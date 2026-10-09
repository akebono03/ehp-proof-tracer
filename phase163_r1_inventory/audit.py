from __future__ import annotations
import ast
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'phase163_r1_inventory_output'
OUT.mkdir(exist_ok=True)
EXCLUDED = {'archive', '.git', '.venv', 'venv', '__pycache__', 'node_modules', '.pytest_cache'}
PATTERNS = ('registry', 'repository', 'reference', 'theorem', 'statement', 'literature', 'fact', 'rule')
TARGET_NAMES = ('toda_rules.py', 'theorem_facts.py', 'standard_repository.py', 'proof_repository.py')

def allowed(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return not any(s in EXCLUDED for s in rel.parts) and not any(s.startswith('phase') and s != 'phase163_r1_inventory' for s in rel.parts[:-1])

def expr(node: ast.AST | None) -> str:
    return ast.unparse(node) if node is not None else ''

def audit() -> dict:
    rows: list[dict] = []
    files: list[dict] = []
    errors: list[dict] = []
    for path in sorted(ROOT.rglob('*.py')):
        if not allowed(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            src = path.read_text(encoding='utf-8-sig')
            tree = ast.parse(src, filename=rel)
        except (OSError, SyntaxError, UnicodeError) as e:
            errors.append({'file': rel, 'error': str(e)})
            continue
        name_matches = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if any(p in node.name.lower() for p in PATTERNS):
                    rows.append({'file': rel, 'line': node.lineno, 'kind': type(node).__name__, 'symbol': node.name, 'value': '', 'evidence': 'declaration'})
                    name_matches.append(node.name)
            elif isinstance(node, ast.Call):
                call = expr(node.func)
                if any(p in call.lower() for p in ('register', 'repositoryentry', 'theoremfactentry', 'literaturereference')):
                    rows.append({'file': rel, 'line': node.lineno, 'kind': 'Call', 'symbol': call, 'value': '; '.join(k.arg + '=' + expr(k.value)[:120] for k in node.keywords if k.arg), 'evidence': 'candidate registration (not unique)'})
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    names = [n.id for n in ast.walk(target) if isinstance(n, ast.Name)]
                    for name in names:
                        if any(p in name.lower() for p in ('registry', 'repository', 'facts', 'entries')):
                            rows.append({'file': rel, 'line': node.lineno, 'kind': 'Assignment', 'symbol': name, 'value': expr(node.value)[:250], 'evidence': 'candidate container'})
        if rel in TARGET_NAMES or name_matches or any(p in path.stem.lower() for p in ('registry','repository','theorem_fact')):
            files.append({'file':rel,'matched_definitions':len(name_matches),'line_count':len(src.splitlines()),'is_test':rel.startswith('tests/')})
    def write_csv(name: str, data: list[dict], fields: list[str]):
        with (OUT / name).open('w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(data)
    write_csv('candidate_sites.csv', rows, ['file','line','kind','symbol','value','evidence'])
    write_csv('candidate_files.csv', files, ['file','matched_definitions','line_count','is_test'])
    summary = {'scope':'canonical Python files, excluding archived and phase patch directories', 'source_root':str(ROOT), 'candidate_rows':len(rows), 'candidate_files':len(files), 'by_kind':dict(Counter(r['kind'] for r in rows)), 'parse_errors':errors, 'known_limits':['AST candidates are not distinct theorem counts','runtime-generated registrations are not evaluated','literature order and proof availability are not inferred','review output manually before Phase 163 R2']}
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Phase 163 R1: 命題登録候補の棚卸し','',f'- 候補行数: {len(rows)}',f'- 候補ファイル数: {len(files)}',f'- 解析失敗: {len(errors)}','', '本監査は読み取り専用です。候補の件数は命題の件数ではありません。', '文献順序、証明完了位置、依存関係は推定していません。','', '## 登録候補の種別']
    lines += [f'- {k}: {v}' for k,v in sorted(summary['by_kind'].items())]
    lines += ['', '## 主要ファイル', '']
    for row in files:
        if Path(row['file']).name in TARGET_NAMES:
            lines.append(f"- `{row['file']}`: {row['matched_definitions']} definitions")
    lines += ['', '## 次の確認', '', 'candidate_sites.csv で登録処理と単なる参照表現を区別し、実行時登録件数を別途確認する。']
    (OUT/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return summary

if __name__ == '__main__':
    result = audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print('Reports:', OUT)
