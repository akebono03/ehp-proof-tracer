from __future__ import annotations
import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / 'phase165_r56_presentation_adapter.py'
REPLACEMENT = PACKAGE / 'phase165_r56_presentation_adapter.py'
BACKUP = ROOT / 'phase165_r56_presentation_adapter.before_renderer_restore_r1.py'


def main():
    old = TARGET.read_text(encoding='utf-8')
    new = REPLACEMENT.read_text(encoding='utf-8')
    ast.parse(old)
    ast.parse(new)
    if old == new:
        print('Original completed Narrative already restored')
        return
    # Fail closed: do not replace unknown evolved adapter versions.
    if ('return render_toda_partial_proof_narrative_markdown(result)' not in old
            or 'def render_completed_shared_narrative(result: PartialProofResult)' not in old
            or 'build_complete_toda_group_result_proof_replay' not in old):
        raise RuntimeError('Unexpected adapter version; no file was changed')
    if BACKUP.exists():
        raise RuntimeError('Existing restore backup; no file was changed')
    BACKUP.write_text(old, encoding='utf-8')
    TARGET.write_text(new, encoding='utf-8')
    print('Restored original completed Narrative adapter')
    print('Backup:', BACKUP)


if __name__ == '__main__':
    main()
