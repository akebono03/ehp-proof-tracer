"""Document-only Phase 164 closure. No tests, no source-code changes."""
from pathlib import Path
import sys, json, shutil, hashlib, datetime, tempfile

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
SECTIONS = json.loads((PACKAGE / "sections.json").read_text(encoding="utf-8"))
OUTPUT = ROOT / "phase164_r10_docs_output"
FILES = tuple(SECTIONS)
MARKER = "Phase 164 — Unified Proof Construction and Rendering" 
OTHER_MARKER = "2026-10-13 — Phase 164"

def main():
    print("Phase 164 document-only closure; NO pytest is executed.")
    missing = [name for name in FILES if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit("Missing existing files (no files changed): " + repr(missing))
    original = {name: (ROOT / name).read_text(encoding="utf-8-sig") for name in FILES}
    if any(MARKER in original[name] if name == "README.md" else OTHER_MARKER in original[name] for name in FILES):
        raise SystemExit("Phase 164 closure markers already present; review manually (no files changed).")
    # Verify all five texts and their required language-specific closure sections before touching files.
    assert "Repository-wide pytest was deliberately NOT run" in SECTIONS["README.md"]
    assert all("pytest" in SECTIONS[name] for name in FILES if name != "README.md")
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = ROOT / ("phase164_r10_docs_backup_" + stamp)
    backup.mkdir(parents=False, exist_ok=False)
    output_files = OUTPUT / "full_documents"
    output_files.mkdir(parents=True, exist_ok=True)
    report=[]
    # Backup every original before any write.
    for name in FILES:
        target = backup / name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(original[name],encoding="utf-8")
    for name in FILES:
        updated = original[name].rstrip("\n") + "\n\n" + SECTIONS[name].strip("\n") + "\n"
        target = ROOT / name
        full_output = output_files / name
        full_output.parent.mkdir(parents=True,exist_ok=True)
        full_output.write_text(updated,encoding="utf-8")
        tmp = target.with_name(target.name + ".phase164_r10_tmp")
        tmp.write_text(updated,encoding="utf-8")
        tmp.replace(target)
        report.append({"file":name,"before_lines":len(original[name].splitlines()),"after_lines":len(updated.splitlines()),"sha256":hashlib.sha256(updated.encode()).hexdigest()})
    summary={"phase":"164 R10 documentation only","state":"DOCUMENTS_UPDATED_WITHOUT_TESTS","files":report,"backup_dir":str(backup),"full_document_dir":str(output_files),"pytest_run":False,"full_pytest_run":False,"scope":"architecture unification closure; neither mathematical certification nor presentation-quality completion"}
    (OUTPUT / "audit.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print("All five FULL Markdown files saved in phase164_r10_docs_output/full_documents/.")

if __name__ == "__main__":
    main()
