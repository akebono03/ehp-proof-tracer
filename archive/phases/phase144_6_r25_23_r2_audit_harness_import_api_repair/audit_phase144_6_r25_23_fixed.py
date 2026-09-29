import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)

TAG_PATTERN = re.compile(
  r"\\tag\{(\d+)\}"
)
REFERENCE_PATTERN = re.compile(
  r"\((\d+)\)"
)


def _group_result(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  if not report.candidates:
    raise RuntimeError(
      f"No report candidate for n={n}, k={k}"
    )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _data(
  n,
  k,
):
  group_result = _group_result(
    n,
    k,
  )
  replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  markdown = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  return (
    presentation,
    blocks,
    sidecar,
    arguments,
    markdown,
  )


def _step_label(
  step,
):
  if step is None:
    return "<none>"
  return type(
    step.conclusion
  ).__name__


def _block_summary(
  block,
):
  return (
    f"{block.role.value}:"
    + ",".join(
      type(
        step.conclusion
      ).__name__
      for step in block.steps
    )
  )


def _forward_references(
  markdown,
):
  defined = set()
  forward = []

  for line_index, line in enumerate(
    markdown.splitlines(),
    start=1,
  ):
    tags = {
      int(
        match.group(1)
      )
      for match in TAG_PATTERN.finditer(
        line
      )
    }
    references = {
      int(
        match.group(1)
      )
      for match in REFERENCE_PATTERN.finditer(
        line
      )
    }
    references.difference_update(
      tags
    )

    for reference in sorted(
      references
    ):
      if reference not in defined:
        forward.append(
          (
            line_index,
            reference,
            line,
          )
        )

    defined.update(
      tags
    )

  return tuple(
    forward
  )


def _duplicate_exactness_lines(
  markdown,
):
  counts = {}

  for line in markdown.splitlines():
    if (
      "は完全である." not in line
      and "次の完全列を考える." not in line
    ):
      continue

    counts[line] = (
      counts.get(
        line,
        0,
      )
      + 1
    )

  return tuple(
    (
      line,
      count,
    )
    for line, count in counts.items()
    if count > 1
  )


def audit_target(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
    markdown,
  ) = _data(
    n,
    k,
  )

  print(
    "=" * 78
  )
  print(
    f"pi_{n + k}^{n}"
  )
  print(
    "=" * 78
  )
  print(
    "presentation nodes:",
    len(
      presentation.nodes
    ),
  )
  print(
    "blocks:",
    len(
      blocks
    ),
  )
  print(
    "arguments:",
    len(
      arguments
    ),
  )
  print(
    "markdown chars:",
    len(
      markdown
    ),
  )

  exactness_blocks = tuple(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )
  print(
    "all exactness blocks:",
    len(
      exactness_blocks
    ),
  )

  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  source_index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      arguments
    )
  }

  print()
  print(
    "ARGUMENT EVIDENCE"
  )
  print(
    "-" * 78
  )

  for ordered_position, argument in enumerate(
    ordered_arguments
  ):
    source_index = source_index_by_identity[
      id(
        argument
      )
    ]
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    direct_premises = (
      ()
      if conclusion_step is None
      else extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
        argument,
        arguments,
      )
    )
    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        source_index,
      )
    )
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        source_index,
      )
    )
    local_exactness = tuple(
      block
      for block in local_body
      if (
        block.role
        is TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      )
    )

    print(
      f"argument {ordered_position + 1}: "
      f"role={argument.role.value}"
    )
    print(
      "  conclusion:",
      _step_label(
        conclusion_step
      ),
    )
    print(
      "  direct premises:",
      tuple(
        _step_label(
          step
        )
        for step in direct_premises
      ),
    )
    print(
      "  local blocks:",
      len(
        local_body
      ),
      "local exactness:",
      len(
        local_exactness
      ),
      "method evidence:",
      len(
        evidence
      ),
    )

    for block in evidence:
      print(
        "    evidence:",
        _block_summary(
          block
        ),
      )

  print()
  print(
    "DEPENDENCY ORDER"
  )
  print(
    "-" * 78
  )
  forward = (
    _forward_references(
      markdown
    )
  )
  print(
    "forward references:",
    len(
      forward
    ),
  )
  for (
    line_index,
    reference,
    line,
  ) in forward[
    :20
  ]:
    print(
      f"  line {line_index}: "
      f"({reference}) before definition :: "
      f"{line}"
    )

  print()
  print(
    "EXACTNESS DUPLICATION"
  )
  print(
    "-" * 78
  )
  duplicates = (
    _duplicate_exactness_lines(
      markdown
    )
  )
  print(
    "duplicate exactness lines:",
    len(
      duplicates
    ),
  )
  for line, count in duplicates[
    :20
  ]:
    print(
      f"  x{count}: {line}"
    )

  print()
  print(
    "NUMBERED EQUATIONS"
  )
  print(
    "-" * 78
  )
  numbered_lines = tuple(
    line
    for line in markdown.splitlines()
    if TAG_PATTERN.search(
      line
    )
  )
  print(
    "numbered equations:",
    len(
      numbered_lines
    ),
  )
  for line in numbered_lines[
    :30
  ]:
    print(
      " ",
      line,
    )
  print()


def main():
  print(
    "Phase 144-6 R25-23 Narrative evidence selection / dependency ordering audit"
  )
  print(
    "Production changes: none"
  )
  print()

  for n, k in TARGETS:
    audit_target(
      n,
      k,
    )


if __name__ == "__main__":
  main()
