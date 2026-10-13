"""R50: retain the typed Delta exactness reason when fixed references are shown."""
from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r49_display_order.py"
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    old = '''        if len(detailed) != 1:
            continue
        rendered = _render_generic_narrative_step(reason.conclusion_step)
'''
    new = '''        if not detailed:
            # After the Reference boundary becomes visible, an existing body
            # suppression pass can keep the Delta conclusion but discard the
            # accompanying exactness reason. Restore it from the typed reason,
            # replacing that same conclusion rather than adding another copy.
            from toda_group_proof_narrative_reason_renderer import (
                render_toda_group_proof_narrative_reason_sentence,
            )
            explanation = render_toda_group_proof_narrative_reason_sentence(reason)
            conclusion = _render_generic_narrative_step(reason.conclusion_step)
            if explanation and conclusion:
                bare_hits = [
                    i for i, paragraph in enumerate(paragraphs)
                    if normalize(paragraph) == normalize(conclusion)
                    and "\\\\operatorname{Im}" not in paragraph
                ]
                if len(bare_hits) == 1:
                    paragraphs[bare_hits[0]] = explanation
                    detailed = [bare_hits[0]]
        if len(detailed) != 1:
            continue
        rendered = _render_generic_narrative_step(reason.conclusion_step)
'''
    if 'After the Reference boundary becomes visible' in text:
        print('R50 reason-preservation repair already installed')
        return
    if text.count(old) != 1:
        raise RuntimeError(f'R50 expected one Delta branch anchor, found {text.count(old)}; no changes')
    updated = text.replace(old, new, 1)
    ast.parse(updated, filename=TARGET.name)
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP / TARGET.name)
    TARGET.write_text(updated, encoding="utf-8")
    print('R50 reason-preservation repair installed; R49 helper backed up')


if __name__ == '__main__':
    main()
