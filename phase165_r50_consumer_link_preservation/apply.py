
from pathlib import Path
import shutil
import ast

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
BACKUP = Path(__file__).resolve().parent / "backup_before_apply" / TARGET.name
START = "def link_toda_group_proof_narrative_reference_body_consumers("
END = "def suppress_toda_group_proof_narrative_reference_body_restatements("
ANCHOR = """    consumer_index = consumer_indices[
      0
    ]

    legacy_marker_only = ("""
REPLACEMENT = """    consumer_index = consumer_indices[
      0
    ]

    # A reference marker may be moved only onto an unadorned
    # conclusion.  The substring match above can find a conclusion
    # embedded in an independently derived explanation; replacing
    # that paragraph would discard its mathematical justification.
    if lines[consumer_index].strip() != consumer_line.strip():
      continue

    legacy_marker_only = ("""

def main():
    original = TARGET.read_text(encoding="utf-8")
    start = original.index(START)
    end = original.index(END, start)
    function = original[start:end]
    if REPLACEMENT in function:
        print("R50 consumer-link guard already installed")
        return
    if function.count(ANCHOR) != 1:
        raise RuntimeError("unexpected consumer-link function; no change made")
    updated = original[:start] + function.replace(ANCHOR, REPLACEMENT, 1) + original[end:]
    ast.parse(updated, filename=str(TARGET))
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP)
    TARGET.write_text(updated,encoding="utf-8",newline="")
    print("R50 consumer-link guard installed; backup saved")

if __name__ == "__main__":
    main()
