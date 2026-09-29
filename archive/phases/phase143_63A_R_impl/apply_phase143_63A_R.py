from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent


def replace_once(path: Path, old: str, new: str) -> None:
  text = path.read_text(encoding="utf-8")
  if old not in text:
    raise RuntimeError("expected anchor not found in " + str(path))
  path.write_text(text.replace(old, new, 1), encoding="utf-8")
  print("updated " + str(path))


generic_renderer = ROOT / "toda_group_proof_generic_narrative_renderer.py"
start = "  if isinstance(\n    statement,\n    TodaProp42ExactnessStatement,\n  ):\n"
end = "  if isinstance(\n    statement,\n    TodaNuFamilyDefinitionStatement,\n  ):\n"
text = generic_renderer.read_text(encoding="utf-8")
start_index = text.find(start)
if start_index < 0:
  raise RuntimeError("Phase 143-63A exactness prose block not found")
end_index = text.find(end, start_index)
if end_index < 0:
  raise RuntimeError("TodaNuFamilyDefinitionStatement anchor not found")
generic_renderer.write_text(text[:start_index] + text[end_index:], encoding="utf-8")
print("updated " + str(generic_renderer))


body_renderer = ROOT / "toda_group_proof_narrative_argument_body_renderer.py"
old_import = "from toda_group_proof_presentation import (\n  TodaGroupProofPresentation,\n)\n"
new_import = old_import + "from toda_rules import (\n  TodaProp42ExactnessStatement,\n)\n"
replace_once(body_renderer, old_import, new_import)

old_render = """  for premise_step in relocated_direct_premises:
    relocated_lines.append(
      _render_generic_narrative_step(
        premise_step
      )
    )
    relocated_lines.append(
      \"\"
    )
"""
new_render = """  for premise_step in relocated_direct_premises:
    rendered_premise = (
      _render_generic_narrative_step(
        premise_step
      )
    )

    if isinstance(
      premise_step.conclusion,
      TodaProp42ExactnessStatement,
    ):
      english_suffix = (
        r\" \\text{ is exact}$\"
      )

      if rendered_premise.endswith(
        english_suffix
      ):
        rendered_premise = (
          rendered_premise[
            :-len(
              english_suffix
            )
          ]
          + \"$ は完全である.\"
        )

    relocated_lines.append(
      rendered_premise
    )
    relocated_lines.append(
      \"\"
    )
"""
replace_once(body_renderer, old_render, new_render)


for test_name in (
  "test_phase143_63a_residual_fallback_provenance.py",
  "test_phase143_63a_r_exactness_repair.py",
):
  source = PACKAGE_ROOT / "tests" / test_name
  target = ROOT / "tests" / test_name
  shutil.copyfile(source, target)
  print("updated " + str(target))
