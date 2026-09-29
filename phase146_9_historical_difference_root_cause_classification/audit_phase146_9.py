from __future__ import annotations

from collections import Counter
from pathlib import Path
import inspect
import re
import sys

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
try:
  from toda_group_proof_narrative_exactness_method_selection import (
    select_toda_group_proof_narrative_primary_exactness_component,
  )
except ImportError:
  from toda_group_proof_narrative_argument_method import (
    select_toda_group_proof_narrative_primary_exactness_component,
  )
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_purpose_sentence,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)

PHASE146_8_REPORT = Path(sys.argv[1])
OUT = Path(sys.argv[2])


def role_name(value) -> str:
  return getattr(value, "value", str(value))


def block_role_name(block) -> str:
  return role_name(block.role)


def safe_component_windows(component) -> int:
  if component is None:
    return 0
  return len(getattr(component, "windows", ()))


def source_contains(function, needle: str) -> bool:
  return needle in inspect.getsource(function)


def count_report_value(label: str, report: str) -> int | None:
  match = re.search(
    rf"^- {re.escape(label)}: (\d+)$",
    report,
    re.MULTILINE,
  )
  if match is None:
    return None
  return int(match.group(1))


def main() -> None:
  report_text = PHASE146_8_REPORT.read_text(
    encoding="utf-8",
  )

  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  connected_markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  argument_rows = []
  for index, argument in enumerate(arguments):
    method_evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        index,
      )
    )
    components = (
      build_toda_group_proof_narrative_exactness_method_components(
        presentation,
        method_evidence,
      )
    )
    primary = (
      select_toda_group_proof_narrative_primary_exactness_component(
        argument,
        components,
      )
    )
    contributions = ordered_contributions[index]
    argument_rows.append(
      {
        "index": index,
        "role": role_name(argument.role),
        "purpose": (
          render_toda_group_proof_narrative_argument_purpose_sentence(
            argument
          )
        ),
        "supporting_roles": tuple(
          block_role_name(block)
          for block in argument.supporting_blocks
        ),
        "method_evidence": len(method_evidence),
        "components": len(components),
        "primary": primary is not None,
        "primary_windows": safe_component_windows(primary),
        "contributions": len(contributions),
        "placements": Counter(
          role_name(contribution.placement)
          for contribution in contributions
        ),
      }
    )

  order_row = next(
    row
    for row in argument_rows
    if row["role"] == "establish_order"
  )
  group_row = next(
    row
    for row in argument_rows
    if row["role"] == "establish_group_structure"
  )

  phase146_8_counts = {
    key: count_report_value(key, report_text)
    for key in (
      "historical units",
      "current units",
      "PRESERVED",
      "LOST",
      "ADDED",
      "MOVED",
      "DUPLICATED",
      "REWORDED",
      "UNMATCHED",
    )
  }

  exactness_match = re.search(
    r"- historical sequence-related units: (\d+).*?"
    r"- current sequence-related units: (\d+)",
    report_text,
    re.DOTALL,
  )
  reference_match = re.search(
    r"- historical \[R#\] units: (\d+).*?"
    r"- current \[R#\] units: (\d+)",
    report_text,
    re.DOTALL,
  )

  root_causes = [
    (
      "RC1",
      "Argument-method ownership is narrower than historical proof-purpose ownership",
      "Phase 146-7 purpose fusion works only when a primary exactness component "
      "is selected. The order argument and group-structure argument differ at "
      "the method-evidence/component/primary-selection layer.",
      (
        "4. order argument と主要 EHP 完全列の ownership",
        "5. EHP exact-sequence method introduction (partly)",
      ),
    ),
    (
      "RC2",
      "Recursive exactness evidence is exposed as body/contribution material",
      "Exactness evidence not absorbed as the primary method remains eligible "
      "for body/contribution rendering. This explains the large increase in "
      "sequence-related material and is upstream of much of the visible noise.",
      (
        "6. 主要完全列の適切な範囲選択",
        "7. 補助完全列の本文抑制",
        "8. 重複 contribution の一部",
      ),
    ),
    (
      "RC3",
      "Contribution ownership/insertion is separate from argument dependency narration",
      "The connected renderer first renders arguments and then inserts selected "
      "contributions around anchors. Therefore facts can be mathematically "
      "available yet appear outside the historical explanatory position.",
      (
        "8. 重複 contribution の一部",
        "9. dependency order に沿った式配置",
        "10. map-property chain の配置",
        "11. short exact sequence → group structure の順序",
      ),
    ),
    (
      "RC4",
      "Historical provenance/reason prose is not reconstructed from generic provenance",
      "Current reference presentation preserves compact references, but the "
      "historical '[R#] の n=... の場合より' derivation prose is not generally "
      "reconstructed.",
      (
        "1. Reference section の詳細",
        "2. Reference → derived fact の理由付け",
        "3. definition argument の理由文章の一部",
      ),
    ),
    (
      "RC5",
      "Exactness semantic type is rendered generically rather than as an EHP-named method",
      "The generic transition says '次の完全列を考える' and does not encode the "
      "historical EHP family name.",
      (
        "5. EHP exact sequence の semantic naming",
      ),
    ),
    (
      "RC6",
      "Equation numbering is downstream of the selected/ordered narrative stream",
      "Because selection and ordering differ from the historical proof, equation "
      "numbering also differs. This should be repaired after RC1-RC5 rather than "
      "with target-specific tag rules.",
      (
        "12. equation numbering / prose formatting",
      ),
    ),
  ]

  lines = [
    "# Phase 146-9 Historical Difference Root-Cause Classification",
    "",
    "## Scope",
    "",
    "Production changes: none.",
    "",
    "This audit groups the Phase 146-8 visible differences by internal cause. "
    "It does not treat every LOST/ADDED unit as an independent bug.",
    "",
    "## Phase 146-8 baseline",
    "",
  ]
  for key, value in phase146_8_counts.items():
    lines.append(f"- {key}: {value}")

  if exactness_match is not None:
    lines.extend(
      (
        f"- sequence-related units: historical {exactness_match.group(1)} / current {exactness_match.group(2)}",
      )
    )
  if reference_match is not None:
    lines.extend(
      (
        f"- [R#] units: historical {reference_match.group(1)} / current {reference_match.group(2)}",
      )
    )

  lines.extend(
    (
      "",
      "## Current pi_6^3 argument diagnostics",
      "",
      "| index | role | method evidence | components | primary | primary windows | contributions |",
      "| ---: | --- | ---: | ---: | --- | ---: | ---: |",
    )
  )

  for row in argument_rows:
    lines.append(
      "| "
      + str(row["index"])
      + " | "
      + row["role"]
      + " | "
      + str(row["method_evidence"])
      + " | "
      + str(row["components"])
      + " | "
      + ("yes" if row["primary"] else "no")
      + " | "
      + str(row["primary_windows"])
      + " | "
      + str(row["contributions"])
      + " |"
    )

  lines.extend(
    (
      "",
      "### Order argument",
      "",
      f"- purpose: {order_row['purpose']}",
      f"- supporting roles: {order_row['supporting_roles']}",
      f"- primary exactness component: {order_row['primary']}",
      f"- contributions: {order_row['contributions']}",
      "",
      "### Group-structure argument",
      "",
      f"- purpose: {group_row['purpose']}",
      f"- supporting roles: {group_row['supporting_roles']}",
      f"- primary exactness component: {group_row['primary']}",
      f"- contributions: {group_row['contributions']}",
      "",
      "## Renderer-layer evidence",
      "",
      f"- base multi-argument chars: {len(base_markdown)}",
      f"- contribution-connected chars: {len(connected_markdown)}",
      f"- contribution renderer changes output: {base_markdown != connected_markdown}",
      "- argument builder uses direct dependency indices: "
      + str(
        source_contains(
          __import__("toda_group_proof_narrative_arguments")
          .build_toda_group_proof_narrative_arguments,
          "_argument_direct_dependency_indices",
        )
      ),
      "- contribution renderer performs post-render insertion: "
      + str(
        source_contains(
          render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
          "_insert_toda_group_proof_narrative_argument_contributions",
        )
      ),
      "",
      "## Root-cause classification",
      "",
    )
  )

  for code, title, evidence, symptoms in root_causes:
    lines.extend(
      (
        f"### {code}: {title}",
        "",
        evidence,
        "",
        "Mapped Phase 146-8 differences:",
      )
    )
    for symptom in symptoms:
      lines.append(f"- {symptom}")
    lines.append("")

  lines.extend(
    (
      "## Consolidated result",
      "",
      f"- visible difference families from Phase 146-8: 12",
      f"- root-cause families after consolidation: {len(root_causes)}",
      "",
      "Recommended dependency order:",
      "",
      "RC1 → RC2 → RC3 → RC4 → RC5 → RC6",
      "",
      "RC6 is intentionally last because numbering/formatting is downstream of "
      "selection and ordering. RC5 may be implemented independently after RC1 "
      "if desired, but should not be used to hide ownership defects.",
      "",
      "## Boundary",
      "",
      "This audit does not change route gates, exactness ownership, contribution "
      "selection, provenance rendering, EHP naming, or equation numbering.",
    )
  )

  OUT.write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8",
  )

  print("=" * 78)
  print("Phase 146-9 Historical Difference Root-Cause Classification")
  print("=" * 78)
  for row in argument_rows:
    print(
      f"arg {row['index']} {row['role']}: "
      f"method_evidence={row['method_evidence']} "
      f"components={row['components']} "
      f"primary={row['primary']} "
      f"primary_windows={row['primary_windows']} "
      f"contributions={row['contributions']}"
    )
  print()
  print("Phase 146-8 visible difference families: 12")
  print("Consolidated root-cause families:", len(root_causes))
  print("Recommended order: RC1 -> RC2 -> RC3 -> RC4 -> RC5 -> RC6")
  print()
  print("Report:", OUT)
  print("Production changes: none")


if __name__ == "__main__":
  main()
