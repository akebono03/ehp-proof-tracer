from pathlib import Path
import inspect
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


import toda_group_proof_narrative_contribution_renderer as contribution_renderer
import toda_group_proof_narrative_renderer as narrative_renderer

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _phase154_r5_reference_source_steps_by_number,
  _phase154_r5_unique_visible_non_root_consumer_line,
  link_toda_group_proof_narrative_reference_body_consumers,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
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


def main():
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  sources_by_number = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      entries,
    )
  )

  print(
    "=" * 78
  )
  print(
    "Phase 161-R4-R5 repair8 active-helper audit"
  )
  print(
    "=" * 78
  )

  print()
  print(
    "[Active helper identity]"
  )
  helper = (
    contribution_renderer
    .link_toda_group_proof_narrative_reference_body_consumers
  )
  imported_helper = (
    narrative_renderer
    .link_toda_group_proof_narrative_reference_body_consumers
  )

  print(
    "contribution helper file:",
    inspect.getsourcefile(
      helper
    ),
  )
  print(
    "contribution helper line:",
    inspect.getsourcelines(
      helper
    )[1],
  )
  print(
    "narrative imported helper file:",
    inspect.getsourcefile(
      imported_helper
    ),
  )
  print(
    "narrative imported helper line:",
    inspect.getsourcelines(
      imported_helper
    )[1],
  )
  print(
    "same function object:",
    helper is imported_helper,
  )

  print()
  print(
    "[Active helper source]"
  )
  print(
    inspect.getsource(
      helper
    )
  )

  prop51_entry = next(
    entry
    for entry in entries
    if (
      entry.reference.locator
      == "Proposition 5.1"
      and entry.number == 3
    )
  )
  prop51_sources = sources_by_number[
    prop51_entry.number
  ]

  synthetic_body = (
    "$\\pi_{4}^{2}$ の群構造を決定する.\n\n"
    "$\\pi_{4}^{3} = "
    "\\mathbb{Z}/2\\{\\eta_{3}\\}$\n\n"
    "[R3]より, "
    "$\\pi_{n + 1}^{n} = "
    "\\mathbb{Z}/2\\{\\eta_{n}\\}$.\n\n"
    "[R1]を $i=4$ に適用すると, "
    "$\\eta_{2}\\circ -: "
    "\\pi_{4}^{3} \\to \\pi_{4}^{2}$ は同型である."
  )

  consumer = (
    _phase154_r5_unique_visible_non_root_consumer_line(
      presentation,
      prop51_sources,
      synthetic_body,
    )
  )

  print()
  print(
    "[Direct R3 consumer lookup]"
  )
  print(
    "consumer:",
    repr(
      consumer
    ),
  )

  print()
  print(
    "[Synthetic body BEFORE]"
  )
  print(
    synthetic_body
  )

  directly_linked = (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      synthetic_body,
      entries,
    )
  )

  print()
  print(
    "[Synthetic body AFTER helper]"
  )
  print(
    directly_linked
  )

  print()
  print(
    "[Direct diagnostics]"
  )
  print(
    "general R3 remains:",
    (
      "[R3]より, "
      "$\\pi_{n + 1}^{n}"
      in directly_linked
    ),
  )
  print(
    "R3 moved to pi_4^3:",
    (
      "[R3]より, "
      "$\\pi_{4}^{3} = "
      "\\mathbb{Z}/2\\{\\eta_{3}\\}$"
      in directly_linked
    ),
  )

  print()
  print(
    "[Full public render]"
  )
  rendered = (
    narrative_renderer
    .render_toda_group_proof_narrative_markdown(
      raw
    )
  )
  print(
    rendered
  )

  print()
  print(
    "Audit completed. Production changes: NONE"
  )


if __name__ == "__main__":
  main()
