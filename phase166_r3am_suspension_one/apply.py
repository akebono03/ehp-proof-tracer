from pathlib import Path
import ast
import shutil

root = Path.cwd()
path = root / 'toda_human_readable_renderer.py'
bundle = Path(__file__).resolve().parent
source = path.read_text(encoding='utf-8-sig')
tree = ast.parse(source)
functions = [item for item in tree.body if isinstance(item, ast.FunctionDef) and item.name == 'render_toda_expression_latex']
if len(functions) != 1:
    raise RuntimeError('Expected one render_toda_expression_latex function')
node = functions[0]
lines = source.splitlines(keepends=True)
original = ''.join(lines[node.lineno - 1:node.end_lineno])
old = '''  if isinstance(\n    expression,\n    IteratedSuspension,\n  ):\n    return (\n      "E^{"\n      + _render_scalar_latex(\n        expression.exponent\n      )\n      + "}"\n      + render_toda_expression_latex(\n        expression.expression\n      )\n    )'''
new = '''  if isinstance(\n    expression,\n    IteratedSuspension,\n  ):\n    prefix = (\n      "E"\n      if type(expression.exponent) is int and expression.exponent == 1\n      else "E^{" + _render_scalar_latex(expression.exponent) + "}"\n    )\n    return prefix + render_toda_expression_latex(expression.expression)'''
normalized = original.replace('\r\n','\n')
if new in normalized:
    print('ALREADY_APPLIED:', path)
    final_function = normalized
elif normalized.count(old) != 1:
    raise RuntimeError('Unexpected renderer implementation; no file modified')
else:
    final_function = normalized.replace(old, new, 1)
    new_source = ''.join(lines[:node.lineno-1]) + final_function + '\n' + ''.join(lines[node.end_lineno:])
    ast.parse(new_source)
    backup = root/'phase166_r3am_suspension_one_backup'
    backup.mkdir(exist_ok=True)
    shutil.copy2(path,backup/path.name)
    path.write_text(new_source, encoding='utf-8')
    print('PATCHED:',path)
    print('BACKUP:', backup/path.name)
(bundle/'render_toda_expression_latex_full.py.txt').write_text(final_function+'\n',encoding='utf-8')
print('FULL FUNCTION:', bundle/'render_toda_expression_latex_full.py.txt')
