from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys


PHASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PHASE_DIR.parent

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
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


CASES = (
  ("pi6_3", 3, 3),
  ("pi8_5", 5, 3),
  ("pi10_4", 4, 6),
  ("pi11_4", 4, 7),
)

MAP_PROPERTY_WORDS = (
  "単射",
  "全射",
  "同型",
  "零写像",
)

MAP_PROPERTY_VERBOSE_FORMS = (
  "は単射である.",
  "は全射である.",
  "は同型写像である.",
  "は零写像である.",
)

REFERENCE_CONNECTOR_PATTERNS = (
  re.compile(
    r"\[R[0-9]+\]\s*より,"
  ),
  re.compile(
    r"\[R[0-9]+\](?:,\s*\([0-9]+\))+\s*より,"
  ),
)

TAG_PATTERN = re.compile(
  r"\\tag\{([0-9]+)\}"
)

CONNECTOR_NUMBER_PATTERN = re.compile(
  r"\(([0-9]+)\)"
)

REFERENCE_MARKER_PATTERN = re.compile(
  r"\[R([0-9]+)\]"
)


@dataclass(frozen=True)
class DisplayBlock:
  start_line: int
  end_line: int
  lines: tuple[str, ...]

  @property
  def text(self) -> str:
    return "\n".join(
      self.lines
    )


def render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise RuntimeError(
      f"no candidate for n={n}, k={k}"
    )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def section_text(
  rendered: str,
  header: str,
  next_headers: tuple[str, ...],
) -> str:
  lines = rendered.splitlines()

  try:
    start = lines.index(
      header
    ) + 1
  except ValueError:
    return ""

  end = len(
    lines
  )

  for candidate in next_headers:
    try:
      index = lines.index(
        candidate,
        start,
      )
    except ValueError:
      continue

    end = min(
      end,
      index,
    )

  return "\n".join(
    lines[
      start:end
    ]
  ).strip()


def extract_display_blocks(
  text: str,
) -> tuple[DisplayBlock, ...]:
  lines = text.splitlines()
  blocks = []
  index = 0

  while index < len(
    lines
  ):
    if lines[index].strip() != r"\[":
      index += 1
      continue

    start = index
    index += 1
    body = []

    while (
      index < len(
        lines
      )
      and lines[index].strip() != r"\]"
    ):
      body.append(
        lines[index]
      )
      index += 1

    if index >= len(
      lines
    ):
      blocks.append(
        DisplayBlock(
          start_line=start + 1,
          end_line=len(
            lines
          ),
          lines=tuple(
            body
          ),
        )
      )
      break

    blocks.append(
      DisplayBlock(
        start_line=start + 1,
        end_line=index + 1,
        lines=tuple(
          body
        ),
      )
    )
    index += 1

  return tuple(
    blocks
  )


def line_numbered_nonblank(
  text: str,
) -> tuple[
  tuple[
    int,
    str,
  ],
  ...,
]:
  return tuple(
    (
      number,
      line.strip(),
    )
    for number, line in enumerate(
      text.splitlines(),
      start=1,
    )
    if line.strip()
  )


def exact_sequence_candidates(
  proof_body: str,
) -> tuple[dict[str, object], ...]:
  candidates = []

  for block in extract_display_blocks(
    proof_body
  ):
    text = block.text
    arrow_count = (
      text.count(
        r"\to"
      )
      + text.count(
        r"\longrightarrow"
      )
      + text.count(
        r"\xrightarrow"
      )
    )
    pi_count = text.count(
      r"\pi_{"
    )

    if (
      arrow_count >= 2
      and pi_count >= 2
    ):
      candidates.append(
        {
          "start_line": block.start_line,
          "end_line": block.end_line,
          "arrow_count": arrow_count,
          "pi_count": pi_count,
          "text": text,
        }
      )

  return tuple(
    candidates
  )


def non_display_sequence_candidates(
  proof_body: str,
) -> tuple[dict[str, object], ...]:
  display_line_numbers = set()

  for block in extract_display_blocks(
    proof_body
  ):
    display_line_numbers.update(
      range(
        block.start_line,
        block.end_line + 1,
      )
    )

  findings = []

  for number, line in enumerate(
    proof_body.splitlines(),
    start=1,
  ):
    if number in display_line_numbers:
      continue

    arrow_count = (
      line.count(
        r"\to"
      )
      + line.count(
        r"\longrightarrow"
      )
      + line.count(
        r"\xrightarrow"
      )
    )

    if (
      arrow_count >= 2
      and r"\pi_" in line
    ):
      findings.append(
        {
          "line": number,
          "text": line.strip(),
        }
      )

  return tuple(
    findings
  )


def equation_tag_audit(
  proof_body: str,
) -> dict[str, object]:
  display_blocks = extract_display_blocks(
    proof_body
  )
  tags = []
  outside = []
  duplicate_tags = []
  seen = set()

  display_ranges = tuple(
    range(
      block.start_line,
      block.end_line + 1,
    )
    for block in display_blocks
  )

  def is_display_line(
    line_number: int,
  ) -> bool:
    return any(
      line_number in line_range
      for line_range in display_ranges
    )

  for line_number, line in enumerate(
    proof_body.splitlines(),
    start=1,
  ):
    for match in TAG_PATTERN.finditer(
      line
    ):
      number = int(
        match.group(
          1
        )
      )
      tags.append(
        {
          "number": number,
          "line": line_number,
          "text": line.strip(),
        }
      )

      if number in seen:
        duplicate_tags.append(
          number
        )

      seen.add(
        number
      )

      if not is_display_line(
        line_number
      ):
        outside.append(
          {
            "number": number,
            "line": line_number,
            "text": line.strip(),
          }
        )

  numbers = tuple(
    item[
      "number"
    ]
    for item in tags
  )
  sequential = (
    numbers
    == tuple(
      range(
        1,
        len(
          numbers
        ) + 1,
      )
    )
  )

  connector_lines = []
  connector_numbers = set()

  for line_number, line in line_numbered_nonblank(
    proof_body
  ):
    if "より," not in line:
      continue

    numbers_in_line = tuple(
      int(
        value
      )
      for value in CONNECTOR_NUMBER_PATTERN.findall(
        line
      )
    )

    if not numbers_in_line:
      continue

    connector_lines.append(
      {
        "line": line_number,
        "numbers": numbers_in_line,
        "text": line,
      }
    )
    connector_numbers.update(
      numbers_in_line
    )

  undefined = tuple(
    sorted(
      connector_numbers
      - set(
        numbers
      )
    )
  )

  return {
    "tags": tags,
    "tag_numbers": numbers,
    "tags_sequential_from_one": sequential,
    "duplicate_tags": tuple(
      sorted(
        set(
          duplicate_tags
        )
      )
    ),
    "tags_outside_display_math": outside,
    "numbered_connector_lines": connector_lines,
    "undefined_connector_numbers": undefined,
  }


def map_property_audit(
  proof_body: str,
) -> dict[str, object]:
  lines = []
  forms = Counter()
  verbose = []

  for line_number, line in line_numbered_nonblank(
    proof_body
  ):
    if not any(
      word in line
      for word in MAP_PROPERTY_WORDS
    ):
      continue

    lines.append(
      {
        "line": line_number,
        "text": line,
      }
    )

    for word in MAP_PROPERTY_WORDS:
      if word in line:
        forms[
          word
        ] += 1

    if any(
      form in line
      for form in MAP_PROPERTY_VERBOSE_FORMS
    ):
      verbose.append(
        {
          "line": line_number,
          "text": line,
        }
      )

  return {
    "lines": lines,
    "word_counts": dict(
      forms
    ),
    "verbose_dearu_candidates": verbose,
  }


def exactness_reason_audit(
  proof_body: str,
) -> dict[str, object]:
  lines = []
  variants = Counter()

  for line_number, line in line_numbered_nonblank(
    proof_body
  ):
    if (
      "完全性" not in line
      and "exactness" not in line.lower()
    ):
      continue

    lines.append(
      {
        "line": line_number,
        "text": line,
      }
    )

    if "完全性より," in line:
      variants[
        "完全性より,"
      ] += 1
    elif "完全性から" in line:
      variants[
        "完全性から"
      ] += 1
    elif "完全性" in line:
      variants[
        "other_japanese"
      ] += 1
    else:
      variants[
        "english_or_internal"
      ] += 1

  return {
    "lines": lines,
    "variant_counts": dict(
      variants
    ),
  }


def reference_audit(
  rendered: str,
  proof_body: str,
) -> dict[str, object]:
  reference_section = section_text(
    rendered,
    "## 使用する結果",
    (
      "---",
      "## 証明",
    ),
  )

  declared = tuple(
    sorted(
      {
        int(
          value
        )
        for value in REFERENCE_MARKER_PATTERN.findall(
          reference_section
        )
      }
    )
  )
  used = tuple(
    sorted(
      {
        int(
          value
        )
        for value in REFERENCE_MARKER_PATTERN.findall(
          proof_body
        )
      }
    )
  )

  lines = []
  style_counts = Counter()
  nonstandard = []

  for line_number, line in line_numbered_nonblank(
    proof_body
  ):
    if "[R" not in line:
      continue

    lines.append(
      {
        "line": line_number,
        "text": line,
      }
    )

    if re.search(
      r"\[R[0-9]+\]\s*より,",
      line,
    ):
      style_counts[
        "[R#] より,"
      ] += 1
    elif re.search(
      r"\[R[0-9]+\],",
      line,
    ):
      style_counts[
        "[R#], ..."
      ] += 1
    else:
      style_counts[
        "other"
      ] += 1
      nonstandard.append(
        {
          "line": line_number,
          "text": line,
        }
      )

  return {
    "declared_reference_numbers": declared,
    "used_reference_numbers": used,
    "unused_declared_reference_numbers": tuple(
      sorted(
        set(
          declared
        )
        - set(
          used
        )
      )
    ),
    "undefined_used_reference_numbers": tuple(
      sorted(
        set(
          used
        )
        - set(
          declared
        )
      )
    ),
    "body_reference_lines": lines,
    "body_reference_style_counts": dict(
      style_counts
    ),
    "nonstandard_reference_lines": nonstandard,
  }


def group_notation_audit(
  rendered: str,
) -> dict[str, object]:
  lines = []
  suspicious = []

  for line_number, line in line_numbered_nonblank(
    rendered
  ):
    if r"\mathbb" not in line:
      continue

    lines.append(
      {
        "line": line_number,
        "text": line,
      }
    )

    if (
      r"\mathbb Z" in line
      or r"\mathbb{Z}" in line
    ):
      if (
        r"\{" not in line
        and r"\oplus" not in line
        and "= 0" not in line
        and r"\mathbb{Z}" != line.strip()
      ):
        suspicious.append(
          {
            "line": line_number,
            "text": line,
          }
        )

  return {
    "lines": lines,
    "possible_missing_generator_braces": suspicious,
  }


def display_punctuation_audit(
  proof_body: str,
) -> dict[str, object]:
  missing = []
  detached = []
  lines = proof_body.splitlines()

  for block in extract_display_blocks(
    proof_body
  ):
    next_index = block.end_line

    while (
      next_index < len(
        lines
      )
      and not lines[
        next_index
      ].strip()
    ):
      next_index += 1

    next_line = (
      None
      if next_index >= len(
        lines
      )
      else lines[
        next_index
      ].strip()
    )

    block_text = block.text.rstrip()
    closes_with_punctuation = (
      block_text.endswith(
        "."
      )
      or block_text.endswith(
        "。"
      )
      or block_text.endswith(
        ","
      )
      or block_text.endswith(
        "，"
      )
    )

    if next_line in (
      ".",
      "。",
    ):
      detached.append(
        {
          "display_start_line": block.start_line,
          "punctuation_line": next_index + 1,
          "text": next_line,
        }
      )
      continue

    if not closes_with_punctuation:
      missing.append(
        {
          "start_line": block.start_line,
          "end_line": block.end_line,
          "text": block.text,
          "next_nonblank_line": next_line,
        }
      )

  return {
    "missing_terminal_punctuation_candidates": missing,
    "detached_punctuation": detached,
  }


def target_contract_audit(
  rendered: str,
) -> dict[str, object]:
  target = section_text(
    rendered,
    "## 証明対象",
    (
      "## 使用する結果",
      "## 証明",
    ),
  )

  return {
    "target_section": target,
    "has_unwanted_show_phrase": "を示す." in target,
  }


def pi3_specific_leak_audit(
  rendered: str,
) -> dict[str, object]:
  fragments = (
    "pi_3^2",
    "pi3_2",
    "Phase159",
    "phase159",
    "Hopf preimage",
  )
  hits = []

  for line_number, line in line_numbered_nonblank(
    rendered
  ):
    for fragment in fragments:
      if fragment in line:
        hits.append(
          {
            "line": line_number,
            "fragment": fragment,
            "text": line,
          }
        )

  return {
    "hits": hits,
  }


def audit_group(
  label: str,
  n: int,
  k: int,
  rendered: str,
) -> dict[str, object]:
  proof_body = section_text(
    rendered,
    "## 証明",
    (),
  )

  return {
    "label": label,
    "n": n,
    "k": k,
    "group_latex": (
      rf"\pi_{{{n + k}}}^{{{n}}}"
    ),
    "section_headers": [
      line.strip()
      for line in rendered.splitlines()
      if line.startswith(
        "## "
      )
    ],
    "exact_sequence_candidates": exact_sequence_candidates(
      proof_body
    ),
    "non_display_sequence_candidates": non_display_sequence_candidates(
      proof_body
    ),
    "equation_tags": equation_tag_audit(
      proof_body
    ),
    "map_properties": map_property_audit(
      proof_body
    ),
    "exactness_reasons": exactness_reason_audit(
      proof_body
    ),
    "references": reference_audit(
      rendered,
      proof_body,
    ),
    "group_notation": group_notation_audit(
      rendered
    ),
    "display_punctuation": display_punctuation_audit(
      proof_body
    ),
    "target_contract": target_contract_audit(
      rendered
    ),
    "pi3_specific_leak": pi3_specific_leak_audit(
      rendered
    ),
  }


def defect_flags(
  record: dict[str, object],
) -> tuple[str, ...]:
  flags = []

  if record[
    "non_display_sequence_candidates"
  ]:
    flags.append(
      "exact_sequence_not_display_math"
    )

  equation_tags = record[
    "equation_tags"
  ]

  if equation_tags[
    "duplicate_tags"
  ]:
    flags.append(
      "duplicate_equation_tags"
    )

  if equation_tags[
    "tags_outside_display_math"
  ]:
    flags.append(
      "equation_tag_outside_display_math"
    )

  if equation_tags[
    "undefined_connector_numbers"
  ]:
    flags.append(
      "undefined_equation_reference"
    )

  if (
    equation_tags[
      "tag_numbers"
    ]
    and not equation_tags[
      "tags_sequential_from_one"
    ]
  ):
    flags.append(
      "nonsequential_public_equation_tags"
    )

  references = record[
    "references"
  ]

  if references[
    "undefined_used_reference_numbers"
  ]:
    flags.append(
      "undefined_reference_marker"
    )

  if record[
    "display_punctuation"
  ][
    "detached_punctuation"
  ]:
    flags.append(
      "detached_display_punctuation"
    )

  if record[
    "target_contract"
  ][
    "has_unwanted_show_phrase"
  ]:
    flags.append(
      "target_contains_unwanted_show_phrase"
    )

  if record[
    "pi3_specific_leak"
  ][
    "hits"
  ]:
    flags.append(
      "pi3_specific_internal_text_leak"
    )

  return tuple(
    flags
  )


def review_flags(
  record: dict[str, object],
) -> tuple[str, ...]:
  flags = []

  if len(
    record[
      "exact_sequence_candidates"
    ]
  ) > 1:
    flags.append(
      "multiple_exact_sequence_candidates"
    )

  if record[
    "map_properties"
  ][
    "verbose_dearu_candidates"
  ]:
    flags.append(
      "map_property_dearu_style_candidate"
    )

  exactness_variants = record[
    "exactness_reasons"
  ][
    "variant_counts"
  ]

  if (
    exactness_variants
    and set(
      exactness_variants
    ) != {
      "完全性より,"
    }
  ):
    flags.append(
      "exactness_reason_style_variation"
    )

  references = record[
    "references"
  ]

  if references[
    "unused_declared_reference_numbers"
  ]:
    flags.append(
      "unused_reference_candidate"
    )

  if references[
    "nonstandard_reference_lines"
  ]:
    flags.append(
      "reference_connector_style_candidate"
    )

  if record[
    "group_notation"
  ][
    "possible_missing_generator_braces"
  ]:
    flags.append(
      "group_generator_brace_candidate"
    )

  if record[
    "display_punctuation"
  ][
    "missing_terminal_punctuation_candidates"
  ]:
    flags.append(
      "display_terminal_punctuation_candidate"
    )

  return tuple(
    flags
  )


def write_group_report(
  output_dir: Path,
  record: dict[str, object],
  rendered: str,
) -> None:
  defect = defect_flags(
    record
  )
  review = review_flags(
    record
  )

  lines = [
    f"# Phase 159-R1-7 — {record['label']}",
    "",
    f"- group: ${record['group_latex']}$",
    "- source: public Narrative",
    "- replay depth: 2",
    "- production changes: none",
    "",
    "## Defect flags",
    "",
  ]

  if defect:
    lines.extend(
      f"- {item}"
      for item in defect
    )
  else:
    lines.append(
      "- none"
    )

  lines.extend(
    (
      "",
      "## Human review candidates",
      "",
    )
  )

  if review:
    lines.extend(
      f"- {item}"
      for item in review
    )
  else:
    lines.append(
      "- none"
    )

  lines.extend(
    (
      "",
      "## Compact counts",
      "",
      (
        "- exact sequence candidates: "
        + str(
          len(
            record[
              "exact_sequence_candidates"
            ]
          )
        )
      ),
      (
        "- equation tags: "
        + str(
          record[
            "equation_tags"
          ][
            "tag_numbers"
          ]
        )
      ),
      (
        "- map-property lines: "
        + str(
          len(
            record[
              "map_properties"
            ][
              "lines"
            ]
          )
        )
      ),
      (
        "- reference declarations: "
        + str(
          record[
            "references"
          ][
            "declared_reference_numbers"
          ]
        )
      ),
      (
        "- reference uses: "
        + str(
          record[
            "references"
          ][
            "used_reference_numbers"
          ]
        )
      ),
      "",
      "## Audit JSON",
      "",
      "```json",
      json.dumps(
        record,
        ensure_ascii=False,
        indent=2,
      ),
      "```",
      "",
      "## Public Narrative",
      "",
      rendered.rstrip(),
      "",
    )
  )

  (
    output_dir
    / f"{record['label']}.md"
  ).write_text(
    "\n".join(
      lines
    ),
    encoding="utf-8",
  )


def main() -> int:
  output_dir = (
    PHASE_DIR
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  records = []
  rendered_by_label = {}

  for label, n, k in CASES:
    rendered = render_group(
      n,
      k,
    )
    rendered_by_label[
      label
    ] = rendered
    record = audit_group(
      label,
      n,
      k,
      rendered,
    )
    records.append(
      record
    )

    write_group_report(
      output_dir,
      record,
      rendered,
    )

  all_defects = {
    record[
      "label"
    ]: defect_flags(
      record
    )
    for record in records
  }
  all_reviews = {
    record[
      "label"
    ]: review_flags(
      record
    )
    for record in records
  }

  summary_lines = [
    "# Phase 159-R1-7 Cross-group Display Audit",
    "",
    "Production code changes: none.",
    "Existing test changes: none.",
    "Repository-wide pytest: intentionally not run.",
    "",
    "Representative groups:",
    "- $\\pi_6^3$",
    "- $\\pi_8^5$",
    "- $\\pi_{10}^4$",
    "- $\\pi_{11}^4$",
    "",
    "## Result matrix",
    "",
    "| group | exact-seq candidates | tags | map property lines | defect flags | review candidates |",
    "| --- | ---: | --- | ---: | --- | --- |",
  ]

  for record in records:
    label = record[
      "label"
    ]
    defects = all_defects[
      label
    ]
    reviews = all_reviews[
      label
    ]
    summary_lines.append(
      "| $"
      + record[
        "group_latex"
      ]
      + "$ | "
      + str(
        len(
          record[
            "exact_sequence_candidates"
          ]
        )
      )
      + " | "
      + (
        str(
          record[
            "equation_tags"
          ][
            "tag_numbers"
          ]
        )
        if record[
          "equation_tags"
        ][
          "tag_numbers"
        ]
        else "-"
      )
      + " | "
      + str(
        len(
          record[
            "map_properties"
          ][
            "lines"
          ]
        )
      )
      + " | "
      + (
        ", ".join(
          defects
        )
        if defects
        else "none"
      )
      + " | "
      + (
        ", ".join(
          reviews
        )
        if reviews
        else "none"
      )
      + " |"
    )

  summary_lines.extend(
    (
      "",
      "## Classification rule for the next step",
      "",
      "- A: generic display rule itself is defective.",
      "- B: generic rule exists but is not applied on a route.",
      "- C: proof data / semantic classification is the source.",
      "- D: group-specific mathematical circumstance; do not generalize blindly.",
      "",
      "R1-7 is audit-only. Do not repair findings in this package.",
      "If a finding is confirmed, split it into R1-7a, R1-7b, ... by root cause.",
      "",
    )
  )

  summary_text = "\n".join(
    summary_lines
  )

  (
    output_dir
    / "phase159_r1_7_summary.md"
  ).write_text(
    summary_text,
    encoding="utf-8",
  )

  (
    output_dir
    / "phase159_r1_7_audit.json"
  ).write_text(
    json.dumps(
      {
        "phase": "159-R1-7",
        "production_changes": False,
        "existing_test_changes": False,
        "full_pytest_run": False,
        "records": records,
        "defect_flags": all_defects,
        "review_flags": all_reviews,
      },
      ensure_ascii=False,
      indent=2,
    ),
    encoding="utf-8",
  )

  print(
    "=" * 78
  )
  print(
    "Phase 159-R1-7 cross-group display audit"
  )
  print(
    "Production changes: none"
  )
  print(
    "Existing test changes: none"
  )
  print(
    "Repository-wide pytest: intentionally not run"
  )
  print(
    "=" * 78
  )
  print()
  print(
    summary_text
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
