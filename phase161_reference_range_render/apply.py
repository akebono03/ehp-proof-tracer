from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
path = root / 'toda_group_proof_narrative_references.py'
source = path.read_text(encoding='utf-8')
tree = ast.parse(source)
name = 'render_toda_group_proof_narrative_reference_entries_markdown'
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
if len(functions) != 1:
    raise RuntimeError('expected exactly one reference rendering function')
node = functions[0]
lines = source.splitlines(keepends=True)
original = ''.join(lines[node.lineno - 1:node.end_lineno])
if 'component.range_text' in original:
    print('Already applied')
else:
    addition = r'''    for statement_line in statement_lines:
      # A catalog range belongs to its general formula, not to an
      # unrelated specialization or another component of the same theorem.
      applicable_ranges = []
      fixed_keys = set()
      for proof_step in entry.proof_steps:
        boundary = classify_toda_literature_statement_step(proof_step)
        if (
          boundary is not None
          and boundary.classification
          == TodaLiteratureStatementClassification.FIXED_STATEMENT
          and boundary.reference_locator == entry.reference.locator
          and boundary.component_key is not None
        ):
          fixed_keys.add(boundary.component_key)

      for component in get_toda_fixed_statement_components(
        entry.reference.locator
      ):
        if component.range_text is None:
          continue
        range_variable = component.range_text.split()[0]
        # Symbolic indices are required in the displayed formula.
        if re.search(
          r"(?<![A-Za-z])" + re.escape(range_variable) + r"(?![A-Za-z])",
          statement_line,
        ) is None:
          continue
        # Explicit component matches are preferred; aggregate carriers
        # can use the unique matching symbolic statement component.
        if fixed_keys and component.component_key not in fixed_keys:
          continue
        rendered_range = (
          component.range_text.replace(">=", r"\ge ")
          .replace("<=", r"\le ")
        )
        if rendered_range not in applicable_ranges:
          applicable_ranges.append(rendered_range)

      if len(applicable_ranges) == 1 and statement_line.startswith("$"):
        range_suffix = r"$\;(" + applicable_ranges[0].strip() + ")$"
        if range_suffix not in statement_line:
          if statement_line.endswith("."):
            statement_line = statement_line[:-1] + " " + range_suffix + "."
          else:
            statement_line += " " + range_suffix
      lines.append(statement_line)
'''
    old = '''    for statement_line in statement_lines:
      lines.append(
        statement_line
      )
'''
    if original.count(old) != 1:
        raise RuntimeError('unexpected rendering function structure; no changes made')
    changed = original.replace(old, addition)
    lines[node.lineno - 1:node.end_lineno] = [changed]
    updated = ''.join(lines)
    ast.parse(updated)
    path.write_text(updated, encoding='utf-8')
    print(f'Updated: {path}')
