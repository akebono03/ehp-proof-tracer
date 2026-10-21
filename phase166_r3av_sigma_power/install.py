from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
source = root / 'toda_human_readable_renderer.py'
backup = root / 'phase166_r3av_sigma_power_backup' / 'toda_human_readable_renderer.py'
backup.parent.mkdir(exist_ok=True)
text = source.read_text(encoding='utf-8')
old = '''  if isinstance(
    expression,
    Composition,
  ):
    return (
      render_toda_expression_latex(
        expression.left
      )
      + render_toda_expression_latex(
        expression.right
      )
    )
'''
new = '''  if isinstance(
    expression,
    Composition,
  ):
    # Compress only a well-typed consecutive sigma family composition.
    # This is a presentation rule: the Composition tree is unchanged.
    factors = []

    def collect_composition_factors(value):
      if isinstance(value, Composition):
        collect_composition_factors(value.left)
        collect_composition_factors(value.right)
      else:
        factors.append(value)

    collect_composition_factors(expression)
    if len(factors) >= 2:
      sigma_indices = []
      for factor in factors:
        if not isinstance(factor, HomotopyElement):
          break
        symbol = factor.generator
        if (
          symbol is None
          or symbol.family not in ("σ", r"\\sigma")
          or type(symbol.index) is not int
          or factor.target != symbol.index
          or factor.source != symbol.index + 7
        ):
          break
        sigma_indices.append(symbol.index)
      if len(sigma_indices) == len(factors) and all(
        following == preceding + 7
        for preceding, following in zip(sigma_indices, sigma_indices[1:])
      ):
        return (
          render_toda_expression_latex(factors[0])
          + "^{" + str(len(factors)) + "}"
        )

    return (
      render_toda_expression_latex(
        expression.left
      )
      + render_toda_expression_latex(
        expression.right
      )
    )
'''
if text.count(old) != 1:
    raise SystemExit('Expected Composition renderer block not uniquely found; no change applied')
shutil.copy2(source, backup)
source.write_text(text.replace(old,new), encoding='utf-8')
print('PATCHED:',source)
print('BACKUP:',backup)
print('FULL FUNCTION: see file after patch (render_toda_expression_latex)')
