from pathlib import Path
import ast

path = Path("toda_proof_narrative_renderer.py")
text = path.read_text(encoding="utf-8")
tree = ast.parse(text)

TARGET_CLASS = "Toda515Sigma8TransportedDecompositionStatement"


def is_target_test(node):
  if not isinstance(node, ast.Call):
    return False

  if not (
    isinstance(node.func, ast.Name)
    and node.func.id == "isinstance"
  ):
    return False

  if len(node.args) != 2:
    return False

  subject, class_node = node.args

  return (
    isinstance(subject, ast.Name)
    and subject.id == "statement"
    and isinstance(class_node, ast.Name)
    and class_node.id == TARGET_CLASS
  )


target_ifs = [
  node
  for node in ast.walk(tree)
  if isinstance(node, ast.If)
  and is_target_test(node.test)
]

if len(target_ifs) != 1:
  raise RuntimeError(
    "Expected exactly one "
    f"{TARGET_CLASS} branch; "
    f"found {len(target_ifs)}."
  )

target = target_ifs[0]

replacement_source = r'''if isinstance(
    statement,
    Toda515Sigma8TransportedDecompositionStatement,
  ):
    transported_group = statement.transported_group

    if not isinstance(
      transported_group,
      DirectSumGroup,
    ):
      raise TypeError(
        "transported_group must be a DirectSumGroup"
      )

    if len(transported_group.summands) != 2:
      raise ValueError(
        "transported_group must have exactly two summands"
      )

    first_summand = transported_group.summands[0]
    second_summand = transported_group.summands[1]

    return (
      _render_phase143_75ao_homotopy_group(
        statement.prop44_isomorphism.map.target_group
      )
      + r" \cong "
      + render_toda_raw_group_structure_latex(
        second_summand
      )
      + r" \oplus "
      + render_toda_raw_group_structure_latex(
        first_summand
      )
    )
'''

lines = text.splitlines(keepends=True)
start = target.lineno - 1
end = target.end_lineno

indent = " " * target.col_offset
replacement_text = "".join(
  indent + line if line.strip() else line
  for line in replacement_source.splitlines(keepends=True)
)

lines[start:end] = [replacement_text]
new_text = "".join(lines)

ast.parse(new_text)
path.write_text(new_text, encoding="utf-8")

print(
  "Phase 143-75AP R9 transported-decomposition "
  "display-contract repair applied."
)
