from pathlib import Path
import shutil

repo = Path.cwd()
package = Path(__file__).resolve().parent

new_module = repo / "toda_group_proof_narrative_equation_numbering.py"
shutil.copyfile(
  package / "toda_group_proof_narrative_equation_numbering.py",
  new_module,
)

test_target = (
  repo
  / "tests"
  / "test_phase144_5_generic_definition_order_equations.py"
)
shutil.copyfile(
  package / "test_phase144_5_generic_definition_order_equations.py",
  test_target,
)

renderer_path = (
  repo
  / "toda_group_proof_narrative_argument_multi_renderer.py"
)
text = renderer_path.read_text(
  encoding="utf-8-sig"
)

import_anchor = """from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
"""
import_addition = """from toda_group_proof_narrative_equation_numbering import (
  number_toda_group_proof_narrative_equations,
)
"""

if import_addition not in text:
  if import_anchor not in text:
    raise RuntimeError(
      "Phase 144-5 import anchor was not found."
    )
  text = text.replace(
    import_anchor,
    import_anchor + import_addition,
    1,
  )

old_return = """  return "\\n\\n".join(
    rendered_arguments
  )
"""
new_return = """  rendered = "\\n\\n".join(
    rendered_arguments
  )

  return (
    number_toda_group_proof_narrative_equations(
      rendered
    )
  )
"""

if new_return not in text:
  if old_return not in text:
    raise RuntimeError(
      "Phase 144-5 final return anchor was not found."
    )
  text = text.replace(
    old_return,
    new_return,
    1,
  )

renderer_path.write_text(
  text,
  encoding="utf-8",
)

print("Phase 144-5 applied.")
print("Modified:")
print("  toda_group_proof_narrative_argument_multi_renderer.py")
print("Added:")
print("  toda_group_proof_narrative_equation_numbering.py")
print("  tests/test_phase144_5_generic_definition_order_equations.py")
print("")
print("Definition / Order semantic and purpose-sentence code was already generic")
print("in the current repository, so it was intentionally not rewritten.")
