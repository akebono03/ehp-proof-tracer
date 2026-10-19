from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

TARGETS = (
    'test_phase144_6_pi6_generic_production_route.py',
    'test_phase144_6_public_route_cutover.py',
)
MISSING_MODULE = 'tests.test_phase143_19_method_evidence'


def retire(root: Path) -> dict:
    root = root.resolve()
    tests = root / 'tests'
    if not (root / 'phase165_r6_closure_audit' / 'resumable_full_pytest.py').is_file():
        raise RuntimeError('Resumable Phase 165 runner not installed')
    if (tests / 'test_phase143_19_method_evidence.py').exists():
        raise RuntimeError('Missing dependency is now present: refusing retirement')
    contents = {}
    for name in TARGETS:
        src = tests / name
        if not src.is_file():
            raise RuntimeError(f'Expected file missing: {src}')
        data = src.read_bytes()
        if MISSING_MODULE.encode('ascii') not in data:
            raise RuntimeError(f'Expected missing-module import not found: {src}')
        if b'def _pi6_3_presentation_data():' not in data:
            raise RuntimeError(f'Expected legacy presentation fixture absent: {src}')
        contents[name] = data
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    archive = root / 'phase165_r6_audit_results' / 'retired_phase144_tests' / stamp
    archive.mkdir(parents=True, exist_ok=False)
    for name, data in contents.items():
        (archive / name).write_bytes(data)
    for name, data in contents.items():
        if (archive / name).read_bytes() != data:
            raise RuntimeError(f'Backup verification failed: {name}')
    for name in TARGETS:
        (tests / name).unlink()
    report = {
        'phase': '165 R6 final collection repair',
        'status': 'ARCHIVED',
        'archive': str(archive),
        'archived_files': list(TARGETS),
        'dependency_missing': MISSING_MODULE,
        'production_modified': False,
        'pytest_executed': False,
        'mathematical_coverage_replaced': False,
        'reason': 'Two historical Phase 144 renderer tests import missing Phase 143 fixture',
    }
    (archive / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    print(json.dumps(retire(root), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
