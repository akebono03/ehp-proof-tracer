from pathlib import Path
import sys
from functools import wraps


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
import toda_group_proof_narrative_contribution_renderer as contribution_renderer
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)


def _presentation():
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

  return build_toda_group_proof_presentation(
    replay
  )


def _entry_summary(
  entries,
  lines_by_number=None,
):
  rows = []

  for entry in entries:
    step_rows = []

    for proof_step in entry.proof_steps:
      boundary = classify_toda_literature_statement_step(
        proof_step
      )
      step_rows.append(
        (
          getattr(
            proof_step.inference_rule,
            "name",
            None,
          ),
          (
            boundary.component_key
            if boundary is not None
            else None
          ),
        )
      )

    rows.append(
      (
        entry.number,
        entry.reference.locator,
        tuple(
          step_rows
        ),
        (
          lines_by_number.get(
            entry.number,
            (),
          )
          if lines_by_number is not None
          else ()
        ),
      )
    )

  return tuple(
    rows
  )


def _print_entries(
  title,
  entries,
  lines_by_number=None,
):
  print()
  print(title)
  print("-" * len(title))

  for (
    number,
    locator,
    step_rows,
    statement_lines,
  ) in _entry_summary(
    entries,
    lines_by_number,
  ):
    print(
      f"R{number}: {locator}"
    )

    for rule_name, component_key in step_rows:
      print(
        "  step: "
        f"component={component_key!r} "
        f"rule={rule_name!r}"
      )

    for line in statement_lines:
      print(
        f"  line: {line}"
      )


def _wrap_entry_only(
  name,
):
  original = getattr(
    contribution_renderer,
    name,
  )

  @wraps(
    original
  )
  def wrapper(
    *args,
    **kwargs,
  ):
    if args:
      try:
        _print_entries(
          name + " INPUT",
          args[0],
        )
      except Exception:
        pass

    result = original(
      *args,
      **kwargs,
    )

    try:
      _print_entries(
        name + " OUTPUT",
        result,
      )
    except Exception:
      pass

    return result

  setattr(
    contribution_renderer,
    name,
    wrapper,
  )


def _wrap_entries_and_lines(
  name,
):
  original = getattr(
    contribution_renderer,
    name,
  )

  @wraps(
    original
  )
  def wrapper(
    *args,
    **kwargs,
  ):
    if len(
      args
    ) >= 2:
      try:
        _print_entries(
          name + " INPUT",
          args[0],
          args[1],
        )
      except Exception:
        pass

    result = original(
      *args,
      **kwargs,
    )

    if (
      isinstance(
        result,
        tuple,
      )
      and len(
        result
      ) >= 2
    ):
      try:
        _print_entries(
          name + " OUTPUT",
          result[0],
          result[1],
        )
      except Exception:
        pass

    return result

  setattr(
    contribution_renderer,
    name,
    wrapper,
  )


def _wrap_statement_lines():
  name = (
    "_toda_group_proof_narrative_reference_statement_lines_by_number"
  )
  original = getattr(
    contribution_renderer,
    name,
  )

  @wraps(
    original
  )
  def wrapper(
    presentation,
    entries,
  ):
    result = original(
      presentation,
      entries,
    )
    _print_entries(
      name + " RESULT",
      entries,
      result,
    )
    return result

  setattr(
    contribution_renderer,
    name,
    wrapper,
  )


def main():
  print("=" * 78)
  print("Phase157 R11-R8 - Reference filter trace audit")
  print("=" * 78)

  _wrap_entry_only(
    "filter_phase157_r3_pi6_3_reference_entries"
  )
  _wrap_entries_and_lines(
    "exclude_toda_group_proof_narrative_root_reference"
  )
  _wrap_entries_and_lines(
    "filter_toda_group_proof_narrative_reference_entries_by_body_usage"
  )
  _wrap_entries_and_lines(
    "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage"
  )
  _wrap_entries_and_lines(
    "_phase157_r3_restore_pi6_3_earlier_prop56_reference"
  )
  _wrap_statement_lines()

  rendered = render_toda_group_proof_narrative_markdown(
    _presentation()
  )

  print()
  print("FINAL PUBLIC REFERENCE HEADERS")
  print("------------------------------")

  reference_part, body = rendered.split(
    "\n## 証明\n",
    1,
  )

  for line in reference_part.splitlines():
    if line.startswith(
      "**[R"
    ):
      print(
        line
      )

  print()
  print("FINAL TARGET LINES")
  print("------------------")

  targets = (
    "[R",
    r"H\left(\nu'\right)",
    r"\nu' \in \pi_{6}^{3}",
    r"\pi_{6}^{5} = ",
    r"H: \pi_{6}^{3} \to \pi_{6}^{5}",
  )

  for number, line in enumerate(
    rendered.splitlines(),
    start=1,
  ):
    if any(
      target in line
      for target in targets
    ):
      print(
        f"{number:04d}: {line}"
      )

  print()
  print("BODY START")
  print("----------")
  for number, line in enumerate(
    body.splitlines()[
      :12
    ],
    start=1,
  ):
    print(
      f"{number:04d}: {line}"
    )

  print()
  print("done")


if __name__ == "__main__":
  main()
