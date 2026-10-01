from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import json
import re
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
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


OUTPUT_DIR = (
  PACKAGE_DIR
  / "phase154_r1_output"
)


@dataclass(
  frozen=True,
)
class RepresentativeGroup:
  slug: str
  latex: str
  n: int
  k: int
  primary: bool


REPRESENTATIVE_GROUPS = (
  RepresentativeGroup(
    slug="pi6_3",
    latex=r"\pi_6^3",
    n=3,
    k=3,
    primary=True,
  ),
  RepresentativeGroup(
    slug="pi10_4",
    latex=r"\pi_{10}^4",
    n=4,
    k=6,
    primary=True,
  ),
  RepresentativeGroup(
    slug="pi11_4",
    latex=r"\pi_{11}^4",
    n=4,
    k=7,
    primary=True,
  ),
  RepresentativeGroup(
    slug="pi12_5",
    latex=r"\pi_{12}^5",
    n=5,
    k=7,
    primary=False,
  ),
  RepresentativeGroup(
    slug="pi16_9",
    latex=r"\pi_{16}^9",
    n=9,
    k=7,
    primary=False,
  ),
)


CONNECTORS = (
  "まず",
  "次に",
  "また",
  "さらに",
  "以上より",
  "したがって",
)


INTERNAL_RULE_PATTERNS = (
  re.compile(
    r"\bToda\b",
  ),
  re.compile(
    r"\b[A-Za-z][A-Za-z0-9_]*Statement\b",
  ),
  re.compile(
    r"\bstable[- ]range\b",
    re.IGNORECASE,
  ),
  re.compile(
    r"\bfinite[- ]dimensional\b",
    re.IGNORECASE,
  ),
  re.compile(
    r"\binference rule\b",
    re.IGNORECASE,
  ),
  re.compile(
    r"\brule[-_ ]name\b",
    re.IGNORECASE,
  ),
)


REFERENCE_HEADER_PATTERN = re.compile(
  r"^\*\*\[R[0-9]+\].*\*\*$"
)


REFERENCE_MARKER_PATTERN = re.compile(
  r"\[R([0-9]+)\]"
)


BARE_REFERENCE_USE_PATTERN = re.compile(
  r"(?:^|[。.\n])"
  r"\s*(?:まず|次に|また|さらに|以上より|したがって)?"
  r"[、,]?\s*"
  r"\[R[0-9]+\]"
  r"\s*(?:により|を用いて|を用いる)"
  r"\s*[。.]*\s*$"
)


REPEATED_SCALAR_PATTERN = re.compile(
  r"=\s*([^=,\n$]+?)\s*=\s*\1(?:\s|$|[,\n$])"
)


ASCII_WORD_PATTERN = re.compile(
  r"[A-Za-z][A-Za-z0-9_-]*"
)


MATH_PATTERN = re.compile(
  r"\$[^$]+\$"
)


def _render_group(
  group: RepresentativeGroup,
) -> str:
  report = build_standard_toda_report(
    n=group.n,
    k=group.k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _proof_body(
  markdown: str,
) -> str:
  marker = "## 証明"

  if marker not in markdown:
    return markdown

  return markdown.split(
    marker,
    1,
  )[1]


def _reference_section(
  markdown: str,
) -> str:
  marker = "## 使用する結果"

  if marker not in markdown:
    return ""

  after_header = markdown.split(
    marker,
    1,
  )[1]

  if "## 証明" in after_header:
    return after_header.split(
      "## 証明",
      1,
    )[0]

  return after_header


def _nonempty_lines(
  text: str,
) -> tuple[str, ...]:
  return tuple(
    line.strip()
    for line in text.splitlines()
    if line.strip()
  )


def _normalized_line(
  line: str,
) -> str:
  normalized = re.sub(
    r"\s+",
    " ",
    line.strip(),
  )
  normalized = normalized.replace(
    "、",
    ",",
  )
  normalized = normalized.replace(
    "。",
    ".",
  )
  return normalized


def _strip_math_and_markdown(
  line: str,
) -> str:
  line = MATH_PATTERN.sub(
    " ",
    line,
  )
  line = REFERENCE_MARKER_PATTERN.sub(
    " ",
    line,
  )
  line = re.sub(
    r"[*#`]",
    " ",
    line,
  )
  return re.sub(
    r"\s+",
    " ",
    line,
  ).strip()


def _is_reference_metadata_line(
  line: str,
) -> bool:
  if REFERENCE_HEADER_PATTERN.match(
    line.strip()
  ):
    return True

  if line.strip().startswith(
    "使用する結果を先にまとめる"
  ):
    return True

  return False


def _connector_counts(
  body: str,
) -> dict[str, int]:
  return {
    connector: body.count(
      connector
    )
    for connector in CONNECTORS
  }


def _connector_repetition_findings(
  body: str,
) -> list[dict[str, object]]:
  findings = []
  lines = _nonempty_lines(
    body
  )

  for connector in (
    "まず",
    "以上より",
    "したがって",
  ):
    hit_lines = tuple(
      line
      for line in lines
      if connector in line
    )

    if len(
      hit_lines
    ) > 1:
      findings.append(
        {
          "kind": "connector_repetition",
          "connector": connector,
          "count": len(
            hit_lines
          ),
          "examples": list(
            hit_lines[
              :6
            ]
          ),
        }
      )

  first_positions = {
    connector: body.find(
      connector
    )
    for connector in CONNECTORS
  }

  conclusion_positions = tuple(
    position
    for connector in (
      "以上より",
      "したがって",
    )
    for position in (
      first_positions[
        connector
      ],
    )
    if position >= 0
  )
  first_conclusion = (
    min(
      conclusion_positions
    )
    if conclusion_positions
    else -1
  )

  if (
    first_conclusion >= 0
    and body.find(
      "まず",
      first_conclusion + 1,
    )
    >= 0
  ):
    findings.append(
      {
        "kind": "late_opening_connector",
        "description": (
          "結論系の接続語の後に「まず」が再登場する"
        ),
      }
    )

  return findings


def _duplicate_findings(
  body: str,
) -> list[dict[str, object]]:
  findings = []
  lines = _nonempty_lines(
    body
  )
  normalized_to_lines = defaultdict(
    list
  )

  for line in lines:
    normalized_to_lines[
      _normalized_line(
        line
      )
    ].append(
      line
    )

  for normalized, originals in (
    normalized_to_lines.items()
  ):
    if (
      normalized
      and len(
        originals
      )
      > 1
    ):
      findings.append(
        {
          "kind": "exact_line_duplicate",
          "count": len(
            originals
          ),
          "normalized": normalized,
          "examples": originals[
            :5
          ],
        }
      )

  for line in lines:
    match = REPEATED_SCALAR_PATTERN.search(
      line
    )
    if match is not None:
      findings.append(
        {
          "kind": "repeated_scalar_chain",
          "example": line,
          "repeated_term": match.group(
            1
          ).strip(),
        }
      )

  math_occurrences = defaultdict(
    list
  )

  for line in lines:
    for expression in MATH_PATTERN.findall(
      line
    ):
      if len(
        expression
      ) < 7:
        continue

      math_occurrences[
        expression
      ].append(
        line
      )

  for expression, occurrence_lines in (
    math_occurrences.items()
  ):
    distinct_lines = tuple(
      dict.fromkeys(
        occurrence_lines
      )
    )

    if len(
      distinct_lines
    ) < 2:
      continue

    if expression.startswith(
      "$\\pi_"
    ):
      findings.append(
        {
          "kind": "repeated_group_equation_candidate",
          "expression": expression,
          "count": len(
            occurrence_lines
          ),
          "examples": list(
            distinct_lines[
              :5
            ]
          ),
        }
      )

  return findings


def _internal_rule_findings(
  markdown: str,
) -> list[dict[str, object]]:
  findings = []

  for line in _nonempty_lines(
    markdown
  ):
    if _is_reference_metadata_line(
      line
    ):
      continue

    matched_patterns = tuple(
      pattern.pattern
      for pattern in INTERNAL_RULE_PATTERNS
      if pattern.search(
        line
      )
    )

    if matched_patterns:
      findings.append(
        {
          "kind": "internal_rule_name_leakage",
          "example": line,
          "patterns": list(
            matched_patterns
          ),
        }
      )

  return findings


def _english_prose_findings(
  markdown: str,
) -> list[dict[str, object]]:
  findings = []

  for line in _nonempty_lines(
    markdown
  ):
    if (
      line.startswith(
        "#"
      )
      or _is_reference_metadata_line(
        line
      )
    ):
      continue

    outside_math = (
      _strip_math_and_markdown(
        line
      )
    )

    if not outside_math:
      continue

    words = ASCII_WORD_PATTERN.findall(
      outside_math
    )

    ignored = {
      "R",
      "Proposition",
      "Lemma",
      "Theorem",
      "Corollary",
      "Toda",
    }
    substantive_words = tuple(
      word
      for word in words
      if word not in ignored
    )

    if len(
      substantive_words
    ) >= 3:
      findings.append(
        {
          "kind": "english_statement_prose",
          "example": line,
          "outside_math": outside_math,
          "ascii_words": list(
            substantive_words
          ),
        }
      )

  return findings


def _reference_linkage_findings(
  markdown: str,
) -> list[dict[str, object]]:
  findings = []
  body = _proof_body(
    markdown
  )
  reference_section = (
    _reference_section(
      markdown
    )
  )

  header_numbers = {
    int(
      number
    )
    for number in re.findall(
      r"\*\*\[R([0-9]+)\]",
      reference_section,
    )
  }
  body_numbers = {
    int(
      number
    )
    for number in REFERENCE_MARKER_PATTERN.findall(
      body
    )
  }

  missing_in_body = sorted(
    header_numbers
    - body_numbers
  )
  missing_in_header = sorted(
    body_numbers
    - header_numbers
  )

  if missing_in_body:
    findings.append(
      {
        "kind": "reference_declared_but_not_used",
        "reference_numbers": missing_in_body,
      }
    )

  if missing_in_header:
    findings.append(
      {
        "kind": "reference_used_but_not_declared",
        "reference_numbers": missing_in_header,
      }
    )

  for line in _nonempty_lines(
    body
  ):
    if (
      REFERENCE_MARKER_PATTERN.search(
        line
      )
      and BARE_REFERENCE_USE_PATTERN.search(
        line
      )
    ):
      findings.append(
        {
          "kind": "bare_reference_use",
          "example": line,
          "description": (
            "Reference の数学的役割を本文側で説明せず、"
            "参照だけで文が完結している候補"
          ),
        }
      )

  return findings


def _ordering_findings(
  body: str,
) -> list[dict[str, object]]:
  findings = []
  lines = _nonempty_lines(
    body
  )

  line_connectors = []

  for index, line in enumerate(
    lines,
    start=1,
  ):
    detected = tuple(
      connector
      for connector in CONNECTORS
      if connector in line
    )

    if detected:
      line_connectors.append(
        {
          "line_number": index,
          "connectors": list(
            detected
          ),
          "line": line,
        }
      )

  conclusion_seen = False

  for row in line_connectors:
    connectors = set(
      row[
        "connectors"
      ]
    )

    if (
      "以上より" in connectors
      or "したがって" in connectors
    ):
      conclusion_seen = True
      continue

    if (
      conclusion_seen
      and "まず" in connectors
    ):
      findings.append(
        {
          "kind": "argument_ordering_candidate",
          "description": (
            "結論接続語の後に新しい導入接続語が現れる"
          ),
          "example": row[
            "line"
          ],
        }
      )

  if line_connectors:
    findings.append(
      {
        "kind": "ordering_trace",
        "description": (
          "目視監査用の接続語出現順"
        ),
        "rows": line_connectors,
      }
    )

  return findings


def _punctuation_findings(
  markdown: str,
) -> list[dict[str, object]]:
  findings = []
  prose_lines = []

  for line in _nonempty_lines(
    markdown
  ):
    if (
      line.startswith(
        "#"
      )
      or _is_reference_metadata_line(
        line
      )
    ):
      continue

    prose_lines.append(
      line
    )

  japanese_comma_lines = tuple(
    line
    for line in prose_lines
    if "、" in line
  )
  japanese_period_lines = tuple(
    line
    for line in prose_lines
    if "。" in line
  )
  ascii_comma_lines = tuple(
    line
    for line in prose_lines
    if "," in line
  )
  ascii_period_lines = tuple(
    line
    for line in prose_lines
    if "." in line
  )

  if japanese_comma_lines:
    findings.append(
      {
        "kind": "japanese_comma_usage",
        "count": len(
          japanese_comma_lines
        ),
        "examples": list(
          japanese_comma_lines[
            :8
          ]
        ),
      }
    )

  if japanese_period_lines:
    findings.append(
      {
        "kind": "japanese_period_usage",
        "count": len(
          japanese_period_lines
        ),
        "examples": list(
          japanese_period_lines[
            :8
          ]
        ),
      }
    )

  punctuation_styles = set()

  if japanese_comma_lines:
    punctuation_styles.add(
      "、"
    )

  if japanese_period_lines:
    punctuation_styles.add(
      "。"
    )

  if ascii_comma_lines:
    punctuation_styles.add(
      ","
    )

  if ascii_period_lines:
    punctuation_styles.add(
      "."
    )

  if len(
    punctuation_styles
  ) > 2:
    findings.append(
      {
        "kind": "mixed_punctuation_style",
        "styles": sorted(
          punctuation_styles
        ),
      }
    )

  return findings


def _category_findings(
  markdown: str,
) -> dict[str, list[dict[str, object]]]:
  body = _proof_body(
    markdown
  )

  return {
    "transition_repetition": (
      _connector_repetition_findings(
        body
      )
    ),
    "semantic_duplication": (
      _duplicate_findings(
        body
      )
    ),
    "internal_rule_name_leakage": (
      _internal_rule_findings(
        markdown
      )
    ),
    "english_statement_prose": (
      _english_prose_findings(
        markdown
      )
    ),
    "reference_body_linkage": (
      _reference_linkage_findings(
        markdown
      )
    ),
    "argument_contribution_ordering": (
      _ordering_findings(
        body
      )
    ),
    "punctuation": (
      _punctuation_findings(
        markdown
      )
    ),
  }


def _manual_review_lines(
  markdown: str,
) -> tuple[str, ...]:
  body = _proof_body(
    markdown
  )

  return tuple(
    (
      f"{index:03d}: {line}"
    )
    for index, line in enumerate(
      _nonempty_lines(
        body
      ),
      start=1,
    )
  )


def _render_report_markdown(
  records: list[dict[str, object]],
) -> str:
  lines = [
    "# Phase 154-R1 — Representative proof prose defect audit",
    "",
    "この監査では production code を変更していない.",
    "public Narrative route を depth=2 で取得し、代表群を同一条件で比較した.",
    "",
    "## Representative groups",
    "",
  ]

  for record in records:
    group = record[
      "group"
    ]
    lines.append(
      "- $"
      + group[
        "latex"
      ]
      + "$"
      + (
        "（primary）"
        if group[
          "primary"
        ]
        else "（secondary）"
      )
    )

  lines.extend(
    [
      "",
      "## Cross-group defect counts",
      "",
      "| category | affected groups | findings |",
      "| --- | ---: | ---: |",
    ]
  )

  category_group_counts = Counter()
  category_finding_counts = Counter()

  for record in records:
    for category, findings in (
      record[
        "categories"
      ].items()
    ):
      substantive = tuple(
        finding
        for finding in findings
        if finding[
          "kind"
        ]
        != "ordering_trace"
      )

      if substantive:
        category_group_counts[
          category
        ] += 1

      category_finding_counts[
        category
      ] += len(
        substantive
      )

  for category in (
    "transition_repetition",
    "semantic_duplication",
    "internal_rule_name_leakage",
    "english_statement_prose",
    "reference_body_linkage",
    "argument_contribution_ordering",
    "punctuation",
  ):
    lines.append(
      "| "
      + category
      + " | "
      + str(
        category_group_counts[
          category
        ]
      )
      + " | "
      + str(
        category_finding_counts[
          category
        ]
      )
      + " |"
    )

  lines.extend(
    [
      "",
      "## Group-by-group audit",
      "",
    ]
  )

  for record in records:
    group = record[
      "group"
    ]

    lines.extend(
      [
        "### $"
        + group[
          "latex"
        ]
        + "$",
        "",
        "Connector counts: `"
        + json.dumps(
          record[
            "connector_counts"
          ],
          ensure_ascii=False,
          sort_keys=True,
        )
        + "`",
        "",
      ]
    )

    for category, findings in (
      record[
        "categories"
      ].items()
    ):
      substantive = tuple(
        finding
        for finding in findings
        if finding[
          "kind"
        ]
        != "ordering_trace"
      )

      lines.append(
        "#### "
        + category
      )

      if not substantive:
        lines.extend(
          [
            "",
            "- machine-detected finding: 0",
            "",
          ]
        )
        continue

      lines.append(
        ""
      )

      for finding in substantive:
        lines.append(
          "- `"
          + str(
            finding[
              "kind"
            ]
          )
          + "`: "
          + json.dumps(
            finding,
            ensure_ascii=False,
            sort_keys=True,
          )
        )

      lines.append(
        ""
      )

    lines.extend(
      [
        "#### ordering trace",
        "",
        "```text",
      ]
    )

    ordering_traces = tuple(
      finding
      for finding in record[
        "categories"
      ][
        "argument_contribution_ordering"
      ]
      if finding[
        "kind"
      ]
      == "ordering_trace"
    )

    if ordering_traces:
      for row in ordering_traces[
        0
      ][
        "rows"
      ]:
        lines.append(
          f"{row['line_number']:03d} "
          + "/".join(
            row[
              "connectors"
            ]
          )
          + ": "
          + row[
            "line"
          ]
        )
    else:
      lines.append(
        "(no connectors detected)"
      )

    lines.extend(
      [
        "```",
        "",
        "#### numbered proof body",
        "",
        "```text",
      ]
    )
    lines.extend(
      record[
        "manual_review_lines"
      ]
    )
    lines.extend(
      [
        "```",
        "",
      ]
    )

  lines.extend(
    [
      "## R1 interpretation rule",
      "",
      "この report は機械検出結果であり、R2 の修正対象を自動決定しない.",
      "R2 では複数群に共通し、かつより上流の一般規則で説明できる defect category を1つ選ぶ.",
      "$\\pi_6^3$ 専用修正は行わない.",
      "",
      "Test Suite Consolidation は Phase 154 の対象外とする.",
      "",
    ]
  )

  return "\n".join(
    lines
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  records = []

  for group in REPRESENTATIVE_GROUPS:
    rendered = _render_group(
      group
    )

    narrative_path = (
      OUTPUT_DIR
      / (
        group.slug
        + "_narrative.md"
      )
    )
    narrative_path.write_text(
      rendered,
      encoding="utf-8",
    )

    categories = (
      _category_findings(
        rendered
      )
    )

    record = {
      "group": {
        "slug": group.slug,
        "latex": group.latex,
        "n": group.n,
        "k": group.k,
        "primary": group.primary,
      },
      "connector_counts": (
        _connector_counts(
          _proof_body(
            rendered
          )
        )
      ),
      "categories": categories,
      "manual_review_lines": list(
        _manual_review_lines(
          rendered
        )
      ),
    }
    records.append(
      record
    )

  json_path = (
    OUTPUT_DIR
    / "phase154_r1_defect_report.json"
  )
  json_path.write_text(
    json.dumps(
      records,
      ensure_ascii=False,
      indent=2,
      sort_keys=True,
    ),
    encoding="utf-8",
  )

  report = (
    _render_report_markdown(
      records
    )
  )
  report_path = (
    OUTPUT_DIR
    / "phase154_r1_defect_report.md"
  )
  report_path.write_text(
    report,
    encoding="utf-8",
  )

  print(
    "=" * 78
  )
  print(
    "Phase 154-R1 — Representative proof prose defect audit"
  )
  print(
    "=" * 78
  )
  print(
    "Production changes: none"
  )
  print(
    "Representative groups: "
    + ", ".join(
      group.slug
      for group in REPRESENTATIVE_GROUPS
    )
  )
  print(
    "Output:"
  )
  print(
    "  "
    + str(
      report_path.relative_to(
        REPO_ROOT
      )
    )
  )
  print(
    "  "
    + str(
      json_path.relative_to(
        REPO_ROOT
      )
    )
  )

  category_group_counts = Counter()
  category_finding_counts = Counter()

  for record in records:
    for category, findings in (
      record[
        "categories"
      ].items()
    ):
      substantive = tuple(
        finding
        for finding in findings
        if finding[
          "kind"
        ]
        != "ordering_trace"
      )

      if substantive:
        category_group_counts[
          category
        ] += 1

      category_finding_counts[
        category
      ] += len(
        substantive
      )

  print(
    ""
  )
  print(
    "Cross-group summary:"
  )

  for category in (
    "transition_repetition",
    "semantic_duplication",
    "internal_rule_name_leakage",
    "english_statement_prose",
    "reference_body_linkage",
    "argument_contribution_ordering",
    "punctuation",
  ):
    print(
      "  "
      + category
      + ": affected_groups="
      + str(
        category_group_counts[
          category
        ]
      )
      + ", findings="
      + str(
        category_finding_counts[
          category
        ]
      )
    )

  print(
    ""
  )
  print(
    "R1 does not modify production code."
  )
  print(
    "Inspect the Markdown report before choosing the single R2 category."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
