"""R42: add source provenance and generic prose; refuse unknown layouts."""
from __future__ import annotations
from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent

def patch(path: Path, replacement):
    old=path.read_text(encoding="utf-8")
    new=replacement(old)
    if new==old:
        print("Already installed:",path.name)
        return
    ast.parse(new,filename=str(path))
    backup=path.with_name(path.stem+".phase165_r42_backup.py")
    if not backup.exists():shutil.copy2(path,backup)
    path.write_text(new,encoding="utf-8")
    print("Updated:",path.name,"backup:",backup.name)

def patch_registry(s):
    if 'phase165_r42_source_inference' in s:return s
    expected='from pathlib import Path\n'
    if s.count(expected)!=1:raise RuntimeError("Unexpected R38 imports")
    s=s.replace(expected,expected+'from dataclasses import replace\nfrom proof import InferenceRule, LiteratureReference\n',1)
    old='        links.append(ProofStepLink(assertion_id, step=matches[0]))'
    if s.count(old)!=1:raise RuntimeError("Unexpected R38 ProofStepLink layout")
    new="""        # phase165_r42_source_inference: keep the existing GIVEN statement,
        # and attach its source locator to the ProofStep used by the renderer.
        # Foundational references retain their separate provenance mechanism.
        source_step = matches[0]
        if locator.startswith("Proposition ") or locator.startswith("("):
            source_step = replace(
                source_step,
                inference_rule=InferenceRule(
                    name="Toda " + locator,
                    literature_reference=LiteratureReference(
                        label="Toda " + locator, locator=locator,
                    ),
                ),
            )
        links.append(ProofStepLink(assertion_id, step=source_step))"""
    return s.replace(old,new,1)

def patch_generic(s):
    if 'phase165_r42_generic_typed_prose' in s:return s
    anchor='def _render_generic_narrative_statement_prose(\n  statement,\n) -> str | None:\n'
    if s.count(anchor)!=1:raise RuntimeError("Unexpected shared renderer prose function")
    addition="""  # phase165_r42_generic_typed_prose: these are shared typed map and
  # generator-image statements; never use target-specific prose.
  kind = type(statement).__name__
  if kind == "GeneratorImage":
    map_name = _generic_group_map_name(statement.map)
    if map_name is not None:
      return (
        "$" + map_name + "("
        + render_toda_expression_latex(statement.source_generator)
        + ") = "
        + render_toda_expression_latex(statement.target_generator)
        + "$."
      )
  if kind in ("MapIsomorphism", "MapInjective", "MapSurjective"):
    map_latex = _render_generic_narrative_group_map_latex(statement.map)
    if map_latex is not None:
      meaning = {
        "MapIsomorphism": "同型写像",
        "MapInjective": "単射",
        "MapSurjective": "全射",
      }[kind]
      return "$" + map_latex + "$ は" + meaning + "である."

"""
    return s.replace(anchor,anchor+addition,1)


def main():
    patch(ROOT/'phase165_r14_r38_direct_registry.py',patch_registry)
    patch(ROOT/'toda_group_proof_generic_narrative_renderer.py',patch_generic)

if __name__=='__main__':main()
