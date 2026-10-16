from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = {
    'pi32_goal': '旧 Goal 生成。文献登録側で利用中',
    'reconstruct_registered_pi32': '旧専用証明再構築。旧 Replay 等から利用中',
    'phase165_r34_expansions': '旧前提生成。現在の共通規則へ統合する必要',
    'expand_existing_pi43_rules': '共通入口から直接利用中。R6-2 で共通化後削除',
    'RegisteredProofProvider': '撤去済み Provider クラス',
    'registered_proof_providers': '撤去済み Provider 関数',
}

def inspect():
    files = sorted(ROOT.glob('*.py'))
    report = {k: [] for k in TARGETS}
    for path in files:
        try:
            source = path.read_text(encoding='utf-8-sig')
            tree = ast.parse(source, filename=str(path))
        except (UnicodeError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.Call, ast.ImportFrom)):
                if isinstance(node, ast.Call):
                    name = node.func.id if isinstance(node.func, ast.Name) else (node.func.attr if isinstance(node.func, ast.Attribute) else None)
                    names = [name] if name else []
                    kind = 'call'
                else:
                    names = [alias.name for alias in node.names]
                    kind = 'import'
                for name in names:
                    if name in report:
                        report[name].append({'file': path.name, 'line': node.lineno, 'kind': kind})
    return {'phase':'165 R6-1 R4', 'scope':'root python modules only', 'usages':report,
            'production_modified':False, 'full_pytest_run':False}

if __name__ == '__main__':
    data = inspect()
    output = Path(__file__).with_name('remaining_paths.json')
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2),encoding='utf-8')
    print(json.dumps({'output':str(output), 'counts':{k:len(v) for k,v in data['usages'].items()}, 'full_pytest_run':False},ensure_ascii=False,indent=2))
