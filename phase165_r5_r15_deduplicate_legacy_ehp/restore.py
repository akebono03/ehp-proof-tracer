from pathlib import Path
HERE = Path(__file__).resolve().parent
BACKUP = HERE / 'phase162_web_narrative_integration.before_r5_r15.py'
TARGET = HERE.parent / 'phase162_web_narrative_integration.py'
if not BACKUP.is_file():
    raise SystemExit('No backup to restore')
TARGET.write_bytes(BACKUP.read_bytes())
BACKUP.unlink()
print('R5-R15 change rolled back')
