from pathlib import Path
import shutil

root=Path.cwd()
pkg=Path(__file__).resolve().parent
sections=pkg/"sections"
out=pkg/"full_files"
out.mkdir(exist_ok=True)

paths={
 "README.md": root/"README.md",
 "design.md": root/"docs"/"design.md",
 "development_log.md": root/"docs"/"development_log.md",
 "roadmap.md": root/"docs"/"roadmap.md",
 "proof_records.md": root/"docs"/"proof_records.md",
}
for name,p in paths.items():
    if not p.exists():
        raise RuntimeError(f"missing required document: {p}")

def append_once(path, marker, section_file):
    text=path.read_text(encoding="utf-8")
    if marker not in text:
        section=(sections/section_file).read_text(encoding="utf-8").strip()
        path.write_text(text.rstrip()+"\n\n"+section+"\n",encoding="utf-8")

append_once(paths["README.md"],"## Phase 144 closure","README_phase144.md")
append_once(paths["design.md"],"# 28. Phase 144 generic Narrative / ownership boundary","design_phase144.md")
append_once(paths["development_log.md"],"# Phase 144 — generic Narrative / ownership-boundary audit closure","development_log_phase144.md")
append_once(paths["proof_records.md"],"# Phase 144 generic Narrative / ownership provenance record","proof_records_phase144.md")

road=paths["roadmap.md"]
text=road.read_text(encoding="utf-8")
marker="# Phase 143 完了後のロードマップ"
newmarker="# Phase 144 完了後のロードマップ"
section=(sections/"roadmap_phase144.md").read_text(encoding="utf-8").strip()
if newmarker not in text:
    if marker not in text:
        raise RuntimeError("roadmap replacement marker not found")
    prefix=text.split(marker,1)[0].rstrip()
    road.write_text(prefix+"\n\n"+section+"\n",encoding="utf-8")

# Correct current-status regression summaries without claiming an unobserved all-green run.
for p in (paths["README.md"], paths["design.md"]):
    text=p.read_text(encoding="utf-8")
    old="""Latest repository-wide regression:

```text
9980 passed in 807.31s (0:13:27)
```"""
    new="""Latest canonical repository-wide Phase 144 run:

```text
10298 collected
10273 passed, 25 failed in 2321.20s (0:38:41)
```

The 25 failures were historical R5-39 through R5-43 snapshot assertions. After
focused historical-test maintenance, the affected regression passed:

```text
66 passed in 1308.82s (0:21:48)
```

The repository-wide suite was not rerun after that maintenance."""
    if old in text:
        text=text.replace(old,new,1)
        p.write_text(text,encoding="utf-8")

# Output complete updated files, as required for documentation changes.
for name,p in paths.items():
    shutil.copy2(p,out/name)

print("Phase 144 documentation closure applied.")
print("Complete updated files written to:", out)
for name in paths:
    print(" -", name)
