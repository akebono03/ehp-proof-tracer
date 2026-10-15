from __future__ import annotations

import csv
import re
import sys
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
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
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

FINAL_RESULT_SENTENCE = (
  "以上で得た群構造, 生成元, および写像に関する結果を合わせると, "
)

KNOWN_ENGLISH_PROSE = (
  r"\text{ is injective}",
  r"\text{ is exact}",
  r"\text{ is surjective}",
  r"\text{ is an isomorphism}",
)

MALFORMED_COMPOSITIONS = (
  "である.を用いる.",
  "である.を得る.",
  "を得る.を用いる.",
  ".そのために,",
  ". そのために,",
)

REPEATED_TRANSITION_PATTERNS = (
  "まず, まず,",
  "次に, 次に,",
  "また, また,",
  "さらに, さらに,",
  "最後に, 最後に,",
  "したがって, したがって,",
  "以上より, 以上より,",
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
      + "n="
      + str(
        n
      )
      + ", k="
      + str(
        k
      )
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


def _strip_inline_math(
  line: str,
) -> str:
  result = []
  inside_math = False
  escaped = False

  for character in line:
    if escaped:
      if not inside_math:
        result.append(
          character
        )
      escaped = False
      continue

    if character == "\\":
      escaped = True
      if not inside_math:
        result.append(
          character
        )
      continue

    if character == "$":
      inside_math = not inside_math
      if not inside_math:
        result.append(
          "MATH"
        )
      continue

    if not inside_math:
      result.append(
        character
      )

  return "".join(
    result
  )


def _prose_lines(
  rendered: str,
):
  in_display_math = False

  for line_number, line in enumerate(
    rendered.splitlines(),
    start=1,
  ):
    stripped = line.strip()

    if stripped in (
      r"\[",
      "$$",
    ):
      in_display_math = True
      continue

    if stripped in (
      r"\]",
      "$$",
    ):
      in_display_math = False
      continue

    if in_display_math:
      continue

    if not stripped:
      continue

    prose = _strip_inline_math(
      stripped
    )

    yield (
      line_number,
      stripped,
      prose,
    )


def _reference_headers(
  rendered: str,
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
      rendered
    )
  )


def _body_markers(
  rendered: str,
  header_numbers: tuple[
    int,
    ...,
  ],
) -> tuple[
  int,
  ...,
]:
  all_numbers = [
    int(
      match.group(
        1
      )
    )
    for match in REFERENCE_MARKER_RE.finditer(
      rendered
    )
  ]

  remaining = list(
    all_numbers
  )

  for header_number in header_numbers:
    try:
      remaining.remove(
        header_number
      )
    except ValueError:
      pass

  return tuple(
    remaining
  )


def _root_locator(
  presentation,
) -> str | None:
  reference = (
    extract_toda_group_proof_step_literature_reference(
      presentation.root_step
    )
  )

  if reference is None:
    return None

  return (
    reference.locator
    or reference.label
  )


def _visible_internal_fallbacks(
  raw_presentation,
  rendered: str,
) -> tuple[
  str,
  ...,
]:
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )

  visible = []

  for node in presentation.nodes:
    step = node.proof_step
    generic = _render_generic_narrative_step(
      step
    )
    rule = step.inference_rule

    is_rule_name = (
      rule is not None
      and generic == rule.name
    )
    is_type_name = (
      generic
      == (
        "`"
        + type(
          step.conclusion
        ).__name__
        + "`"
      )
    )

    if not (
      is_rule_name
      or is_type_name
    ):
      continue

    if generic and generic in rendered:
      visible.append(
        generic
      )

  return tuple(
    dict.fromkeys(
      visible
    )
  )


def _add_violation(
  rows: list[dict],
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
  rows: list[dict],
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


def main() -> int:
  output_dir = (
    PACKAGE_DIR
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  scanned_groups = 0
  rendered_groups = 0
  exceptions = []
  violations = []

  category_counts = {
    "transition_repetition": 0,
    "semantic_duplication": 0,
    "internal_fallback_leakage": 0,
    "english_prose": 0,
    "reference_linkage": 0,
    "ordering": 0,
    "punctuation": 0,
  }

  groups_with_reference_section = 0
  groups_with_body_markers = 0
  groups_with_ascii_comma = 0
  groups_with_ascii_period = 0

  for n in N_RANGE:
    for k in K_RANGE:
      group = _label(
        n,
        k,
      )

      try:
        raw_presentation = (
          _build_raw_presentation(
            n,
            k,
          )
        )
        rendered = (
          render_toda_group_proof_narrative_markdown(
            raw_presentation
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
      rendered_groups += 1

      has_ascii_comma = False
      has_ascii_period = False

      for (
        _line_number,
        line,
        prose,
      ) in _prose_lines(
        rendered
      ):
        if "、" in prose:
          _add_violation(
            violations,
            n=n,
            k=k,
            group=group,
            category="punctuation",
            detail=(
              "Japanese comma: "
              + line
            ),
          )

        if "。" in prose:
          _add_violation(
            violations,
            n=n,
            k=k,
            group=group,
            category="punctuation",
            detail=(
              "Japanese period: "
              + line
            ),
          )

        if re.search(
          r",(?:\s|$)",
          prose,
        ):
          has_ascii_comma = True

        if prose.endswith(
          "."
        ):
          has_ascii_period = True

      if has_ascii_comma:
        groups_with_ascii_comma += 1

      if has_ascii_period:
        groups_with_ascii_period += 1

      for fragment in KNOWN_ENGLISH_PROSE:
        if fragment in rendered:
          _add_violation(
            violations,
            n=n,
            k=k,
            group=group,
            category="english_prose",
            detail=fragment,
          )

      visible_fallbacks = (
        _visible_internal_fallbacks(
          raw_presentation,
          rendered,
        )
      )

      for fallback in visible_fallbacks:
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="internal_fallback_leakage",
          detail=fallback,
        )

      for fragment in MALFORMED_COMPOSITIONS:
        if fragment in rendered:
          _add_violation(
            violations,
            n=n,
            k=k,
            group=group,
            category="semantic_duplication",
            detail=fragment,
          )

      if rendered.count(
        FINAL_RESULT_SENTENCE
      ) > 1:
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="semantic_duplication",
          detail=(
            "FINAL_RESULT_DERIVATION repeated "
            + str(
              rendered.count(
                FINAL_RESULT_SENTENCE
              )
            )
            + " times"
          ),
        )

      for pattern in REPEATED_TRANSITION_PATTERNS:
        if pattern in rendered:
          _add_violation(
            violations,
            n=n,
            k=k,
            group=group,
            category="transition_repetition",
            detail=pattern,
          )

      headers = _reference_headers(
        rendered
      )
      header_numbers = tuple(
        number
        for number, _title in headers
      )
      header_titles = tuple(
        title
        for _number, title in headers
      )
      body_markers = _body_markers(
        rendered,
        header_numbers,
      )

      if headers:
        groups_with_reference_section += 1

      if body_markers:
        groups_with_body_markers += 1

      expected_numbers = tuple(
        range(
          1,
          len(
            headers
          )
          + 1,
        )
      )

      if header_numbers != expected_numbers:
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="reference_linkage",
          detail=(
            "non-contiguous reference numbers: "
            + repr(
              header_numbers
            )
          ),
        )

      if len(
        set(
          header_titles
        )
      ) != len(
        header_titles
      ):
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="reference_linkage",
          detail="duplicate reference titles",
        )

      root_locator = _root_locator(
        raw_presentation
      )

      if (
        root_locator is not None
        and root_locator in header_titles
      ):
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="reference_linkage",
          detail=(
            "root reference exposed: "
            + root_locator
          ),
        )

      unknown_markers = (
        set(
          body_markers
        )
        - set(
          header_numbers
        )
      )

      if unknown_markers:
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="reference_linkage",
          detail=(
            "body markers without displayed reference: "
            + repr(
              tuple(
                sorted(
                  unknown_markers
                )
              )
            )
          ),
        )

      if body_markers:
        unused_headers = (
          set(
            header_numbers
          )
          - set(
            body_markers
          )
        )

        if unused_headers:
          _add_violation(
            violations,
            n=n,
            k=k,
            group=group,
            category="reference_linkage",
            detail=(
              "marker-bearing route has unused references: "
              + repr(
                tuple(
                  sorted(
                    unused_headers
                  )
                )
              )
            ),
          )

      rendered_lines = rendered.splitlines()

      reference_heading_count = sum(
        line.strip()
        == "## 使用する結果"
        for line in rendered_lines
      )
      proof_heading_count = sum(
        line.strip()
        == "## 証明"
        for line in rendered_lines
      )

      if reference_heading_count > 1:
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="ordering",
          detail="duplicate reference section heading",
        )

      if proof_heading_count > 1:
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="ordering",
          detail="duplicate proof section heading",
        )

      if (
        reference_heading_count == 1
        and proof_heading_count == 1
        and rendered.index(
          "## 使用する結果"
        )
        > rendered.index(
          "## 証明"
        )
      ):
        _add_violation(
          violations,
          n=n,
          k=k,
          group=group,
          category="ordering",
          detail="Reference section appears after proof section",
        )

  for row in violations:
    category = row["category"]
    if category in category_counts:
      category_counts[
        category
      ] += 1

  _write_csv(
    output_dir
    / "violations.csv",
    violations,
  )
  _write_csv(
    output_dir
    / "exceptions.csv",
    exceptions,
  )

  affected_groups = sorted(
    {
      row["group"]
      for row in violations
    }
  )

  summary_lines = [
    "=" * 78,
    "Phase 154 — Closure Audit",
    "=" * 78,
    "Production changes: none",
    "Existing test changes: none",
    "Population: n=2..15, k=0..7 (112 groups)",
    "Replay depth: 2",
    "Route: public Narrative renderer",
    "",
    "Summary",
    "-" * 78,
    "scanned groups: "
    + str(
      scanned_groups
    ),
    "rendered groups: "
    + str(
      rendered_groups
    ),
    "exceptions: "
    + str(
      len(
        exceptions
      )
    ),
    "violations: "
    + str(
      len(
        violations
      )
    ),
    "affected groups: "
    + str(
      len(
        affected_groups
      )
    ),
    "",
    "Phase 154 categories",
    "-" * 78,
  ]

  for category in (
    "transition_repetition",
    "semantic_duplication",
    "internal_fallback_leakage",
    "english_prose",
    "reference_linkage",
    "ordering",
    "punctuation",
  ):
    summary_lines.append(
      category
      + ": "
      + str(
        category_counts[
          category
        ]
      )
    )

  summary_lines.extend(
    (
      "",
      "Coverage",
      "-" * 78,
      "groups with Reference section: "
      + str(
        groups_with_reference_section
      ),
      "groups with body Reference markers: "
      + str(
        groups_with_body_markers
      ),
      "groups with ASCII comma prose: "
      + str(
        groups_with_ascii_comma
      ),
      "groups with ASCII period prose: "
      + str(
        groups_with_ascii_period
      ),
    )
  )

  if affected_groups:
    summary_lines.extend(
      (
        "",
        "Affected groups",
        "-" * 78,
        *affected_groups,
      )
    )

  if violations:
    summary_lines.extend(
      (
        "",
        "Violation preview",
        "-" * 78,
      )
    )

    for row in violations[
      :60
    ]:
      summary_lines.append(
        (
          row["group"]
          + " "
          + row["category"]
          + ": "
          + row["detail"]
        )
      )

  if exceptions:
    summary_lines.extend(
      (
        "",
        "Exception preview",
        "-" * 78,
      )
    )

    for row in exceptions[
      :30
    ]:
      summary_lines.append(
        (
          row["group"]
          + ": "
          + row["detail"]
        )
      )

  summary_lines.extend(
    (
      "",
      "Output files",
      "-" * 78,
      "audit_output/summary.txt",
      "audit_output/violations.csv",
      "audit_output/exceptions.csv",
      "=" * 78,
    )
  )

  summary = (
    "\n".join(
      summary_lines
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

  passed = (
    scanned_groups
    == EXPECTED_GROUP_COUNT
    and rendered_groups
    == EXPECTED_GROUP_COUNT
    and not exceptions
    and not violations
    and groups_with_ascii_comma
    == EXPECTED_GROUP_COUNT
    and groups_with_ascii_period
    == EXPECTED_GROUP_COUNT
  )

  if passed:
    print(
      "PASS: all 112 public Narratives satisfy the "
      "Phase 154 closure invariants."
    )
    return 0

  print(
    "FAIL: Phase 154 closure has unresolved findings. "
    "Inspect violations.csv / exceptions.csv before "
    "changing production code."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
