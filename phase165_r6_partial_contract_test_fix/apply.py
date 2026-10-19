from pathlib import Path
import ast
import shutil
from datetime import datetime, timezone
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
CHANGES = {
    'test_phase165_r52_partial_proof.py': {
      'test_r52_arbitrary_range_and_unknown': (
          'assert "unknown" in text', 'assert "探索状態：未探索" in text'),
      'test_r52_complete_requires_matching_step': (
          'assert "□" in render_partial_proof_markdown(valid)',
          'with pytest.raises(ValueError, match="completed target does not match conclusion"):\n        render_partial_proof_markdown(valid)'),
    },
    'test_phase165_r52_r3_web_adapter.py': {
      'test_partial_result_keeps_observed_steps_and_unresolved_goals': (
          'assert "Reference" in _visible_text(view)',
          'assert "参照情報を持つ ProofStep はありません。" in _visible_text(view)\n    assert "General theorem" not in _visible_text(view)'),
    },
}

def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = ROOT / 'phase165_r6_audit_results' / 'runner_backup' / ('partial_contract_' + stamp)
    pending = {}
    for filename, replacements in CHANGES.items():
        path = ROOT / filename
        source = path.read_text(encoding='utf-8')
        tree = ast.parse(source)
        functions = {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef)}
        for name, (old, new) in replacements.items():
            if name not in functions:
                raise RuntimeError(f'Missing test: {filename}:{name}')
            node = functions[name]
            segment = '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno])
            if segment.count(old) != 1:
                raise RuntimeError(f'Unexpected source: {filename}:{name}: {segment.count(old)} matches')
        altered = source
        for old, new in replacements.values():
            altered = altered.replace(old, new, 1)
        ast.parse(altered)
        pending[path] = (source,altered)
    backup.mkdir(parents=True, exist_ok=False)
    for path, (source, altered) in pending.items():
        shutil.copy2(path, backup/path.name)
        path.write_text(altered, encoding='utf-8', newline='')
        print('PATCHED:', path)
    print('BACKUP:', backup)
    tests = [
        'test_phase165_r52_partial_proof.py::test_r52_arbitrary_range_and_unknown',
        'test_phase165_r52_partial_proof.py::test_r52_complete_requires_matching_step',
        'test_phase165_r52_r3_web_adapter.py::test_partial_result_keeps_observed_steps_and_unresolved_goals',
        'test_phase165_r52_r3_web_adapter.py::test_failed_and_unknown_state_does_not_claim_completion',
    ]
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', *tests], cwd=ROOT)
    print('R6 LIMITED PYTEST EXIT:',result.returncode,'; FULL SUITE NOT RUN')
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
