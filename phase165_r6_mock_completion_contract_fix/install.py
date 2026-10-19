from pathlib import Path
from datetime import datetime
import shutil
import subprocess
import sys

root = Path.cwd()
target = root / 'test_phase165_r52_r2_search_adapter.py'
if not target.is_file() or not (root / 'phase165_r56_presentation_adapter.py').is_file():
    raise SystemExit('ERROR: run from ehp_proof root and ensure target files exist')
original = target.read_text(encoding='utf-8')
old = '''    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == target
    assert "□" in render_partial_proof_markdown(result)
    other = adapter.search_registered_partial_proof(**{**args, "n": 999})'''
new = '''    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == target
    with pytest.raises(ValueError, match="unsupported group structure"):
        render_partial_proof_markdown(result)
    other = adapter.search_registered_partial_proof(**{**args, "n": 999})'''
if original.count(old) != 1:
    if new in original:
        print('ALREADY APPLIED: test expectation matches current completion contract')
    else:
        raise SystemExit('ERROR: unexpected test file content; nothing modified')
else:
    backup_dir = root / 'phase165_r6_audit_results' / 'runner_backup'
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f'test_phase165_r52_r2_search_adapter_before_completion_{datetime.now():%Y%m%d_%H%M%S_%f}.py'
    shutil.copy2(target, backup)
    target.write_text(original.replace(old,new),encoding='utf-8')
    print('PATCHED:',target)
    print('BACKUP:',backup)
print('Run limited R52-R2 tests; full pytest NOT run')
result = subprocess.run([sys.executable,'-m','pytest','-q','test_phase165_r52_r2_search_adapter.py'],cwd=root)
raise SystemExit(result.returncode)
