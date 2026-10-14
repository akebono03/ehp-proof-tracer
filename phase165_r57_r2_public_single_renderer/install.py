"""Install only the Phase 165 R57-R2 single-public-renderer entry change."""
import ast
from pathlib import Path
import shutil

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PUBLIC = ROOT / "toda_group_proof_narrative_renderer.py"
WRAPPER = ROOT / "phase165_r52_partial_proof.py"
PARTIAL = ROOT / "phase165_r57_r2_partial_narrative.py"

NEW_PUBLIC_FUNCTION = '''def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  """The single public Narrative entry for complete and incomplete searches."""
  from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
  if isinstance(presentation, PartialProofResult):
    if presentation.status is ProofSearchStatus.COMPLETE:
      from phase165_r56_presentation_adapter import render_completed_shared_narrative
      return render_completed_shared_narrative(presentation)
    from phase165_r57_r2_partial_narrative import render_incomplete_public_narrative
    return render_incomplete_public_narrative(presentation)

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
  return rendered
'''

NEW_WRAPPER_FUNCTION = '''def render_partial_proof_markdown(result: PartialProofResult) -> str:
    """Compatibility API: use the one public Toda narrative renderer."""
    from toda_group_proof_narrative_renderer import (
        render_toda_group_proof_narrative_markdown,
    )
    return render_toda_group_proof_narrative_markdown(result)
'''

def replace_last_function(source, name, new_code):
    module = ast.parse(source)
    matches = [node for node in module.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if not matches:
        raise RuntimeError("Missing required function: " + name)
    node = matches[-1]
    lines = source.splitlines(keepends=True)
    return "".join(lines[:node.lineno-1]) + new_code + "".join(lines[node.end_lineno:])

def install():
    for path in (PUBLIC, WRAPPER):
        if not path.exists():
            raise FileNotFoundError(path)
    public_source = PUBLIC.read_text(encoding="utf-8")
    wrapper_source = WRAPPER.read_text(encoding="utf-8")
    if 'from phase165_r57_r2_partial_narrative import render_incomplete_public_narrative' in public_source:
        if 'from toda_group_proof_narrative_renderer import (' not in wrapper_source:
            raise RuntimeError("Partial installation detected; wrapper not updated")
        print("R57-R2 public Narrative entry already installed")
        return
    public_updated = replace_last_function(public_source, "render_toda_group_proof_narrative_markdown", NEW_PUBLIC_FUNCTION)
    wrapper_updated = replace_last_function(wrapper_source, "render_partial_proof_markdown", NEW_WRAPPER_FUNCTION)
    ast.parse(public_updated)
    ast.parse(wrapper_updated)
    shutil.copy2(PUBLIC, ROOT / "toda_group_proof_narrative_renderer.py.phase165_r57_r2_backup")
    shutil.copy2(WRAPPER, ROOT / "phase165_r52_partial_proof.py.phase165_r57_r2_backup")
    if PARTIAL.exists() and PARTIAL.read_bytes() != (PACKAGE / PARTIAL.name).read_bytes():
        raise RuntimeError("Existing R57-R2 partial adapter differs; refusing overwrite")
    shutil.copy2(PACKAGE / PARTIAL.name, PARTIAL)
    PUBLIC.write_text(public_updated, encoding="utf-8")
    WRAPPER.write_text(wrapper_updated, encoding="utf-8")
    print("R57-R2 installed: complete and incomplete search results use the public Narrative entry")
    print("No legacy renderer functions deleted in R57-R2; complete public presentation unchanged")

if __name__ == "__main__":
    install()
