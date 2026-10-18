from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

TARGETS = (
    'phase165_r52_r4_flask_bridge.py',
    'phase165_r52_r3_web_adapter.py',
    'phase165_r56_presentation_adapter.py',
    'phase165_r52_partial_proof.py',
    'phase165_r55_nk_only_goal.py',
    'phase165_r57_r10_step_narrative.py',
    'toda_group_proof_narrative_renderer.py',
)


def audit(root: Path) -> dict:
    files = sorted(p for p in root.rglob('*.py') if not any(x in p.parts for x in ('.git', '.venv', 'venv', '__pycache__')))
    checked = {}
    parse_errors = {}
    for rel in TARGETS:
        path = root / rel
        if not path.is_file():
            checked[rel] = {'present': False}
            continue
        source = path.read_text(encoding='utf-8-sig')
        try:
            tree = ast.parse(source, filename=rel)
        except SyntaxError as exc:
            parse_errors[rel] = str(exc)
            checked[rel] = {'present': True, 'syntax_ok': False}
            continue
        module = path.stem
        references = []
        # Search all Python files including tests, and inspect source literally so
        # string-based dynamic imports are counted as possible consumers.
        pattern = re.compile(r'(?<![A-Za-z0-9_])' + re.escape(module) + r'(?![A-Za-z0-9_])')
        for other in files:
            if other == path:
                continue
            try:
                text = other.read_text(encoding='utf-8-sig')
            except (OSError, UnicodeError):
                continue
            if pattern.search(text):
                references.append(str(other.relative_to(root)))
        functions = [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        checked[rel] = {
            'present': True,
            'syntax_ok': True,
            'top_level_functions': functions,
            'possible_python_consumers_count': len(references),
            'possible_python_consumers_sample': references[:40],
            'interpretation': 'candidate_not_proven_unused',
        }
    return {
        'phase': '165 R5',
        'mode': 'READ_ONLY_CONSERVATIVE_AUDIT',
        'python_files_scanned': len(files),
        'targets': checked,
        'syntax_errors': parse_errors,
        'deleted_files': [],
        'modified_production_files': [],
        'cleanup_decision': 'NO_DELETION_WITHOUT_VERIFIED_REACHABILITY_AND_REGRESSION',
        'limitations': [
            'AST and literal reference scanning cannot prove runtime dead code.',
            'Non-Python callers, Jinja templates, generated modules and runtime imports may escape the scan.',
            'Local uncommitted work and R2/R3/R4 artifacts are not modified.',
        ],
        'full_pytest_run': False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not (args.root / 'phase165_r52_r4_flask_bridge.py').is_file():
        raise SystemExit('ERROR: run from project root; no files modified')
    report = audit(args.root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('R5 READ-ONLY audit complete; Python files scanned:', report['python_files_scanned'])
    print('No deletions and no production modifications.')
    for name, item in report['targets'].items():
        print(name, 'present=', item.get('present'), 'possible_consumers=', item.get('possible_python_consumers_count', 'n/a'))
    print('Report:', args.output)


if __name__ == '__main__':
    main()
