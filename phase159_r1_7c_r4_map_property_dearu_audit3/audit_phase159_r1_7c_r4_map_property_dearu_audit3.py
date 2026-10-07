from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
ROOT_TEXT = str(
  ROOT
)

if ROOT_TEXT not in sys.path:
  sys.path.insert(
    0,
    ROOT_TEXT,
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_aggregate_statement_renderer import (
  render_toda_group_proof_aggregate_statement_prose,
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


TARGETS = (
  (
    6,
    5,
  ),
  (
    6,
    6,
  ),
  (
    7,
    6,
  ),
  (
    9,
    7,
  ),
)

TARGET_PHRASES = (
  "は単射である.",
  "は全射である.",
)

REFERENCE_PREFIX = re.compile(
  r"^\[R\d+\]\s+より,\s+"
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


def _build(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise RuntimeError(
      "no report candidate"
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
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  return (
    raw,
    closure,
    rendered,
  )


def _rule_name(
  proof_step,
) -> str:
  inference_rule = getattr(
    proof_step,
    "inference_rule",
    None,
  )

  if inference_rule is not None:
    name = getattr(
      inference_rule,
      "name",
      None,
    )
    if name is not None:
      return str(
        name
      )

  rule = getattr(
    proof_step,
    "rule",
    None,
  )

  if rule is not None:
    name = getattr(
      rule,
      "name",
      None,
    )
    if name is not None:
      return str(
        name
      )

  return "<unknown>"


def _strip_public_prefix(
  line: str,
) -> str:
  return REFERENCE_PREFIX.sub(
    "",
    line,
  )


def _step_rows(
  presentation,
):
  rows = []

  for node_index, node in enumerate(
    presentation.nodes,
    start=1,
  ):
    step = node.proof_step

    try:
      generic = _render_generic_narrative_step(
        step
      )
    except Exception as exc:
      generic = (
        "<generic render error: "
        + type(
          exc
        ).__name__
        + ": "
        + str(
          exc
        )
        + ">"
      )

    try:
      aggregate = (
        render_toda_group_proof_aggregate_statement_prose(
          step.conclusion
        )
      )
    except Exception as exc:
      aggregate = (
        "<aggregate render error: "
        + type(
          exc
        ).__name__
        + ": "
        + str(
          exc
        )
        + ">"
      )

    rows.append(
      (
        node_index,
        type(
          step.conclusion
        ).__name__,
        _rule_name(
          step
        ),
        generic,
        aggregate,
      )
    )

  return tuple(
    rows
  )


def _print_matches(
  title: str,
  target: str,
  rows,
) -> int:
  matches = tuple(
    row
    for row in rows
    if (
      row[3] == target
      or row[4] == target
    )
  )

  print(
    title,
    len(
      matches
    ),
  )

  for (
    node_index,
    statement_type,
    rule_name,
    generic,
    aggregate,
  ) in matches:
    print(
      "  node_index:",
      node_index,
    )
    print(
      "  statement_type:",
      statement_type,
    )
    print(
      "  rule_name:",
      rule_name,
    )
    print(
      "  generic:",
      generic,
    )
    print(
      "  aggregate:",
      aggregate,
    )

  return len(
    matches
  )


def main() -> None:
  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 map-property 'である' exact source-route audit3"
  )
  print(
    "=" * 78
  )

  public_occurrences = 0
  raw_exact_matches = 0
  closure_exact_matches = 0
  unresolved = 0

  for n, k in TARGETS:
    label = _label(
      n,
      k,
    )
    raw, closure, rendered = _build(
      n,
      k,
    )

    raw_rows = _step_rows(
      raw
    )
    closure_rows = _step_rows(
      closure
    )

    public_lines = tuple(
      (
        line_number,
        line,
      )
      for line_number, line in enumerate(
        rendered.splitlines(),
        start=1,
      )
      if any(
        phrase in line
        for phrase in TARGET_PHRASES
      )
    )

    print()
    print(
      "-" * 78
    )
    print(
      label
    )
    print(
      "raw nodes:",
      len(
        raw.nodes
      ),
      "closure nodes:",
      len(
        closure.nodes
      ),
    )
    print(
      "-" * 78
    )

    for line_number, line in public_lines:
      public_occurrences += 1
      target = _strip_public_prefix(
        line
      )

      print(
        f"[PUBLIC line {line_number}]"
      )
      print(
        line
      )
      print(
        "[TARGET AFTER PREFIX STRIP]"
      )
      print(
        target
      )

      raw_count = _print_matches(
        "[RAW EXACT MATCHES]",
        target,
        raw_rows,
      )
      closure_count = _print_matches(
        "[CLOSURE EXACT MATCHES]",
        target,
        closure_rows,
      )

      raw_exact_matches += raw_count
      closure_exact_matches += closure_count

      if (
        raw_count == 0
        and closure_count == 0
      ):
        unresolved += 1
        print(
          "[CLASSIFICATION] later composition / insertion route"
        )
      elif raw_count > 0:
        print(
          "[CLASSIFICATION] raw-step renderer route"
        )
      else:
        print(
          "[CLASSIFICATION] semantic-closure step renderer route"
        )

      print()

  print(
    "=" * 78
  )
  print(
    "SUMMARY"
  )
  print(
    "=" * 78
  )
  print(
    "public occurrences:",
    public_occurrences,
  )
  print(
    "raw exact matches:",
    raw_exact_matches,
  )
  print(
    "closure exact matches:",
    closure_exact_matches,
  )
  print(
    "unresolved later-composition occurrences:",
    unresolved,
  )
  print(
    "Production code changes: none"
  )
  print(
    "Test code changes: none"
  )
  print(
    "Full pytest: not run"
  )


if __name__ == "__main__":
  main()
