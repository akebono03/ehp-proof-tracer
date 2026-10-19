from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'phase165_r6_audit_results' / 'closure_check_fast'
OUT.mkdir(parents=True, exist_ok=True)

def main() -> int:
    reports = sorted((ROOT / 'phase165_r6_audit_results' / 'old_proof_retirement').glob('*/report.json'))
    result = {'phase': '165 R6', 'mode': 'READ_ONLY', 'full_pytest_run': False, 'timestamp': datetime.now(timezone.utc).isoformat(), 'old_report': str(reports[-1]) if reports else None}
    if reports:
        try:
            prior = json.loads(reports[-1].read_text(encoding='utf-8'))
            result['old_report_data'] = {k: v for k, v in prior.items() if k in ('status', 'removed', 'remaining_collection_errors', 'full_pytest_run')}
        except (OSError, ValueError) as exc:
            result['old_report_error'] = str(exc)
    patterns = ('*phase165*r52*test*.py', '*phase165*r57*test*.py', '*phase165*backward*test*.py')
    candidates = sorted({p for pat in patterns for p in ROOT.glob(pat) if p.is_file()})
    candidates.extend(sorted(p for p in (ROOT / 'tests').glob('test_phase165*.py') if p.is_file() and any(s in p.name.lower() for s in ('r52', 'r57', 'backward'))))
    candidates = list(dict.fromkeys(candidates))[:3]
    result['candidate_tests'] = [str(p.relative_to(ROOT)) for p in candidates]
    print('候補テスト:', result['candidate_tests'], flush=True)
    if candidates:
        cmd = [sys.executable, '-m', 'pytest', '-q', '--maxfail=1', *[str(p.relative_to(ROOT)) for p in candidates]]
        print('限定テスト実行（最大60秒）:', ' '.join(cmd), flush=True)
        try:
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=60)
            (OUT / 'focused.log').write_text(p.stdout + '\n' + p.stderr, encoding='utf-8')
            result['focused_returncode'] = p.returncode
            print((p.stdout + '\n' + p.stderr)[-5000:], flush=True)
        except subprocess.TimeoutExpired:
            result['focused_returncode'] = 'TIMEOUT_60_SECONDS'
            print('限定テストが60秒でタイムアウトしました。', flush=True)
    else:
        result['focused_returncode'] = 'NO_MATCHING_TEST_FILES'
    target = OUT / 'report.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('結果:', target, flush=True)
    return 0
if __name__ == '__main__':
    sys.exit(main())
