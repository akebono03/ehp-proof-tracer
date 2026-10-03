from pathlib import Path
import sys


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
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
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


def _raw_presentation():
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


def _generic_render(
  presentation,
):
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
  return (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def _presence(
  markdown: str,
):
  return {
    label: tuple(
      number
      for number, line in enumerate(
        markdown.splitlines(),
        start=1,
      )
      if fragment in line
    )
    for label, fragment in TARGETS
  }


def _print_stage(
  name: str,
  presentation,
  markdown: str,
):
  print()
  print(name)
  print("-" * len(name))
  print(
    f"nodes={len(presentation.nodes)} "
    f"edges={len(presentation.edges)} "
    f"chars={len(markdown)}"
  )
  for label, lines in _presence(
    markdown
  ).items():
    print(
      f"  {label}: "
      f"present={bool(lines)} "
      f"lines={lines}"
    )


def main():
  raw = _raw_presentation()
  closure1 = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  closure2 = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      closure1
    )
  )

  generic1 = _generic_render(
    closure1
  )
  generic2 = _generic_render(
    closure2
  )

  public_from_raw = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )
  public_from_closure1 = (
    render_toda_group_proof_narrative_markdown(
      closure1
    )
  )

  print("=" * 78)
  print("Phase157 R11-R4 - semantic closure idempotency/origin audit")
  print("=" * 78)

  _print_stage(
    "generic after one closure",
    closure1,
    generic1,
  )
  _print_stage(
    "generic after two closures",
    closure2,
    generic2,
  )
  _print_stage(
    "public renderer from raw presentation",
    raw,
    public_from_raw,
  )
  _print_stage(
    "public renderer from already-closed presentation",
    closure1,
    public_from_closure1,
  )

  print()
  print("closure identity")
  print("----------------")
  print(
    "same node count: "
    + str(
      len(
        closure1.nodes
      )
      == len(
        closure2.nodes
      )
    )
  )
  print(
    "same edge count: "
    + str(
      len(
        closure1.edges
      )
      == len(
        closure2.edges
      )
    )
  )
  print(
    "generic outputs equal: "
    + str(
      generic1
      == generic2
    )
  )
  print(
    "public raw/closed outputs equal: "
    + str(
      public_from_raw
      == public_from_closure1
    )
  )

  output_dir = PACKAGE_DIR / "output"
  output_dir.mkdir(
    exist_ok=True
  )

  outputs = (
    (
      "01_generic_closure1.md",
      generic1,
    ),
    (
      "02_generic_closure2.md",
      generic2,
    ),
    (
      "03_public_from_raw.md",
      public_from_raw,
    ),
    (
      "04_public_from_closure1.md",
      public_from_closure1,
    ),
  )

  for filename, markdown in outputs:
    (
      output_dir
      / filename
    ).write_text(
      markdown,
      encoding="utf-8",
    )

  print()
  print("done")


if __name__ == "__main__":
  main()
