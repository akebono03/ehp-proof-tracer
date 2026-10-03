from pathlib import Path
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
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
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


def _presentation(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
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


def _proof_body(
  rendered: str,
) -> str:
  marker = "\n## 証明\n"
  if marker not in rendered:
    return rendered
  return rendered.split(
    marker,
    1,
  )[1]


def _print_numbered_lines(
  title: str,
  text: str,
) -> None:
  print()
  print(title)
  print("-" * len(title))
  for number, line in enumerate(
    text.splitlines(),
    start=1,
  ):
    print(
      f"{number:04d}: {line}"
    )


def _find_lines(
  text: str,
  patterns,
):
  hits = []
  for number, line in enumerate(
    text.splitlines(),
    start=1,
  ):
    for label, pattern in patterns:
      if re.search(
        pattern,
        line,
      ):
        hits.append(
          (
            number,
            label,
            line,
          )
        )
  return hits


def main() -> None:
  presentation = _presentation(
    3,
    3,
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )
  body = _proof_body(
    rendered
  )

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
  ordered = build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    sidecar,
    arguments,
  )

  print("=" * 78)
  print("Phase157 R11-R1 — proof body relevance audit")
  print("=" * 78)
  print("target: pi_6^3")
  print(f"rendered chars: {len(rendered)}")
  print(f"proof body chars: {len(body)}")
  print(f"arguments: {len(arguments)}")
  print(f"ordered contributions: {len(ordered)}")

  patterns = (
    (
      "pi4_2_to_pi5_3_map",
      r"pi_\{?4\}?\^\{?2\}?.*pi_\{?5\}?\^\{?3\}?",
    ),
    (
      "latex_pi4_2_to_pi5_3",
      r"\\pi_\{4\}\^\{2\}.*\\pi_\{5\}\^\{3\}",
    ),
    (
      "pi6_5_group",
      r"\\pi_\{6\}\^\{5\}",
    ),
    (
      "eta5_group",
      r"\\mathbb\{Z\}/2.*\\eta_\{5\}",
    ),
  )

  hits = _find_lines(
    body,
    patterns,
  )

  print()
  print("Matched proof-body lines")
  print("------------------------")
  if not hits:
    print("(no configured fragment matched)")
  else:
    for number, label, line in hits:
      print(
        f"{number:04d} [{label}] {line}"
      )

  print()
  print("Arguments")
  print("---------")
  for index, argument in enumerate(
    arguments,
  ):
    conclusion = getattr(
      argument,
      "conclusion_block",
      None,
    )
    conclusion_role = getattr(
      conclusion,
      "role",
      None,
    )
    print(
      f"A{index:02d}: "
      f"role={getattr(argument, 'role', None)} "
      f"conclusion_role={conclusion_role}"
    )

  print()
  print("Ordered contributions")
  print("---------------------")
  for index, contribution in enumerate(
    ordered,
  ):
    proof_step = contribution.proof_step
    conclusion = proof_step.conclusion
    rendered_conclusion = str(
      conclusion
    ).replace(
      "\n",
      " ",
    )
    if len(rendered_conclusion) > 220:
      rendered_conclusion = (
        rendered_conclusion[:217]
        + "..."
      )
    print(
      f"C{index:03d}: "
      f"owner=A{contribution.owner_argument_index:02d} "
      f"role={contribution.contribution_role.value} "
      f"placement={contribution.placement.value} "
      f"provider_anchor={contribution.provider_anchor} "
      f"distance={contribution.distance_to_conclusion} "
      f"type={type(conclusion).__name__} "
      f"value={rendered_conclusion}"
    )

  _print_numbered_lines(
    "Rendered proof body",
    body,
  )

  output_dir = (
    PACKAGE_DIR
    / "output"
  )
  output_dir.mkdir(
    exist_ok=True
  )
  (
    output_dir
    / "pi6_3_rendered.md"
  ).write_text(
    rendered,
    encoding="utf-8",
  )
  (
    output_dir
    / "pi6_3_body.md"
  ).write_text(
    body,
    encoding="utf-8",
  )

  print()
  print("Audit files written:")
  print(
    output_dir
    / "pi6_3_rendered.md"
  )
  print(
    output_dir
    / "pi6_3_body.md"
  )


if __name__ == "__main__":
  main()
