from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)


N_RANGE = range(
  2,
  16,
)
K_RANGE = range(
  0,
  8,
)
MAX_DEPTH = 2
EXPECTED_GROUP_COUNT = 112

REFERENCE_HEADER_RE = re.compile(
  r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*"
)
REFERENCE_MARKER_RE = re.compile(
  r"\[R([0-9]+)\]"
)
REPEATED_NUMERIC_EQUALITY_RE = re.compile(
  r"=\s*([0-9]+)\s*=\s*\1(?:[^0-9]|$)"
)
FOUR_TERM_EHP_RE = re.compile(
  r"^\$\\pi_\{[^}]+\}\^\{[^}]+\}\s+"
  r"\\xrightarrow\{\\Delta\}\s+"
  r"\\pi_\{[^}]+\}\^\{[^}]+\}\s+"
  r"\\xrightarrow\{E\}\s+"
  r"\\pi_\{[^}]+\}\^\{[^}]+\}\s+"
  r"\\xrightarrow\{H\}\s+"
  r"\\pi_\{[^}]+\}\^\{[^}]+\}\$\.$"
)

STANDALONE_CONNECTORS = (
  "以上より,",
  "したがって,",
  "これより,",
)


def _label(
  n: int,
  k: int,
) -> str:
  return (
    "pi_"
    + str(
      n + k
    )
    + "^"
    + str(
      n
    )
  )


def _build_raw_presentation(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise AssertionError(
      "no report candidate for "
      + f"n={n}, k={k}"
    )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )

  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=MAX_DEPTH,
  )

  return build_toda_group_proof_presentation(
    replay
  )


def _split_reference_and_body(
  rendered: str,
) -> tuple[
  str,
  str,
]:
  marker = "\n## 証明\n"

  if marker not in rendered:
    return (
      "",
      rendered,
    )

  return tuple(
    rendered.split(
      marker,
      1,
    )
  )


def _statement_match_key(
  text: str,
) -> str:
  normalized = text.strip()

  if normalized.startswith(
    "[R"
  ):
    for connector in (
      "]より, ",
      "]を用いて, ",
    ):
      marker_end = normalized.find(
        connector
      )

      if marker_end >= 0:
        normalized = normalized[
          marker_end
          + len(
            connector
          ):
        ]
        break

  normalized = re.sub(
    r"\\tag\{[0-9]+\}",
    "",
    normalized,
  )

  return normalized.rstrip(
    ".,"
  )


def _paragraphs(
  body: str,
) -> tuple[
  str,
  ...,
]:
  return tuple(
    paragraph
    for paragraph in body.split(
      "\n\n"
    )
    if paragraph.strip()
  )


def _paragraph_indices_by_key(
  paragraphs: tuple[
    str,
    ...,
  ],
) -> dict[
  str,
  tuple[
    int,
    ...,
  ],
]:
  result = {}

  for index, paragraph in enumerate(
    paragraphs
  ):
    key = _statement_match_key(
      paragraph
    )
    result.setdefault(
      key,
      [],
    ).append(
      index
    )

  return {
    key: tuple(
      indices
    )
    for key, indices in result.items()
  }


def _unique_visible_index_for_step(
  step,
  indices_by_key,
) -> int | None:
  rendered = (
    _render_generic_narrative_step(
      step
    )
  )

  if not rendered:
    return None

  key = _statement_match_key(
    rendered
  )
  matches = indices_by_key.get(
    key,
    (),
  )

  if len(
    matches
  ) != 1:
    return None

  return matches[
    0
  ]


def _reference_headers(
  reference: str,
) -> tuple[
  tuple[
    int,
    str,
  ],
  ...,
]:
  return tuple(
    (
      int(
        match.group(
          1
        )
      ),
      match.group(
        2
      ),
    )
    for match in REFERENCE_HEADER_RE.finditer(
      reference
    )
  )


def _body_marker_numbers(
  body: str,
) -> tuple[
  int,
  ...,
]:
  return tuple(
    int(
      match.group(
        1
      )
    )
    for match in REFERENCE_MARKER_RE.finditer(
      body
    )
  )


def _add_finding(
  rows: list[
    dict,
  ],
  *,
  n: int,
  k: int,
  group: str,
  category: str,
  detail: str,
) -> None:
  rows.append(
    {
      "n": n,
      "k": k,
      "group": group,
      "category": category,
      "detail": detail,
    }
  )


def _write_csv(
  path: Path,
  rows: list[
    dict,
  ],
) -> None:
  fieldnames = (
    "n",
    "k",
    "group",
    "category",
    "detail",
  )

  with path.open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=fieldnames,
    )
    writer.writeheader()
    writer.writerows(
      rows
    )


def _visible_dependency_order_findings(
  *,
  n: int,
  k: int,
  group: str,
  presentation,
  body: str,
  rows: list[
    dict,
  ],
) -> None:
  body_paragraphs = _paragraphs(
    body
  )
  indices_by_key = (
    _paragraph_indices_by_key(
      body_paragraphs
    )
  )
  checked_pairs = set()

  for node in presentation.nodes:
    step = node.proof_step
    role = (
      classify_toda_proof_step_role(
        step
      )
    )

    if role not in (
      TodaProofDependencyRole.ORDER,
      TodaProofDependencyRole.MAP_PROPERTY,
    ):
      continue

    conclusion_index = (
      _unique_visible_index_for_step(
        step,
        indices_by_key,
      )
    )

    if conclusion_index is None:
      continue

    for premise in step.premises:
      premise_index = (
        _unique_visible_index_for_step(
          premise,
          indices_by_key,
        )
      )

      if premise_index is None:
        continue

      pair = (
        id(
          premise
        ),
        id(
          step
        ),
      )

      if pair in checked_pairs:
        continue

      checked_pairs.add(
        pair
      )

      if premise_index > conclusion_index:
        _add_finding(
          rows,
          n=n,
          k=k,
          group=group,
          category="visible_dependency_order",
          detail=(
            "premise after conclusion: "
            + _render_generic_narrative_step(
              premise
            )
            + " -> "
            + _render_generic_narrative_step(
              step
            )
          ),
        )


def _zero_map_visibility_findings(
  *,
  n: int,
  k: int,
  group: str,
  presentation,
  body: str,
  rows: list[
    dict,
  ],
) -> None:
  body_paragraphs = _paragraphs(
    body
  )
  indices_by_key = (
    _paragraph_indices_by_key(
      body_paragraphs
    )
  )

  for node in presentation.nodes:
    step = node.proof_step
    rendered = (
      _render_generic_narrative_step(
        step
      )
    )

    if (
      not rendered
      or "零写像である."
      not in rendered
    ):
      continue

    visible_index = (
      _unique_visible_index_for_step(
        step,
        indices_by_key,
      )
    )

    if visible_index is not None:
      continue

    if (
      "Δ=0" in body
      or r"\Delta=0" in body
    ) and (
      r"\Delta" in rendered
      or (
        step.inference_rule is not None
        and "Delta"
        in step.inference_rule.name
      )
    ):
      _add_finding(
        rows,
        n=n,
        k=k,
        group=group,
        category="zero_map_used_without_visible_statement",
        detail=(
          "body uses zero-map shorthand while full statement is hidden: "
          + rendered
        ),
      )


def _redundant_left_ehp_findings(
  *,
  n: int,
  k: int,
  group: str,
  body: str,
  rows: list[
    dict,
  ],
) -> None:
  body_paragraphs = _paragraphs(
    body
  )
  injective_indices = tuple(
    index
    for index, paragraph in enumerate(
      body_paragraphs
    )
    if (
      paragraph.strip().startswith(
        "$E:"
      )
      and " は単射である."
      in paragraph
    )
  )

  if not injective_indices:
    return

  first_injective_index = min(
    injective_indices
  )

  for index, paragraph in enumerate(
    body_paragraphs
  ):
    stripped = paragraph.strip()

    if (
      index > first_injective_index
      and FOUR_TERM_EHP_RE.match(
        stripped
      )
    ):
      _add_finding(
        rows,
        n=n,
        k=k,
        group=group,
        category="possible_redundant_left_ehp_term",
        detail=stripped,
      )


def _connector_and_numeric_findings(
  *,
  n: int,
  k: int,
  group: str,
  body: str,
  rows: list[
    dict,
  ],
) -> None:
  body_paragraphs = _paragraphs(
    body
  )

  for index, paragraph in enumerate(
    body_paragraphs
  ):
    stripped = paragraph.strip()

    if stripped in STANDALONE_CONNECTORS:
      _add_finding(
        rows,
        n=n,
        k=k,
        group=group,
        category="standalone_connector",
        detail=(
          f"paragraph[{index}]: "
          + stripped
        ),
      )

    if REPEATED_NUMERIC_EQUALITY_RE.search(
      stripped
    ):
      _add_finding(
        rows,
        n=n,
        k=k,
        group=group,
        category="repeated_numeric_equality",
        detail=stripped,
      )


def _reference_marker_findings(
  *,
  n: int,
  k: int,
  group: str,
  reference: str,
  body: str,
  rows: list[
    dict,
  ],
) -> None:
  headers = _reference_headers(
    reference
  )
  markers = set(
    _body_marker_numbers(
      body
    )
  )

  for number, title in headers:
    if number not in markers:
      _add_finding(
        rows,
        n=n,
        k=k,
        group=group,
        category="public_reference_without_body_marker",
        detail=(
          f"[R{number}] {title}"
        ),
      )


def main() -> int:
  output_dir = (
    PACKAGE_DIR
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  findings = []
  exceptions = []
  narratives_dir = (
    output_dir
    / "narratives"
  )
  narratives_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  scanned_groups = 0

  for n in N_RANGE:
    for k in K_RANGE:
      group = _label(
        n,
        k,
      )

      try:
        raw = (
          _build_raw_presentation(
            n,
            k,
          )
        )
        presentation = (
          build_toda_group_proof_narrative_semantic_closure_presentation(
            raw
          )
        )
        rendered = (
          render_toda_group_proof_narrative_markdown(
            raw
          )
        )
      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "category": "render_exception",
            "detail": (
              type(
                exc
              ).__name__
              + ": "
              + str(
                exc
              )
            ),
          }
        )
        continue

      scanned_groups += 1
      reference, body = (
        _split_reference_and_body(
          rendered
        )
      )

      _visible_dependency_order_findings(
        n=n,
        k=k,
        group=group,
        presentation=presentation,
        body=body,
        rows=findings,
      )
      _zero_map_visibility_findings(
        n=n,
        k=k,
        group=group,
        presentation=presentation,
        body=body,
        rows=findings,
      )
      _redundant_left_ehp_findings(
        n=n,
        k=k,
        group=group,
        body=body,
        rows=findings,
      )
      _connector_and_numeric_findings(
        n=n,
        k=k,
        group=group,
        body=body,
        rows=findings,
      )
      _reference_marker_findings(
        n=n,
        k=k,
        group=group,
        reference=reference,
        body=body,
        rows=findings,
      )

      if any(
        row["group"] == group
        for row in findings
      ):
        (
          narratives_dir
          / (
            group
            + ".md"
          )
        ).write_text(
          rendered,
          encoding="utf-8",
        )

  _write_csv(
    output_dir
    / "findings.csv",
    findings,
  )
  _write_csv(
    output_dir
    / "exceptions.csv",
    exceptions,
  )

  counts = Counter(
    row["category"]
    for row in findings
  )
  affected_groups = sorted(
    {
      row["group"]
      for row in findings
    }
  )

  categories = (
    "visible_dependency_order",
    "zero_map_used_without_visible_statement",
    "possible_redundant_left_ehp_term",
    "standalone_connector",
    "repeated_numeric_equality",
    "public_reference_without_body_marker",
  )

  lines = [
    "=" * 78,
    "Phase157 R11-R18 — 112-group Narrative Re-audit",
    "=" * 78,
    "Production code changes: none",
    "Test code changes: none",
    "Population: n=2..15, k=0..7 (112 groups)",
    "Replay depth: 2",
    "",
    "Summary",
    "-" * 78,
    "scanned groups: "
    + str(
      scanned_groups
    ),
    "exceptions: "
    + str(
      len(
        exceptions
      )
    ),
    "findings: "
    + str(
      len(
        findings
      )
    ),
    "affected groups: "
    + str(
      len(
        affected_groups
      )
    ),
    "",
    "Categories",
    "-" * 78,
  ]

  for category in categories:
    lines.append(
      category
      + ": "
      + str(
        counts.get(
          category,
          0,
        )
      )
    )

  if affected_groups:
    lines.extend(
      (
        "",
        "Affected groups",
        "-" * 78,
        *affected_groups,
      )
    )

  if findings:
    lines.extend(
      (
        "",
        "Finding preview",
        "-" * 78,
      )
    )

    for row in findings[
      :100
    ]:
      lines.append(
        (
          row["group"]
          + " "
          + row["category"]
          + ": "
          + row["detail"]
        )
      )

  if exceptions:
    lines.extend(
      (
        "",
        "Exception preview",
        "-" * 78,
      )
    )

    for row in exceptions[
      :30
    ]:
      lines.append(
        row["group"]
        + ": "
        + row["detail"]
      )

  closure_ready = (
    scanned_groups
    == EXPECTED_GROUP_COUNT
    and not exceptions
    and not findings
  )

  lines.extend(
    (
      "",
      "Closure candidate",
      "-" * 78,
      (
        "YES"
        if closure_ready
        else "NO"
      ),
      "",
      "Output files",
      "-" * 78,
      "audit_output/summary.txt",
      "audit_output/findings.csv",
      "audit_output/exceptions.csv",
      "audit_output/narratives/<affected-group>.md",
      "=" * 78,
    )
  )

  summary = (
    "\n".join(
      lines
    )
    + "\n"
  )

  (
    output_dir
    / "summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )

  print(
    summary
  )

  if scanned_groups != EXPECTED_GROUP_COUNT:
    print(
      "FAIL: expected 112 groups."
    )
    return 1

  if exceptions:
    print(
      "FAIL: render exceptions occurred."
    )
    return 1

  print(
    "AUDIT COMPLETE"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
