from __future__ import annotations

import inspect
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
import toda_group_proof_narrative_equation_numbering as numbering_module
from toda_group_proof_narrative_equation_numbering import (
  _numbered_step_line,
  number_toda_group_proof_narrative_equations,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)


TARGET_PLAIN = r"$2\nu' = \eta_{3}^{3}$"


def all_indices(
  lines: list[str],
  target: str,
) -> tuple[
  int,
  ...,
]:
  return tuple(
    index
    for index, line in enumerate(
      lines
    )
    if line == target
  )


def main() -> int:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  lines = rendered.splitlines()

  transitions = (
    extract_toda_group_proof_narrative_step_transitions(
      presentation,
      blocks,
    )
  )

  target_step = next(
    transition.target_step
    for transition in transitions
    if (
      _render_generic_narrative_step(
        transition.target_step
      )
      == TARGET_PLAIN
    )
  )

  source_steps = tuple(
    transition.source_step
    for transition in transitions
    if transition.target_step is target_step
  )

  source_plains = tuple(
    _render_generic_narrative_step(
      step
    )
    for step in source_steps
  )
  target_tagged = (
    _numbered_step_line(
      target_step,
      3,
    )
  )

  source = inspect.getsource(
    number_toda_group_proof_narrative_equations
  )

  result_direct = (
    number_toda_group_proof_narrative_equations(
      rendered,
      presentation,
      blocks,
    )
  )
  result_lines = result_direct.splitlines()

  lines_out = [
    "=" * 120,
    "Phase 158-R5-5b repair1t - target numbering runtime diagnosis",
    "=" * 120,
    "",
    "A. RUNTIME SOURCE LOCATION",
    "-" * 120,
    "module_path="
    + str(
      Path(
        inspect.getsourcefile(
          numbering_module
        )
        or ""
      ).resolve()
    ),
    "",
    "B. RUNTIME NUMBERING SOURCE",
    "-" * 120,
    source,
    "",
    "C. TARGET / SOURCE IDENTITIES",
    "-" * 120,
    "target_id="
    + str(
      id(
        target_step
      )
    ),
    "target_plain="
    + _render_generic_narrative_step(
      target_step
    ),
    "target_tagged_expected="
    + target_tagged,
    "target_plain_indices="
    + str(
      all_indices(
        lines,
        TARGET_PLAIN,
      )
    ),
    "target_tagged_indices="
    + str(
      all_indices(
        lines,
        target_tagged,
      )
    ),
    "",
  ]

  for index, (
    step,
    plain,
  ) in enumerate(
    zip(
      source_steps,
      source_plains,
    )
  ):
    tagged = (
      _numbered_step_line(
        step,
        index + 1,
      )
    )
    lines_out.append(
      f"source_{index + 1}_id={id(step)}"
    )
    lines_out.append(
      f"source_{index + 1}_plain={plain}"
    )
    lines_out.append(
      f"source_{index + 1}_plain_indices="
      + str(
        all_indices(
          lines,
          plain,
        )
      )
    )
    lines_out.append(
      f"source_{index + 1}_tagged_expected={tagged}"
    )
    lines_out.append(
      f"source_{index + 1}_tagged_indices="
      + str(
        all_indices(
          lines,
          tagged,
        )
      )
    )

  lines_out.extend(
    (
      "",
      "D. CONNECTOR LINES",
      "-" * 120,
    )
  )

  for index, line in enumerate(
    lines
  ):
    if (
      "より," in line
      and (
        "(" in line
        or "これ" in line
      )
    ):
      lines_out.append(
        f"{index:03d}: {line}"
      )

  lines_out.extend(
    (
      "",
      "E. DIRECT NUMBERING RESULT STATE",
      "-" * 120,
      "target_tag3_present="
      + str(
        target_tagged
        in result_direct
      ),
      "target_plain_present="
      + str(
        TARGET_PLAIN
        in result_direct
      ),
      "connector_12_present="
      + str(
        "(1) と (2) より, "
        in result_direct
      ),
      "",
      "F. DIRECT NUMBERING RESULT",
      "-" * 120,
      result_direct,
      "",
      "=" * 120,
      "Production code changes: none",
      "Repository-wide pytest: not run",
      "=" * 120,
    )
  )

  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    output_dir
    / "target_numbering_runtime.txt"
  ).write_text(
    "\n".join(
      lines_out
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    "\n".join(
      lines_out
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
