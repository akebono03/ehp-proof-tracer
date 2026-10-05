from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

from web_group_proof import build_standard_web_group_proof_view


CONNECTOR_RE = re.compile(
  r"^\((?P<first>\d+)\)(?:\s+と\s+\((?P<second>\d+)\))?\s+より,?\s*$"
)
TAG_RE = re.compile(r"\\tag\{(?P<number>\d+)\}")

FINDINGS = (
  (3, 4, "(1) と (2) より,"),
  (5, 5, "(1) より,"),
  (5, 6, "(1) より,"),
  (6, 6, "(1) より,"),
  (6, 6, "(2) より,"),
)


@dataclass(frozen=True)
class FindingClassification:
  n: int
  k: int
  connector: str
  connector_line: int
  referenced_tags: tuple[int, ...]
  source_lines: tuple[int | None, ...]
  next_line: int | None
  next_text: str
  next_has_math: bool
  next_tags: tuple[int, ...]
  classification: str
  production_bug: str
  reason: str


def _line_text(line) -> str:
  if line.segments:
    return "".join(segment.value for segment in line.segments)

  return (
    line.prefix
    + ("" if line.statement_latex is None else line.statement_latex)
    + line.suffix
  )


def _proof_lines(n: int, k: int) -> list[tuple[object, str]]:
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=2,
    mode="narrative",
  )
  result = []
  in_proof = False

  for line in view.rendered_lines:
    if line.kind == "heading" and line.prefix == "証明":
      in_proof = True
      continue

    if not in_proof:
      continue

    text = _line_text(line).strip()
    if not text:
      continue

    result.append((line, text))

  return result


def _connector_numbers(connector: str) -> tuple[int, ...]:
  match = CONNECTOR_RE.match(connector.strip())
  if match is None:
    raise ValueError(f"unsupported connector: {connector}")

  numbers = [int(match.group("first"))]
  if match.group("second") is not None:
    numbers.append(int(match.group("second")))
  return tuple(numbers)


def _tag_numbers(text: str) -> tuple[int, ...]:
  return tuple(int(match.group("number")) for match in TAG_RE.finditer(text))


def classify_public_connector(
  *,
  n: int,
  k: int,
  connector: str,
  lines: list[tuple[object, str]],
) -> FindingClassification:
  normalized = connector.strip()
  connector_indices = [
    index
    for index, (_, text) in enumerate(lines)
    if text.strip() == normalized
  ]

  if not connector_indices:
    return FindingClassification(
      n=n,
      k=k,
      connector=connector,
      connector_line=-1,
      referenced_tags=_connector_numbers(connector),
      source_lines=(),
      next_line=None,
      next_text="",
      next_has_math=False,
      next_tags=(),
      classification="TARGET_VISIBILITY_SUPPRESSION",
      production_bug="UNDECIDED",
      reason=(
        "The expected public connector is absent. Public evidence alone cannot prove "
        "whether suppression is correct, so pipeline inspection is required before "
        "changing production code."
      ),
    )

  connector_index = connector_indices[0]
  referenced_tags = _connector_numbers(connector)
  source_lines_list = []

  for number in referenced_tags:
    source_index = next(
      (
        index
        for index, (_, text) in enumerate(lines)
        if number in _tag_numbers(text)
      ),
      None,
    )
    source_lines_list.append(None if source_index is None else source_index + 1)

  source_lines = tuple(source_lines_list)

  if any(
    line_number is None or line_number >= connector_index + 1
    for line_number in source_lines
  ):
    next_index = connector_index + 1 if connector_index + 1 < len(lines) else None
    next_line_obj = None if next_index is None else lines[next_index][0]
    next_text = "" if next_index is None else lines[next_index][1]
    return FindingClassification(
      n=n,
      k=k,
      connector=connector,
      connector_line=connector_index + 1,
      referenced_tags=referenced_tags,
      source_lines=source_lines,
      next_line=None if next_index is None else next_index + 1,
      next_text=next_text,
      next_has_math=(
        False
        if next_line_obj is None
        else bool(next_line_obj.statement_latex)
        or any(segment.kind in ("inline_math", "display_math") for segment in next_line_obj.segments)
      ),
      next_tags=_tag_numbers(next_text),
      classification="REAL_ORDERING_DEFECT",
      production_bug="YES",
      reason="At least one numbered source is missing or does not appear before the connector.",
    )

  next_index = connector_index + 1 if connector_index + 1 < len(lines) else None
  if next_index is None:
    return FindingClassification(
      n=n,
      k=k,
      connector=connector,
      connector_line=connector_index + 1,
      referenced_tags=referenced_tags,
      source_lines=source_lines,
      next_line=None,
      next_text="",
      next_has_math=False,
      next_tags=(),
      classification="TARGET_VISIBILITY_SUPPRESSION",
      production_bug="UNDECIDED",
      reason=(
        "The connector is the last visible proof line, so no public target follows it. "
        "Inspect the rendering pipeline before treating this as a production defect."
      ),
    )

  next_line_obj, next_text = lines[next_index]
  next_tags = _tag_numbers(next_text)
  next_has_math = bool(next_line_obj.statement_latex) or any(
    segment.kind in ("inline_math", "display_math")
    for segment in next_line_obj.segments
  )

  if next_tags:
    classification = "AUDIT_HARNESS_FALSE_POSITIVE"
    production_bug = "NO"
    reason = (
      "All referenced sources are earlier and the immediately following public target "
      "is tagged. The R5-5c finding is therefore a harness false positive."
    )
  elif next_has_math:
    classification = "CONNECTOR_TARGET_NOT_TAGGED"
    production_bug = "NO"
    reason = (
      "All referenced sources are earlier and a mathematical target immediately follows, "
      "but that target is intentionally or currently untagged. Tag absence alone is not an "
      "ordering defect under the public numbering rule."
    )
  else:
    classification = "TARGET_VISIBILITY_SUPPRESSION"
    production_bug = "UNDECIDED"
    reason = (
      "All numbered sources are earlier, but the next visible line is not a mathematical "
      "target. This is a suppression candidate and requires pipeline inspection before any "
      "production change."
    )

  return FindingClassification(
    n=n,
    k=k,
    connector=connector,
    connector_line=connector_index + 1,
    referenced_tags=referenced_tags,
    source_lines=source_lines,
    next_line=next_index + 1,
    next_text=next_text,
    next_has_math=next_has_math,
    next_tags=next_tags,
    classification=classification,
    production_bug=production_bug,
    reason=reason,
  )


def main() -> int:
  output_dir = Path(__file__).resolve().parent / "audit_output"
  output_dir.mkdir(parents=True, exist_ok=True)

  rows = []
  contexts = []
  exceptions = []

  for n, k, connector in FINDINGS:
    try:
      lines = _proof_lines(n, k)
      result = classify_public_connector(
        n=n,
        k=k,
        connector=connector,
        lines=lines,
      )
      rows.append(result)

      contexts.append("=" * 88)
      contexts.append(f"pi_{n + k}^{n}  connector={connector}")
      contexts.append(
        f"classification={result.classification} production_bug={result.production_bug}"
      )
      contexts.append(f"reason={result.reason}")
      contexts.append("-" * 88)

      connector_zero_index = result.connector_line - 1
      if connector_zero_index >= 0:
        start = max(0, connector_zero_index - 4)
        end = min(len(lines), connector_zero_index + 5)
      else:
        start = 0
        end = min(len(lines), 12)

      for index in range(start, end):
        marker = "=>" if index == connector_zero_index else "  "
        contexts.append(f"{marker} {index + 1:03d}: {lines[index][1]}")
      contexts.append("")
    except Exception as exc:
      exceptions.append((n, k, connector, type(exc).__name__, str(exc)))

  csv_path = output_dir / "classification.csv"
  with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(
      (
        "group",
        "n",
        "k",
        "connector",
        "connector_line",
        "referenced_tags",
        "source_lines",
        "next_line",
        "next_text",
        "next_has_math",
        "next_tags",
        "classification",
        "production_bug",
        "reason",
      )
    )
    for row in rows:
      writer.writerow(
        (
          f"pi_{row.n + row.k}^{row.n}",
          row.n,
          row.k,
          row.connector,
          row.connector_line,
          ";".join(str(value) for value in row.referenced_tags),
          ";".join("" if value is None else str(value) for value in row.source_lines),
          "" if row.next_line is None else row.next_line,
          row.next_text,
          row.next_has_math,
          ";".join(str(value) for value in row.next_tags),
          row.classification,
          row.production_bug,
          row.reason,
        )
      )

  (output_dir / "finding_context.txt").write_text(
    "\n".join(contexts) + "\n",
    encoding="utf-8",
    newline="\n",
  )

  with (output_dir / "exceptions.csv").open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.writer(handle)
    writer.writerow(("n", "k", "connector", "exception_type", "message"))
    writer.writerows(exceptions)

  counts = {}
  for row in rows:
    counts[row.classification] = counts.get(row.classification, 0) + 1

  summary_lines = [
    "Phase 158-R5-5c-1 — finding classification",
    "",
    "Scope:",
    "  classify only the 5 equation-chain findings from R5-5c",
    "  Web Narrative depth=2",
    "  production code changes: none",
    "  existing test changes: none",
    "",
    f"classified findings: {len(rows)}",
    f"exceptions: {len(exceptions)}",
    "",
    "Classification counts:",
  ]
  for name in (
    "REAL_ORDERING_DEFECT",
    "TARGET_VISIBILITY_SUPPRESSION",
    "CONNECTOR_TARGET_NOT_TAGGED",
    "AUDIT_HARNESS_FALSE_POSITIVE",
  ):
    summary_lines.append(f"  {name}: {counts.get(name, 0)}")

  confirmed_bugs = sum(1 for row in rows if row.production_bug == "YES")
  undecided = sum(1 for row in rows if row.production_bug == "UNDECIDED")
  summary_lines.extend(
    (
      "",
      f"confirmed production ordering bugs: {confirmed_bugs}",
      f"suppression cases requiring pipeline inspection: {undecided}",
      "",
      "Decision rule:",
      "  Do not change production code for CONNECTOR_TARGET_NOT_TAGGED or",
      "  AUDIT_HARNESS_FALSE_POSITIVE findings.",
      "  Change production code only after a REAL_ORDERING_DEFECT is confirmed,",
      "  or after a TARGET_VISIBILITY_SUPPRESSION case is separately proven incorrect.",
      "",
      "Repository-wide pytest: not run",
    )
  )

  summary_text = "\n".join(summary_lines) + "\n"
  (output_dir / "summary.txt").write_text(
    summary_text,
    encoding="utf-8",
    newline="\n",
  )
  print(summary_text)

  if exceptions:
    return 1
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
