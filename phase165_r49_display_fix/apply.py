"""Install only the R49 final typed-reason order bridge."""
from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_contribution_renderer.py'
MODULE = Path(__file__).resolve().parent / 'phase165_r49_display_order.py'
DEST = ROOT / MODULE.name
BACKUP = Path(__file__).resolve().parent / 'backup_before_apply'


def main():
    source = TARGET.read_text(encoding='utf-8')
    original_module = DEST.read_text(encoding='utf-8') if DEST.exists() else None
    import_statement = 'from phase165_r49_display_order import finalize_phase165_r49_typed_reason_order\n'
    anchor = '''  rendered = (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

  reference_section = ('''
    replacement = '''  rendered = (
    finalize_phase165_r49_typed_reason_order(
      rendered,
      reason_sidecar,
    )
  )
  rendered = (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

  reference_section = ('''
    if import_statement in source and replacement in source:
        print('R49 display bridge already installed')
        return
    if source.count(anchor) != 1:
        raise RuntimeError(f'Expected one final-link anchor; found {source.count(anchor)}. No files changed.')
    if import_statement in source:
        raise RuntimeError('Unexpected partially installed import; no files changed.')
    updated = import_statement + source.replace(anchor, replacement, 1)
    ast.parse(updated, filename=TARGET.name)
    ast.parse(MODULE.read_text(encoding='utf-8'), filename=MODULE.name)
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP / TARGET.name)
    if original_module is not None:
        shutil.copy2(DEST, BACKUP / DEST.name)
    DEST.write_bytes(MODULE.read_bytes())
    TARGET.write_text(updated, encoding='utf-8')
    print('R49 display bridge installed; original renderer backed up')


if __name__ == '__main__':
    main()
