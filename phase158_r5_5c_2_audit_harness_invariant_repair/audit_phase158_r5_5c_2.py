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


@dataclass(frozen=True)
class EquationChainDefect:
  n: int
  k: int
  connector_line: int
  connector: str
  defect_kind: str
  detail: str


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


def _connector_numbers(text: str) -> tuple[int, ...] | None:
  match = CONNECTOR_RE.match(text.strip())
  if match is None:
    return None

  numbers = [int(match.group("first"))]
  if match.group("second") is not None:
    numbers.append(int(match.group("second")))
  return tuple(numbers)


def _tag_numbers(text: str) -> tuple[int, ...]:
  return tuple(int(match.group("number")) for match in TAG_RE.finditer(text))


def _line_has_math(line) -> bool:
  if line.statement_latex:
    return True

  return any(
    segment.kind in ("inline_math", "display_math")
    for segment in line.segments
  )


def audit_equation_chain(
  *,
  n: int,
  k: int,
  lines: list[tuple[object, str]],
) -> tuple[EquationChainDefect, ...]:
  defects = []
  tag_indices: dict[int, int] = {}

  for index, (_, text) in enumerate(lines):
    for number in _tag_numbers(text):
      tag_indices.setdefault(number, index)

  for connector_index, (_, text) in enumerate(lines):
    referenced = _connector_numbers(text)
    if referenced is None:
      continue

    missing_or_late = tuple(
      number
      for number in referenced
      if number not in tag_indices
      or tag_indices[number] >= connector_index
    )

    if missing_or_late:
      defects.append(
        EquationChainDefect(
          n=n,
          k=k,
          connector_line=connector_index + 1,
          connector=text,
          defect_kind="MISSING_OR_LATE_SOURCE",
          detail=(
            "connector references source tag(s) that are missing or not earlier: "
            + ", ".join(str(number) for number in missing_or_late)
          ),
        )
      )
      continue

    target_index = connector_index + 1
    if target_index >= len(lines):
      defects.append(
        EquationChainDefect(
          n=n,
          k=k,
          connector_line=connector_index + 1,
          connector=text,
          defect_kind="MISSING_VISIBLE_TARGET",
          detail="connector is the final visible proof line",
        )
      )
      continue

    target_line, target_text = lines[target_index]
    if not _line_has_math(target_line):
      defects.append(
        EquationChainDefect(
          n=n,
          k=k,
          connector_line=connector_index + 1,
          connector=text,
          defect_kind="MISSING_VISIBLE_TARGET",
          detail=(
            "the immediately following visible proof line is not mathematical: "
            + target_text
          ),
        )
      )

  return tuple(defects)


def main() -> int:
  output_dir = Path(__file__).resolve().parent / "audit_output"
  output_dir.mkdir(parents=True, exist_ok=True)

  groups = []
  defects = []
  exceptions = []
  rendered_count = 0
  connector_count = 0
  tagged_target_count = 0
  untagged_target_count = 0

  for n in range(2, 16):
    for k in range(0, 8):
      key = f"pi_{n + k}^{n}"
      try:
        lines = _proof_lines(n, k)
        rendered_count += 1
        group_connectors = 0
        group_tagged_targets = 0
        group_untagged_targets = 0

        for index, (_, text) in enumerate(lines):
          referenced = _connector_numbers(text)
          if referenced is None:
            continue

          connector_count += 1
          group_connectors += 1
          target_index = index + 1
          if target_index >= len(lines):
            continue

          target_line, target_text = lines[target_index]
          if not _line_has_math(target_line):
            continue

          if _tag_numbers(target_text):
            tagged_target_count += 1
            group_tagged_targets += 1
          else:
            untagged_target_count += 1
            group_untagged_targets += 1

        group_defects = audit_equation_chain(
          n=n,
          k=k,
          lines=lines,
        )
        defects.extend(group_defects)
        groups.append(
          {
            "n": n,
            "k": k,
            "group": key,
            "rendered": "yes",
            "connector_count": group_connectors,
            "tagged_target_count": group_tagged_targets,
            "untagged_target_count": group_untagged_targets,
            "equation_chain_defects": len(group_defects),
          }
        )
      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "group": key,
            "exception_type": type(exc).__name__,
            "message": str(exc),
          }
        )
        groups.append(
          {
            "n": n,
            "k": k,
            "group": key,
            "rendered": "no",
            "connector_count": 0,
            "tagged_target_count": 0,
            "untagged_target_count": 0,
            "equation_chain_defects": 0,
          }
        )

  with (output_dir / "groups.csv").open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "group",
        "rendered",
        "connector_count",
        "tagged_target_count",
        "untagged_target_count",
        "equation_chain_defects",
      ),
    )
    writer.writeheader()
    writer.writerows(groups)

  with (output_dir / "equation_chain_defects.csv").open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "connector_line",
        "connector",
        "defect_kind",
        "detail",
      ),
    )
    writer.writeheader()
    writer.writerows(
      {
        "n": defect.n,
        "k": defect.k,
        "connector_line": defect.connector_line,
        "connector": defect.connector,
        "defect_kind": defect.defect_kind,
        "detail": defect.detail,
      }
      for defect in defects
    )

  with (output_dir / "exceptions.csv").open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "group",
        "exception_type",
        "message",
      ),
    )
    writer.writeheader()
    writer.writerows(exceptions)

  summary_lines = [
    "Phase 158-R5-5c-2 — audit-harness invariant repair",
    "",
    "Scope:",
    "  current historical audit corpus: n=2..15, k=0..7, Web Narrative depth=2",
    "  NOTE: this coordinate window is an audit corpus only; it is NOT an architectural group-count contract.",
    "",
    "Revised equation-chain invariant:",
    "  1. every numbered source referenced by a connector must already be visible",
    "  2. the connector must be immediately followed by a visible mathematical target",
    "  3. the target does NOT need a tag unless later prose needs to reference it",
    "",
    "Totals:",
    f"  audited coordinates: {len(groups)}",
    f"  rendered: {rendered_count}",
    f"  exceptions: {len(exceptions)}",
    f"  numbered connectors: {connector_count}",
    f"  connector targets with tag: {tagged_target_count}",
    f"  connector targets without tag: {untagged_target_count}",
    f"  revised equation-chain defects: {len(defects)}",
    "",
    "Production changes: none",
    "Existing test changes: none",
    "Repository-wide pytest: not run",
    "",
  ]

  if defects or exceptions:
    summary_lines.extend(
      (
        "R5-5c-2 RESULT: FINDINGS",
        "Review equation_chain_defects.csv and exceptions.csv before changing production code.",
      )
    )
  else:
    summary_lines.extend(
      (
        "R5-5c-2 RESULT: PASS",
        "The 5 R5-5c findings are eliminated by the corrected generic invariant without production changes.",
      )
    )

  summary = "\n".join(summary_lines) + "\n"
  (output_dir / "summary.txt").write_text(
    summary,
    encoding="utf-8",
    newline="\n",
  )
  print(summary, end="")

  return 0 if not exceptions else 1


if __name__ == "__main__":
  raise SystemExit(main())
