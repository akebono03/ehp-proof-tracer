from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_partial_proof.py"
OLD = """def render_partial_proof_markdown(result: PartialProofResult) -> str:
    \"\"\"Use the R2 shared model and the canonical Narrative dispatch for any state.\"\"\"
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    from phase165_renderer_narrative_model import build_narrative_proof_model
    from toda_group_proof_narrative_renderer import render_narrative_proof_model

    return render_narrative_proof_model(build_narrative_proof_model(result))
"""
NEW = """def render_partial_proof_markdown(result: PartialProofResult) -> str:
    \"\"\"Route complete results to the restored Narrative; incomplete results to partial.\"\"\"
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is ProofSearchStatus.COMPLETE:
        from phase165_r56_presentation_adapter import render_completed_shared_narrative
        return render_completed_shared_narrative(result)
    from toda_group_proof_narrative_renderer import render_toda_partial_proof_narrative_markdown
    return render_toda_partial_proof_narrative_markdown(result)
"""

def install():
    source=TARGET.read_text(encoding="utf-8")
    if source.count(NEW)==1:
        print("R57-R21 completed entry route already removed")
        return
    if source.count(OLD)!=1:
        raise RuntimeError("Unexpected entrypoint source: refusing destructive edit")
    updated=source.replace(OLD,NEW,1)
    ast.parse(updated)
    backup=TARGET.with_suffix(".before_remove_r57_r21_route.py")
    if backup.exists():
        raise RuntimeError("Backup path exists: refusing overwrite")
    backup.write_text(source,encoding="utf-8")
    TARGET.write_text(updated,encoding="utf-8")
    print("Removed completed Narrative model detour from public entry.")
    print("Backup:",backup)

if __name__=="__main__":
    install()
