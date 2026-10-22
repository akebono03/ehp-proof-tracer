from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / 'phase166_r3t_goal_source_binding' / 'test_connection.py'
SOURCE = PACKAGE / 'test_connection.py'
if not TARGET.is_file():
    raise SystemExit(f'Missing expected test file: {TARGET}')
prior = TARGET.read_text(encoding='utf-8-sig')
if 'def test_pi43_is_not_assigned_pi54_citing_id' not in prior or 'def test_pi32_is_not_assigned_pi54_citing_id' not in prior:
    raise SystemExit('Unexpected test contents; no files changed')
backup = PACKAGE / 'backup' / datetime.now().strftime('%Y%m%dT%H%M%S') / 'test_connection.py'
backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(TARGET, backup)
shutil.copy2(SOURCE, TARGET)
print('PATCHED:', TARGET)
print('BACKUP:', backup)
print('FULL_TEST_FILE:', SOURCE)
