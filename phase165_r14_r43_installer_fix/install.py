"""Install R43 shared-renderer hook using AST guarded body replacement."""
from pathlib import Path
import ast
import shutil

ROOT=Path(__file__).resolve().parent.parent
NAME="toda_group_proof_narrative_renderer.py"
TARGET=ROOT/NAME
MARKER="phase165_r43_shared_narrative_enrichment"

def main():
    target_text=TARGET.read_text(encoding="utf8")
    if MARKER in target_text:
        print("R43 shared narrative hook already installed")
    else:
        tree=ast.parse(target_text)
        definitions=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))
                     and n.name=="render_toda_group_proof_narrative_markdown"]
        if not definitions:
            raise RuntimeError("Existing common narrative renderer function not found")
        node=definitions[-1]
        if not any(isinstance(n,ast.Return) for n in ast.walk(node)):
            raise RuntimeError("Unexpected renderer body")
        lines=target_text.splitlines(keepends=True)
        # Rewrite only the final renderer function, preserving earlier routes.
        prefix="".join(lines[:node.lineno-1])
        replacement="""def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  stable_transport_narrative = (
    _phase160_r7_render_stable_finite_cyclic_transport_narrative(
      presentation
    )
  )
  if stable_transport_narrative is not None:
    return stable_transport_narrative

  rendered = (
    _phase160_r7_previous_public_narrative_renderer(
      presentation
    )
  )
  from phase164_r9_narrative_contract import normalize_public_narrative_contract
  rendered = normalize_public_narrative_contract(
    suppress_toda_group_proof_narrative_dangling_connectors(
      rendered
    )
  )
  # phase165_r43_shared_narrative_enrichment
  from phase165_r14_r43_reference_reason import enrich_common_narrative
  return enrich_common_narrative(presentation, rendered)
"""
        # Later functions and aliases are legitimate. Keep them unchanged.
        suffix="".join(lines[node.end_lineno:])
        output=prefix+replacement+suffix
        ast.parse(output)
        backup=TARGET.with_name("toda_group_proof_narrative_renderer.phase165_r43_backup.py")
        if not backup.exists():
            shutil.copy2(TARGET,backup)
        TARGET.write_text(output,encoding="utf8")
        print("Updated common Narrative renderer; backup:",backup.name)
    source=Path(__file__).with_name("phase165_r14_r43_reference_reason.py")
    destination=ROOT/source.name
    shutil.copy2(source,destination)
    print("Installed common reference and inference explanation module")

if __name__=="__main__":
    main()
