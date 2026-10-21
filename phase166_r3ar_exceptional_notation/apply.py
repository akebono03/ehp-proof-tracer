from pathlib import Path
import ast
import shutil

root = Path(__file__).resolve().parent.parent
source = root / 'toda_human_readable_renderer.py'
backup_dir = root / 'phase166_r3ar_exceptional_notation_backup'
backup_dir.mkdir(exist_ok=True)
backup = backup_dir / source.name
body = source.read_text(encoding='utf-8')
start = body.index('def _render_unicode_math_name_latex(')
end = body.index('\ndef _render_scalar_latex(', start)
old = body[start:end]
needle = '''  pieces: list[str] = []'''
insert = '''  # Normalize exceptional DB labels without altering their typed identity.
  # The source HyoujiGen.csv stores these labels as Unicode, while their
  # mathematical TeX equivalents use nested bars and numeric subscripts.
  import re

  bar_pattern = re.compile(r"([Α-Ωα-ω])([\\u0304\\u0305]+)")

  def render_bars(match):
    base = _GREEK_LATEX.get(match.group(1), match.group(1))
    level = len(match.group(2))
    for _ in range(level):
      base = r"\\bar{" + base + "}"
    return base

  name = bar_pattern.sub(render_bars, name)
  index_pattern = re.compile(r"([Α-Ωα-ω])([0-9]+)")
  name = index_pattern.sub(
    lambda match: match.group(1) + "".join(
      next(key for key, value in _SUBSCRIPT_DIGITS.items() if value == digit)
      for digit in match.group(2)
    ),
    name,
  )

'''
if 'bar_pattern = re.compile' in old:
    print('ALREADY PATCHED:', source)
else:
    if old.count(needle) != 1:
        raise RuntimeError('Unexpected Unicode renderer function; no changes made')
    new = old.replace(needle, insert + needle, 1)
    patched = body[:start] + new + body[end:]
    ast.parse(patched, filename=str(source))
    if not backup.exists():
        shutil.copy2(source, backup)
    source.write_text(patched, encoding='utf-8')
    print('PATCHED:', source)
    print('BACKUP:', backup)
updated = source.read_text(encoding='utf-8')
s = updated.index('def _render_unicode_math_name_latex(')
e = updated.index('\ndef _render_scalar_latex(', s)
full = Path(__file__).with_name('_render_unicode_math_name_latex_full.py.txt')
full.write_text(updated[s:e], encoding='utf-8')
print('FULL FUNCTION:', full)
