from collections import Counter, defaultdict
import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


PATTERNS = (
  ("python_backtick_identifier", re.compile(r"`[A-Za-z_][A-Za-z0-9_]*`")),
  ("python_repr", re.compile(r"(?:Scalar|Toda|Homotopy|Proof|Relation)[A-Za-z0-9_]*\(")),
  ("raw_none_true_false", re.compile(r"\b(?:None|True|False)\b")),
  ("malformed_scalar_plus_minus", re.compile(r"\+\s*-1(?:\\,|\s)")),
  ("malformed_double_operator", re.compile(r"(?:\+\s*\+|-\s*-|=\s*=)")),
  ("internal_snake_case", re.compile(r"\b[A-Za-z]+_[A-Za-z0-9_]+\b")),
  ("memory_address", re.compile(r"0x[0-9A-Fa-f]+")),
)


def main():
  findings = defaultdict(list)
  scanned_groups = 0
  rendered_groups = 0

  for k in range(8):
    for n in range(2, 16):
      scanned_groups += 1
      try:
        report = build_standard_toda_report(
          n=n,
          k=k,
        )
        group_result = (
          report.candidates[
            0
          ].source_candidate.group_result
        )
        replay = build_toda_group_result_proof_replay(
          group_result,
          max_depth=7,
        )
        presentation = build_toda_group_proof_presentation(
          replay,
        )
        narrative = render_toda_group_proof_narrative_markdown(
          presentation,
        )
      except Exception as exc:
        findings["render_error"].append(
          (n, k, type(exc).__name__, str(exc))
        )
        continue

      rendered_groups += 1

      for name, pattern in PATTERNS:
        for match in pattern.finditer(narrative):
          start = max(0, match.start() - 80)
          end = min(len(narrative), match.end() + 80)
          context = narrative[start:end].replace("\n", " ")
          findings[name].append(
            (n, k, match.group(0), context)
          )

  print("=" * 78)
  print("Phase 143-75 machine-like Narrative expression audit")
  print("range: n=2..15, k=0..7, depth=7")
  print(f"scanned groups: {scanned_groups}")
  print(f"rendered groups: {rendered_groups}")
  print("=" * 78)

  total = 0
  for name, _ in PATTERNS:
    items = findings.get(name, [])
    total += len(items)
    print()
    print(name)
    print(f"  occurrences: {len(items)}")
    counts = Counter(item[2] for item in items)
    for token, count in counts.most_common(12):
      print(f"  - {token!r}: {count}")
    for n, k, token, context in items[:8]:
      print(f"    pi_{n+k}^{n}, k={k}: {context}")

  errors = findings.get("render_error", [])
  print()
  print(f"render errors: {len(errors)}")
  for item in errors[:20]:
    print("  -", item)

  print()
  print("=" * 78)
  if total == 0 and not errors:
    print("PASS: no audited machine-like expression pattern was found.")
  else:
    print(
      "AUDIT FINDING: machine-like or suspicious Narrative expressions remain. "
      "Review the categories above and choose the smallest generic rendering target "
      "for the next subphase."
    )


if __name__ == "__main__":
  main()
