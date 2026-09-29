from pathlib import Path
import runpy

candidates = [
  Path("phase143_75ap") / "audit_phase143_75ap.py",
  Path("phase143_75ap_r8") / "audit_phase143_75ap.py",
  Path("phase143_75ap_r8") / "audit_phase143_75ap_r8.py",
]

existing = [p for p in candidates if p.is_file()]

if not existing:
  matches = sorted(
    p for p in Path(".").glob("phase143_75ap*/**/*.py")
    if "audit" in p.name.lower()
    and "completion" in p.name.lower()
  )
  existing = matches

if not existing:
  raise RuntimeError(
    "Existing Phase 143-75AP completion audit script not found. "
    "No project files changed."
  )

script = existing[0]
print(f"Using existing completion audit: {script}")
print("=" * 78)
runpy.run_path(str(script), run_name="__main__")
