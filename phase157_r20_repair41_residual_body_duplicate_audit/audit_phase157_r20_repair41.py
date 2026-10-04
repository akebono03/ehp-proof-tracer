from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _phase157_r11_reference_statement_match_key,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  normalize_toda_group_proof_narrative_connectors,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
  suppress_toda_group_proof_narrative_reference_body_restatements,
  suppress_toda_group_proof_narrative_reflexive_equalities,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
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


WATCH = (
  r"H\left(\nu'\right) = \eta_{5}",
  r"2\nu' = \eta_{3}^{3}",
  r"\Delta: \pi_{7}^{5} \to \pi_{5}^{2}",
  "これらより,",
  "(6) と (7) より,",
  "したがって,",
)


def strip_reference_prefix(
  paragraph: str,
) -> str:
  stripped = paragraph.strip()

  if not stripped.startswith(
    "[R"
  ):
    return stripped

  marker_end = stripped.find(
    "]"
  )

  if marker_end < 0:
    return stripped

  suffix = stripped[
    marker_end + 1:
  ]

  for prefix in (
    "より, ",
    "を用いて, ",
    "を用いる. ",
  ):
    if suffix.startswith(
      prefix
    ):
      return suffix[
        len(
          prefix
        ):
      ]

  return stripped


def normalized_key(
  paragraph: str,
) -> str:
  stripped = strip_reference_prefix(
    paragraph
  )

  return (
    _phase157_r11_reference_statement_match_key(
      stripped
    )
  )


def print_watch(
  label: str,
  markdown: str,
) -> None:
  print("")
  print("=" * 96)
  print(label)
  print("=" * 96)

  for index, paragraph in enumerate(
    markdown.split(
      "\n\n"
    )
  ):
    if any(
      token in paragraph
      for token in WATCH
    ):
      print(
        f"[{index}]",
        paragraph,
      )


def print_duplicate_keys(
  markdown: str,
) -> None:
  paragraphs = tuple(
    paragraph
    for paragraph in markdown.split(
      "\n\n"
    )
    if paragraph.strip()
  )
  keys = tuple(
    normalized_key(
      paragraph
    )
    for paragraph in paragraphs
  )
  counts = Counter(
    keys
  )

  print("")
  print("=" * 96)
  print("DUPLICATE NORMALIZED KEYS")
  print("=" * 96)

  for key, count in counts.most_common():
    if count < 2:
      continue

    matching = tuple(
      (
        index,
        paragraph,
      )
      for index, paragraph in enumerate(
        paragraphs
      )
      if normalized_key(
        paragraph
      )
      == key
    )

    if not any(
      any(
        token in paragraph
        for token in WATCH
      )
      for _, paragraph in matching
    ):
      continue

    print(
      "count=",
      count,
      "key=",
      repr(
        key
      ),
    )

    for index, paragraph in matching:
      print(
        f"  [{index}]",
        paragraph,
      )


def compare(
  label: str,
  before: str,
  after: str,
) -> None:
  print("")
  print("=" * 96)
  print(label)
  print("=" * 96)
  print(
    "changed:",
    before != after,
  )
  print(
    "chars:",
    len(
      before
    ),
    "->",
    len(
      after
    ),
  )

  if before == after:
    return

  before_paragraphs = before.split(
    "\n\n"
  )
  after_paragraphs = after.split(
    "\n\n"
  )

  removed = [
    paragraph
    for paragraph in before_paragraphs
    if paragraph not in after_paragraphs
  ]
  added = [
    paragraph
    for paragraph in after_paragraphs
    if paragraph not in before_paragraphs
  ]

  print("removed:")
  for paragraph in removed:
    if any(
      token in paragraph
      for token in WATCH
    ):
      print(
        "  -",
        paragraph,
      )

  print("added:")
  for paragraph in added:
    if any(
      token in paragraph
      for token in WATCH
    ):
      print(
        "  +",
        paragraph,
      )


def main() -> int:
  report = build_standard_toda_report(
    n=3,
    k=3,
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )

  print_watch(
    "FINAL BODY WATCH",
    body,
  )
  print_duplicate_keys(
    body
  )

  duplicate_suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      statement_lines,
    )
  )
  compare(
    "RE-RUN reference_body_duplicates",
    body,
    duplicate_suppressed,
  )
  print_watch(
    "AFTER reference_body_duplicates",
    duplicate_suppressed,
  )

  restatement_suppressed = (
    suppress_toda_group_proof_narrative_reference_body_restatements(
      body,
      statement_lines,
    )
  )
  compare(
    "RE-RUN reference_body_restatements",
    body,
    restatement_suppressed,
  )
  print_watch(
    "AFTER reference_body_restatements",
    restatement_suppressed,
  )

  connector_normalized = (
    normalize_toda_group_proof_narrative_connectors(
      body
    )
  )
  compare(
    "RE-RUN connector normalization",
    body,
    connector_normalized,
  )
  print_watch(
    "AFTER connector normalization",
    connector_normalized,
  )

  reflexive_suppressed = (
    suppress_toda_group_proof_narrative_reflexive_equalities(
      presentation,
      body,
    )
  )
  compare(
    "RE-RUN reflexive suppression",
    body,
    reflexive_suppressed,
  )

  print("")
  print("=" * 96)
  print("COUNTS")
  print("=" * 96)

  for token in WATCH:
    print(
      repr(
        token
      ),
      body.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
