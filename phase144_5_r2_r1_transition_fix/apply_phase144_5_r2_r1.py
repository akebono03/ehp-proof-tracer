from pathlib import Path

repo=Path.cwd()
p=repo/"toda_group_proof_narrative_equation_numbering.py"
text=r"""from proof import ProofStep
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_narrative_blocks import TodaGroupProofNarrativeBlock
from toda_group_proof_narrative_step_transitions import extract_toda_group_proof_narrative_step_transitions
from toda_group_proof_presentation import TodaGroupProofPresentation


def toda_group_proof_narrative_equation_reference(equation_number: int) -> str:
  if not isinstance(equation_number, int) or isinstance(equation_number, bool) or equation_number <= 0:
    raise ValueError("equation_number must be a positive integer")
  return "(" + str(equation_number) + ")"


def _numbered_step_line(proof_step: ProofStep, equation_number: int) -> str:
  rendered = _render_generic_narrative_step(proof_step)
  closing = rendered.rfind("$")
  if not rendered.startswith("$") or closing <= 0:
    return rendered
  return rendered[:closing] + r"\\tag{" + str(equation_number) + "}" + rendered[closing:]


def number_toda_group_proof_narrative_equations(
  markdown: str,
  presentation: TodaGroupProofPresentation,
  blocks: tuple[TodaGroupProofNarrativeBlock, ...],
) -> str:
  if not isinstance(markdown, str):
    raise TypeError("markdown must be a string")
  transitions = extract_toda_group_proof_narrative_step_transitions(presentation, blocks)
  sources_by_target = {}
  for transition in transitions:
    key=id(transition.target_step)
    current=sources_by_target.get(key, ())
    if not any(step is transition.source_step for step in current):
      sources_by_target[key]=(*current, transition.source_step)

  ordered=[]
  seen=set()
  for block in blocks:
    for target in block.steps:
      sources=sources_by_target.get(id(target), ())
      for step in sources:
        if id(step) not in seen:
          ordered.append(step); seen.add(id(step))
      if sources and id(target) not in seen:
        ordered.append(target); seen.add(id(target))

  numbers={id(step): i for i,step in enumerate(ordered,1)}
  plain={id(step): _render_generic_narrative_step(step) for step in ordered}
  tagged={id(step): _numbered_step_line(step,numbers[id(step)]) for step in ordered}
  lines=markdown.splitlines()

  for i,line in enumerate(lines):
    for sid,value in plain.items():
      if line == value:
        lines[i]=tagged[sid]
        break

  for target_id,sources in sources_by_target.items():
    target_line=tagged.get(target_id)
    if target_line is None:
      continue
    try:
      target_index=lines.index(target_line)
    except ValueError:
      continue
    connector=None
    for i in range(target_index-1,-1,-1):
      if lines[i] == "これらより、":
        connector=i
        break
      if lines[i] and not lines[i].startswith("$"):
        break
    if connector is None:
      continue
    refs=[toda_group_proof_narrative_equation_reference(numbers[id(s)]) for s in sources if id(s) in numbers]
    if not refs:
      continue
    reftext=refs[0] if len(refs)==1 else ", ".join(refs[:-1])+" と "+refs[-1]
    lines[connector]=reftext+" より、"

  return "\\n".join(lines)
"""
p.write_text(text,encoding="utf-8")

mp=repo/"toda_group_proof_narrative_argument_multi_renderer.py"
m=mp.read_text(encoding="utf-8-sig")
old="""number_toda_group_proof_narrative_equations(
      rendered
    )"""
new="""number_toda_group_proof_narrative_equations(
      rendered,
      presentation,
      blocks,
    )"""
if new not in m:
  if old not in m:
    raise RuntimeError("numbering call not found")
  m=m.replace(old,new,1)
mp.write_text(m,encoding="utf-8")
print("Phase 144-5-R2-R1 applied.")
