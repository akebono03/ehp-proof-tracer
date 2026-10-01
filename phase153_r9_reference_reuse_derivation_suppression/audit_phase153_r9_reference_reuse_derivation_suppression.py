from pathlib import Path
import sys

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(0, str(REPO_ROOT))

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

TARGETS = (
  ("pi4_2", 2, 2),
  ("pi5_2", 2, 3),
  ("pi6_2", 2, 4),
  ("pi7_2", 2, 5),
  ("pi8_2", 2, 6),
  ("pi9_2", 2, 7),
  ("pi10_6", 6, 4),
  ("pi12_7", 7, 5),
)

def render_body(n, k):
  report = build_standard_toda_report(n=n, k=k)
  result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(result, max_depth=2)
  presentation = build_toda_group_proof_presentation(replay)
  rendered = render_toda_group_proof_narrative_markdown(presentation)
  marker = "## 証明\n\n"
  if marker not in rendered:
    return rendered
  return rendered.split(marker, 1)[1]

def main():
  failures = []
  print("=" * 72)
  print("Phase 153-R9 Reference reuse / derivation suppression audit")
  print("=" * 72)

  for label, n, k in TARGETS:
    body = render_body(n, k)
    nonblank = tuple(line for line in body.splitlines() if line.strip())
    print(f"{label}: chars={len(body)} nonblank-lines={len(nonblank)}")

    if not body.strip():
      failures.append((label, "empty proof body"))

    if label == "pi6_2":
      for fragment in (
        "[R2]を用いる。",
        "[R3]を用いる。",
        r"\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}",
      ):
        if fragment not in body:
          failures.append((label, "missing", fragment))

      for fragment in (
        r"\pi_{i - 1}^{1} = 0",
        "[R4]を用いる。",
        r"γ \mapsto \eta_{2}γ",
        "Toda (5.2) の η₂ 合成同型を得る。",
      ):
        if fragment in body:
          failures.append((label, "unexpected", fragment))

  print()
  if failures:
    print("FAIL")
    for failure in failures:
      print("  ", failure)
    raise SystemExit(1)

  print("PASS")
  print(
    "Selected Reference statements with ancestry are reused directly "
    "instead of re-expanding their derivations."
  )

if __name__ == "__main__":
  main()
