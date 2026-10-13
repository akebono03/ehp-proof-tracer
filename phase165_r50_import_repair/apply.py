from pathlib import Path
import ast
import shutil

project = Path(__file__).resolve().parent.parent
target = project / 'toda_group_proof_narrative_contribution_renderer.py'
source = target.read_text(encoding='utf-8-sig')
imports, separator, rest = source.partition('\ndef _provider_anchor_index(')
if not separator:
    raise RuntimeError('Unexpected module layout; source was not changed')
if 'import re\n' in imports or '\nimport re\r\n' in imports:
    print('import re already exists; no source change needed')
else:
    anchor = 'from collections import deque\n'
    if imports.count(anchor) != 1:
        raise RuntimeError('Import anchor missing or repeated; source was not changed')
    updated = source.replace(anchor, anchor + 'import re\n', 1)
    ast.parse(updated, filename=str(target))
    backup = Path(__file__).resolve().parent / 'backup_before_apply' / target.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup)
    target.write_text(updated, encoding='utf-8', newline='')
    print('R50 missing `import re` added; original backed up')
