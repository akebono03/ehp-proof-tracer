from pathlib import Path
import sys

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(0, str(REPO_ROOT))

from toda_calculation_facade import build_standard_toda_report
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown

import toda_group_proof_narrative_contribution_renderer as contribution_renderer


TRACE_NAMES = (
  "build_toda_group_proof_narrative_reference_entries",
  "filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary",
  "exclude_toda_group_proof_narrative_root_reference",
  "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage",
  "filter_toda_group_proof_narrative_reference_entries_by_body_usage",
  "filter_toda_group_proof_narrative_reference_entries_by_step_usage",
  "render_toda_group_proof_narrative_reference_entries_markdown",
)


def _entry_locators(value):
  if isinstance(value, tuple):
    locators = []
    for item in value:
      reference = getattr(item, "reference", None)
      locator = getattr(reference, "locator", None)
      if locator is not None:
        locators.append(locator)
    return tuple(locators)

  return ()


def _describe_result(value):
  if isinstance(value, tuple):
    direct = _entry_locators(value)
    if direct:
      return f"entries={direct}"

    if value:
      first = value[0]
      nested = _entry_locators(first)
      if nested:
        return f"entries={nested}"

    return f"tuple(len={len(value)})"

  if isinstance(value, str):
    headers = []
    for line in value.splitlines():
      if line.startswith("**[R"):
        headers.append(line)
    return f"str(len={len(value)}, headers={tuple(headers)})"

  return type(value).__name__


def _wrap(name):
  original = getattr(
    contribution_renderer,
    name,
    None,
  )

  if original is None:
    print(
      f"TRACE {name}: not present in contribution renderer"
    )
    return

  def wrapper(*args, **kwargs):
    before = ()

    if args:
      before = _entry_locators(
        args[0]
      )

    print()
    print(
      f"TRACE ENTER {name}"
    )
    if before:
      print(
        "  input entries:",
        before,
      )

    result = original(
      *args,
      **kwargs,
    )

    print(
      f"TRACE EXIT  {name}"
    )
    print(
      "  result:",
      _describe_result(
        result
      ),
    )

    return result

  setattr(
    contribution_renderer,
    name,
    wrapper,
  )


def _print_public_reference(rendered):
  print()
  print(
    "=" * 78
  )
  print(
    "Final public Reference section"
  )
  print(
    "=" * 78
  )

  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  if reference_header not in rendered:
    print(
      "NO REFERENCE SECTION"
    )
    return

  start = rendered.index(
    reference_header
  )

  if proof_header in rendered[
    start:
  ]:
    end = rendered.index(
      proof_header,
      start,
    )
  else:
    end = len(
      rendered
    )

  print(
    rendered[
      start:end
    ].rstrip()
  )


def main():
  for name in TRACE_NAMES:
    _wrap(
      name
    )

  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )

  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  print(
    "=" * 78
  )
  print(
    "Phase 161-R2 / pi_4^2 Reference pipeline trace"
  )
  print(
    "=" * 78
  )
  print(
    "root rule:",
    getattr(
      getattr(
        presentation.root_step,
        "inference_rule",
        None,
      ),
      "name",
      None,
    ),
  )

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  _print_public_reference(
    rendered
  )

  print()
  print(
    "=" * 78
  )
  print(
    "Final diagnostics"
  )
  print(
    "=" * 78
  )
  print(
    "(5.2) present:",
    "(5.2)" in rendered,
  )
  print(
    "Proposition 4.4 present:",
    "Proposition 4.4" in rendered,
  )
  print(
    "eta2 composition isomorphism body present:",
    (
      r"\eta_{2}\circ -"
      in rendered
    ),
  )
  print(
    "AUDIT COMPLETE"
  )
  print(
    "Production code changes: none"
  )


if __name__ == "__main__":
  main()
