from pathlib import Path
import shutil

ROOT = Path.cwd()
PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "updated_full_documents"

DESIGN_SECTION = (PACKAGE / "sections" / "design_phase146.md").read_text(encoding="utf-8").strip()
DEV_SECTION = (PACKAGE / "sections" / "development_log_phase146.md").read_text(encoding="utf-8").strip()
ROADMAP_REPLACEMENT = (PACKAGE / "sections" / "roadmap_phase146.md").read_text(encoding="utf-8").strip()
PROOF_SECTION = (PACKAGE / "sections" / "proof_records_phase146.md").read_text(encoding="utf-8").strip()

FILES = {
    "design": ROOT / "docs" / "design.md",
    "development_log": ROOT / "docs" / "development_log.md",
    "roadmap": ROOT / "docs" / "roadmap.md",
    "proof_records": ROOT / "docs" / "proof_records.md",
}

def read(path):
    return path.read_text(encoding="utf-8")

def write(path, text):
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")

def append_once(text, marker, section):
    if marker in text:
        return text
    return text.rstrip() + "\n\n---\n\n" + section + "\n"

def update_roadmap(text):
    completed_marker = "## Phase 146 — 完了: historical Narrative difference audit"
    if completed_marker in text:
        return text
    start_marker = "## Phase 146 以降 — 1 Phase = 1 concrete issue"
    start = text.find(start_marker)
    if start == -1:
        raise RuntimeError("roadmap.md: Phase 146 planned section boundary not found")
    return text[:start].rstrip() + "\n\n" + ROADMAP_REPLACEMENT + "\n"

def main():
    missing = [str(path) for path in FILES.values() if not path.exists()]
    if missing:
        raise RuntimeError("Missing canonical docs: " + ", ".join(missing))

    design = append_once(
        read(FILES["design"]),
        "# 30. Phase 146 historical Narrative difference audit / root-cause boundary",
        DESIGN_SECTION,
    )
    dev = append_once(
        read(FILES["development_log"]),
        "# Phase 146 — historical Narrative difference audit / root-cause classification",
        DEV_SECTION,
    )
    roadmap = update_roadmap(read(FILES["roadmap"]))
    proof = append_once(
        read(FILES["proof_records"]),
        "# Phase 146 historical Narrative comparison / provenance record",
        PROOF_SECTION,
    )

    write(FILES["design"], design)
    write(FILES["development_log"], dev)
    write(FILES["roadmap"], roadmap)
    write(FILES["proof_records"], proof)

    OUT.mkdir(parents=True, exist_ok=True)
    for path in FILES.values():
        shutil.copy2(path, OUT / path.name)

    print("Phase 146 documentation closure applied.")
    print("Changed canonical files:")
    for path in FILES.values():
        print(" -", path.relative_to(ROOT))
    print("README.md: unchanged")
    print("Production code changes: none")
    print("Test code changes: none")
    print("Full updated documents:")
    print(" -", OUT)

if __name__ == "__main__":
    main()
