"""Apply a small, reversible delegation in the current web_group_proof function."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
source = root / "web_group_proof.py"
backup = root / "web_group_proof.phase162_r4_b3_web_pre_change.bak"
new_module = root / "phase162_r4_b3_web_common_display.py"
bundle_module = Path(__file__).resolve().parent / "files" / new_module.name
text = source.read_text(encoding="utf-8")
anchor = (
    'def build_standard_web_group_proof_view(\n'
    '  n: int,\n'
    '  k: int,\n'
    '  max_depth: int = 2,\n'
    '  mode: str = "narrative",\n'
    ') -> WebGroupProofView:\n'
)
insert = (
    '  if (\n'
    '    mode == "narrative"\n'
    '    and k == 1\n'
    '    and n in (4, 5)\n'
    '  ):\n'
    '    from phase162_r4_b3_web_common_display import (\n'
    '      build_phase162_r4_b3_web_common_display_view,\n'
    '    )\n'
    '    return build_phase162_r4_b3_web_common_display_view(\n'
    '      n=n, k=k, max_depth=max_depth,\n'
    '    )\n\n'
)
if text.count(anchor) != 1:
    raise RuntimeError("Unexpected web_group_proof.py: function signature mismatch")
if insert not in text:
    if not backup.exists():
        shutil.copy2(source, backup)
    source.write_text(text.replace(anchor, anchor + insert, 1), encoding="utf-8")
    print("Updated:", source.name)
else:
    print("Already patched:", source.name)
shutil.copy2(bundle_module, new_module)
print("Updated:", new_module.name)
print("Backup:", backup.name)
