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
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
import toda_group_proof_narrative_contribution_renderer as contribution_renderer
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGETS = (
  (
    "unwanted_suspension_iso",
    r"$E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である.",
  ),
  (
    "needed_pi6_5_group",
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$",
  ),
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
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )


def _all_strings(value):
  if isinstance(
    value,
    str,
  ):
    return (
      value,
    )

  if isinstance(
    value,
    tuple,
  ):
    return tuple(
      text
      for item in value
      for text in _all_strings(
        item
      )
    )

  if isinstance(
    value,
    list,
  ):
    return tuple(
      text
      for item in value
      for text in _all_strings(
        item
      )
    )

  if isinstance(
    value,
    dict,
  ):
    return tuple(
      text
      for item in value.values()
      for text in _all_strings(
        item
      )
    )

  return ()


def _presence(
  values,
):
  strings = tuple(
    text
    for value in values
    for text in _all_strings(
      value
    )
  )

  return {
    label: any(
      fragment in text
      for text in strings
    )
    for label, fragment in TARGETS
  }


def _wrap(
  name,
):
  original = getattr(
    contribution_renderer,
    name,
    None,
  )

  if original is None:
    print(
      f"SKIP missing function: {name}"
    )
    return

  @wraps(
    original
  )
  def wrapper(
    *args,
    **kwargs,
  ):
    before = _presence(
      (
        args,
        kwargs,
      )
    )

    result = original(
      *args,
      **kwargs,
    )

    after = _presence(
      (
        result,
      )
    )

    transitions = tuple(
      (
        label,
        before[label],
        after[label],
      )
      for label, _ in TARGETS
      if (
        before[label]
        != after[label]
      )
    )

    print(
      f"{name}: "
      f"before={before} "
      f"after={after}"
    )

    for label, old, new in transitions:
      print(
        f"  TRANSITION {label}: "
        f"{old} -> {new}"
      )

    return result

  setattr(
    contribution_renderer,
    name,
    wrapper,
  )


def main():
  presentation = _presentation()
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )

  targets = (
    "render_toda_group_proof_narrative_multi_argument_markdown",
    "_insert_toda_group_proof_narrative_argument_contributions",
    "insert_toda_group_proof_narrative_reason_prose",
    "suppress_toda_group_proof_narrative_reference_internal_body",
    "suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry",
    "suppress_toda_group_proof_narrative_reference_body_duplicates",
    "link_toda_group_proof_narrative_reference_body_consumers",
    "normalize_toda_group_proof_narrative_connectors",
    "order_toda_group_proof_narrative_local_equation_derivations",
    "_phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism",
    "filter_toda_group_proof_narrative_reference_entries_by_body_usage",
    "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage",
  )

  print("=" * 78)
  print("Phase157 R11-R5 - generic stage transition audit")
  print("=" * 78)
  print(
    f"nodes={len(presentation.nodes)} "
    f"edges={len(presentation.edges)}"
  )
  print()

  for name in targets:
    _wrap(
      name
    )

  print()
  print("RUN generic renderer")
  print("--------------------")

  rendered = (
    contribution_renderer
    .render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  print()
  print("FINAL")
  print("-----")
  final_presence = _presence(
    (
      rendered,
    )
  )

  for label, present in final_presence.items():
    print(
      f"{label}: present={present}"
    )

  print()
  print("Target lines in final output")
  print("----------------------------")

  for number, line in enumerate(
    rendered.splitlines(),
    start=1,
  ):
    if any(
      fragment in line
      for _, fragment in TARGETS
    ):
      print(
        f"{number:04d}: {line}"
      )

  print()
  print("done")


if __name__ == "__main__":
  main()
