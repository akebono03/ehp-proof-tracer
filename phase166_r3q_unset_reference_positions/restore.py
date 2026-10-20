"""Restore the precise file installed by apply.py if targeted tests fail."""
import hashlib
import json
from pathlib import Path
state_path = Path(__file__).parent / 'last_install.json'
if not state_path.exists():
    raise SystemExit('No applied patch recorded')
state = json.loads(state_path.read_text(encoding='utf-8'))
target = Path(state['target'])
backup = Path(state['backup'])
current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
if current_hash != state['patched_sha256']:
    raise SystemExit('Current file changed since patch; refusing automatic overwrite')
if hashlib.sha256(backup.read_bytes()).hexdigest() != state['original_sha256']:
    raise SystemExit('Backup checksum mismatch; refusing restore')
target.write_bytes(backup.read_bytes())
print('RESTORED:', target)
