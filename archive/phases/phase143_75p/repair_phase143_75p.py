from pathlib import Path

PATH = Path("toda_group_proof_narrative_renderer.py")
if not PATH.exists():
  raise SystemExit("toda_group_proof_narrative_renderer.py was not found.")

original = PATH.read_text(encoding="utf-8")
text = original
helper_name = "_render_prop44_suspension_injective_statement_latex"

helper = """

def _render_prop44_suspension_injective_statement_latex(
  statement,
) -> str | None:
  if (
    type(statement).__name__
    != "TodaProp44SuspensionInjectiveStatement"
  ):
    return None

  suspension_map = statement.map

  return (
    "E: "
    + render_toda_primary_group_latex(
      suspension_map.source_group
    )
    + r" \\hookrightarrow "
    + render_toda_primary_group_latex(
      suspension_map.target_group
    )
  )
"""

if "def " + helper_name + "(" not in text:
  marker = "def _render_group_proof_narrative_latex("
  index = text.find(marker)
  if index < 0:
    raise SystemExit("Could not find renderer function.")
  text = text[:index] + helper + "\n" + text[index:]

function_start = text.find("def _render_group_proof_narrative_latex(")
next_function = text.find("\ndef ", function_start + 1)
if function_start < 0 or next_function < 0:
  raise SystemExit("Could not determine renderer function boundary.")
function_text = text[function_start:next_function]

call_marker = "_render_prop44_suspension_injective_statement_latex("
if call_marker not in function_text:
  statement_marker = "  statement = proof_step.conclusion\n"
  statement_index = function_text.find(statement_marker)
  if statement_index < 0:
    raise SystemExit("Could not find statement assignment.")
  insertion_index = statement_index + len(statement_marker)
  call = """

  prop44_suspension_injective_latex = (
    _render_prop44_suspension_injective_statement_latex(
      statement
    )
  )

  if (
    prop44_suspension_injective_latex
    is not None
  ):
    return prop44_suspension_injective_latex
"""
  function_text = (
    function_text[:insertion_index]
    + call
    + function_text[insertion_index:]
  )
  text = text[:function_start] + function_text + text[next_function:]

backup = PATH.with_name(PATH.name + ".phase143_75p_backup")
if not backup.exists():
  backup.write_text(original, encoding="utf-8")

PATH.write_text(text, encoding="utf-8")
print("Phase 143-75P repair applied.")
print("Backup:", backup)
