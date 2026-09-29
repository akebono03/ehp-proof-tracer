from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
import re
import sys

HISTORICAL = Path(sys.argv[1])
CURRENT = Path(sys.argv[2])
OUT = Path(sys.argv[3])

CLASSIFICATIONS = (
  "PRESERVED",
  "LOST",
  "ADDED",
  "MOVED",
  "DUPLICATED",
  "REWORDED",
  "UNMATCHED",
)


@dataclass(frozen=True)
class Unit:
  index: int
  kind: str
  text: str
  normalized: str
  signature: str


def normalize(text: str) -> str:
  text = text.replace("\r\n", "\n").replace("\r", "\n")
  text = re.sub(r"\\tag\{\d+\}", "", text)
  text = re.sub(r"\s+", "", text)
  text = text.replace("、", ",").replace("。", ".")
  return text


def math_signature(text: str) -> str:
  value = normalize(text)
  value = re.sub(r"\\tag\{\d+\}", "", value)
  value = value.replace(r"\quad\text{は完全である.}", "")
  value = value.replace(r"\text{は完全である.}", "")
  value = value.replace("は完全である.", "")
  return value


def split_units(text: str) -> tuple[Unit, ...]:
  lines = [line.strip() for line in text.splitlines() if line.strip()]
  units = []
  buffer = []
  in_math = False

  def emit(kind: str, parts: list[str]) -> None:
    if not parts:
      return
    value = "\n".join(parts).strip()
    if not value:
      return
    units.append(
      Unit(
        index=len(units),
        kind=kind,
        text=value,
        normalized=normalize(value),
        signature=math_signature(value),
      )
    )

  for line in lines:
    if line == "$$":
      if in_math:
        emit("MATH", buffer)
        buffer = []
        in_math = False
      else:
        emit("PROSE", buffer)
        buffer = []
        in_math = True
      continue

    if in_math:
      buffer.append(line)
      continue

    if line.startswith("$") and line.endswith("$") and len(line) > 1:
      emit("PROSE", buffer)
      buffer = []
      emit("MATH", [line])
      continue

    buffer.append(line)
    if line.endswith(".") or line.endswith("。"):
      emit("PROSE", buffer)
      buffer = []

  emit("MATH" if in_math else "PROSE", buffer)
  return tuple(units)


def similarity(a: Unit, b: Unit) -> float:
  return SequenceMatcher(
    None,
    a.normalized,
    b.normalized,
  ).ratio()


def classify(
  historical: tuple[Unit, ...],
  current: tuple[Unit, ...],
):
  current_by_norm = {}
  current_by_sig = {}
  for unit in current:
    current_by_norm.setdefault(unit.normalized, []).append(unit)
    current_by_sig.setdefault(unit.signature, []).append(unit)

  hist_by_norm = Counter(unit.normalized for unit in historical)
  cur_by_norm = Counter(unit.normalized for unit in current)

  rows = []
  used_current = set()

  for h in historical:
    exact = [
      c for c in current_by_norm.get(h.normalized, ())
      if c.index not in used_current
    ]
    if exact:
      c = exact[0]
      used_current.add(c.index)
      relative_h = h.index / max(1, len(historical) - 1)
      relative_c = c.index / max(1, len(current) - 1)
      status = (
        "MOVED"
        if abs(relative_h - relative_c) > 0.12
        else "PRESERVED"
      )
      rows.append((status, h, c, 1.0))
      continue

    same_sig = [
      c for c in current_by_sig.get(h.signature, ())
      if c.index not in used_current
    ]
    if same_sig and h.signature:
      c = same_sig[0]
      used_current.add(c.index)
      rows.append(("REWORDED", h, c, similarity(h, c)))
      continue

    candidates = [
      (similarity(h, c), c)
      for c in current
      if c.index not in used_current and c.kind == h.kind
    ]
    candidates.sort(key=lambda item: item[0], reverse=True)
    if candidates and candidates[0][0] >= 0.58:
      score, c = candidates[0]
      used_current.add(c.index)
      rows.append(("REWORDED", h, c, score))
      continue

    rows.append(("LOST", h, None, 0.0))

  for c in current:
    if c.index in used_current:
      continue
    if cur_by_norm[c.normalized] > hist_by_norm.get(c.normalized, 0):
      status = "DUPLICATED" if cur_by_norm[c.normalized] > 1 else "ADDED"
    else:
      status = "ADDED"
    rows.append((status, None, c, 0.0))

  return rows


def exact_sequence_inventory(units):
  items = []
  for unit in units:
    text = unit.normalized
    if (
      r"\xrightarrow" in text
      or "は完全である" in unit.text
      or "完全列" in unit.text
    ):
      items.append(unit)
  return items


def reference_reason_inventory(units):
  return [
    unit
    for unit in units
    if re.search(r"\[R\d+\]", unit.text)
  ]


def numbered_formula_inventory(units):
  return [
    unit
    for unit in units
    if re.search(r"\\tag\{\d+\}", unit.text)
  ]


def write_report(historical, current, rows):
  counts = Counter(row[0] for row in rows)
  lines = []
  lines.append("# Phase 146-8 Historical Narrative Full Structural Diff Audit")
  lines.append("")
  lines.append("## Summary")
  lines.append("")
  lines.append(f"- historical units: {len(historical)}")
  lines.append(f"- current units: {len(current)}")
  for status in CLASSIFICATIONS:
    lines.append(f"- {status}: {counts.get(status, 0)}")
  lines.append("")
  lines.append("Classification is structural/heuristic. REWORDED and MOVED candidates must be reviewed before production changes.")
  lines.append("")

  lines.append("## Exactness / sequence inventory")
  lines.append("")
  hseq = exact_sequence_inventory(historical)
  cseq = exact_sequence_inventory(current)
  lines.append(f"- historical sequence-related units: {len(hseq)}")
  lines.append(f"- current sequence-related units: {len(cseq)}")
  lines.append("")

  lines.append("## Reference-reason inventory")
  lines.append("")
  lines.append(f"- historical [R#] units: {len(reference_reason_inventory(historical))}")
  lines.append(f"- current [R#] units: {len(reference_reason_inventory(current))}")
  lines.append("")

  lines.append("## Numbered-formula inventory")
  lines.append("")
  lines.append(f"- historical tagged units: {len(numbered_formula_inventory(historical))}")
  lines.append(f"- current tagged units: {len(numbered_formula_inventory(current))}")
  lines.append("")

  for status in CLASSIFICATIONS:
    selected = [row for row in rows if row[0] == status]
    if not selected:
      continue
    lines.append(f"## {status}")
    lines.append("")
    for _, h, c, score in selected:
      if h is not None:
        lines.append(f"### Historical unit H{h.index + 1} ({h.kind})")
        lines.append("")
        lines.append("```text")
        lines.append(h.text)
        lines.append("```")
      if c is not None:
        lines.append(f"### Current unit C{c.index + 1} ({c.kind})")
        lines.append("")
        lines.append("```text")
        lines.append(c.text)
        lines.append("```")
      if h is not None and c is not None:
        lines.append(f"- similarity: {score:.4f}")
      lines.append("")

  OUT.write_text("\n".join(lines), encoding="utf-8")


def main():
  historical_text = HISTORICAL.read_text(encoding="utf-8")
  current_text = CURRENT.read_text(encoding="utf-8")

  historical = split_units(historical_text)
  current = split_units(current_text)
  rows = classify(historical, current)
  write_report(historical, current, rows)

  counts = Counter(row[0] for row in rows)
  print("=" * 78)
  print("Phase 146-8 Historical Narrative Full Structural Diff Audit")
  print("=" * 78)
  print(f"historical units: {len(historical)}")
  print(f"current units: {len(current)}")
  print()
  for status in CLASSIFICATIONS:
    print(f"{status:10s}: {counts.get(status, 0)}")
  print()
  print(
    "historical sequence-related units:",
    len(exact_sequence_inventory(historical)),
  )
  print(
    "current sequence-related units:",
    len(exact_sequence_inventory(current)),
  )
  print(
    "historical [R#] units:",
    len(reference_reason_inventory(historical)),
  )
  print(
    "current [R#] units:",
    len(reference_reason_inventory(current)),
  )
  print(
    "historical tagged units:",
    len(numbered_formula_inventory(historical)),
  )
  print(
    "current tagged units:",
    len(numbered_formula_inventory(current)),
  )
  print()
  print("Report:", OUT)
  print(
    "NOTE: REWORDED/MOVED are candidates for human review; "
    "no production change is made."
  )


if __name__ == "__main__":
  main()
