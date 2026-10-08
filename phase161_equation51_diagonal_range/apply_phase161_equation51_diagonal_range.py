from pathlib import Path
import sys

root = Path(__file__).resolve().parent.parent
catalog = root / "toda_literature_statement_boundary.py"
renderer = root / "toda_group_proof_narrative_references.py"

old_catalog = '''    component_key="diagonal_identity_group",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
'''
new_catalog = old_catalog.replace("range_text=None,", 'range_text="n >= 1",')

old_render = r'''      if "diagonal_identity_group" in component_keys:
        lines.append(
          (
            r"$\pi_{n}^{n} = "
            r"\mathbb{Z}\{\iota_{n}\}$."
          )
        )
'''
new_render = r'''      if "diagonal_identity_group" in component_keys:
        component = get_toda_fixed_statement_component(
          "(5.1)",
          "diagonal_identity_group",
        )
        range_latex = ""
        if component.range_text is not None:
          range_latex = (
            r"\qquad ("
            + component.range_text.replace(">=", r"\ge").replace("<=", r"\le")
            + ")"
          )
        lines.append(
          (
            r"$\pi_{n}^{n} = "
            r"\mathbb{Z}\{\iota_{n}\}"
            + range_latex
            + "$."
          )
        )
'''

def prepare(path, old, new):
    source = path.read_text(encoding="utf-8")
    if new in source:
        print(f"Already updated: {path.name}")
        return None
    if source.count(old) != 1:
        raise RuntimeError(f"Expected exactly one unchanged target in {path.name}; found {source.count(old)}")
    return source.replace(old, new, 1)

# Both anchors are checked before either file is written.
changes = [(catalog, prepare(catalog, old_catalog, new_catalog)),
           (renderer, prepare(renderer, old_render, new_render))]
for path, content in changes:
    if content is not None:
        path.write_text(content, encoding="utf-8")
        print(f"Updated: {path}")
