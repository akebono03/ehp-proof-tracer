from __future__ import annotations

import ast
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / 'phase165_r55_nk_only_goal.py'
BACKUP = ROOT / 'phase166_r3q_web_publication_order_backups' / '20261020T103615Z' / 'phase165_r55_nk_only_goal.py'
OUTPUT = ROOT / 'phase166_r3q_recovery_results'


def function_bounds(source: str, name: str) -> tuple[int, int]:
    node = next((entry for entry in ast.parse(source).body
                 if isinstance(entry, (ast.FunctionDef, ast.AsyncFunctionDef)) and entry.name == name), None)
    if node is None:
        raise ValueError('missing expected function')
    lines = source.splitlines(keepends=True)
    return sum(map(len, lines[:node.lineno - 1])), sum(map(len, lines[:node.end_lineno]))


def main() -> None:
    if not TARGET.is_file() or not BACKUP.is_file():
        raise SystemExit('STOP: exact R3-Q source or timestamped prepatch backup is missing; nothing changed')
    current = TARGET.read_text(encoding='utf-8')
    previous = BACKUP.read_text(encoding='utf-8')
    a, b = function_bounds(current, 'search_group_from_registered_goal')
    c, d = function_bounds(previous, 'search_group_from_registered_goal')
    damaged = current[a:b]
    preserved = previous[c:d]
    required = ('証明目標に対応する掲載順付き型付き命題を一意に選択できない',
                'citing_assertion_id=citing_assertion_id', 'def contains_relation(')
    if all(item in damaged for item in required):
        if 'citing_assertion_id=citing_assertion_id' in preserved:
            raise SystemExit('STOP: backup unexpectedly includes R3-Q modification')
        restored = current[:a] + preserved + current[b:]
        ast.parse(restored)
        OUTPUT.mkdir(exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        shutil.copy2(TARGET, OUTPUT / f'phase165_r55_nk_only_goal_before_recovery_{stamp}.py')
        TARGET.write_text(restored, encoding='utf-8')
        status = 'RECOVERED'
    elif damaged == preserved:
        status = 'ALREADY_RECOVERED'
        OUTPUT.mkdir(exist_ok=True)
    else:
        raise SystemExit('STOP: live function differs from expected R3-Q version; nothing changed')
    updated = TARGET.read_text(encoding='utf-8')
    x, y = function_bounds(updated, 'search_group_from_registered_goal')
    (OUTPUT / 'RESTORED_FUNCTION.py.txt').write_text(updated[x:y], encoding='utf-8')
    report = {'status': status, 'modified_file': str(TARGET),
              'restored_from': str(BACKUP),
              'full_pytest_run': False,
              'preserved_other_functions': True,
              'restored_function_sha256': hashlib.sha256(updated[x:y].encode('utf-8')).hexdigest()}
    (OUTPUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
