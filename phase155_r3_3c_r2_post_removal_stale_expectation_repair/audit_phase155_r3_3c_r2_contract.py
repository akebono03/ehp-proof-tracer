
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _render(
  n: int,
  k: int,
) -> str:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def collect_contract() -> dict:
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
      max_depth=2,
      mode="narrative",
    )
  )

  latex_values = tuple(
    line.statement_latex
    for line in view.rendered_lines
    if line.statement_latex is not None
  )

  pi6_rendered = _render(
    3,
    3,
  )
  pi8_rendered = _render(
    5,
    3,
  )

  return {
    "pi16_9_math_present": (
      r"\pi_{16}^{9} = "
      r"\mathbb{Z}/16\{\sigma_{9}\}"
      in latex_values
    ),
    "pi16_9_source_theorem": view.theorem,
    "pi16_9_root_theorem_in_rendered_prefix": any(
      "Proposition 5.15" in line.prefix
      for line in view.rendered_lines
    ),
    "pi6_ascii_connector_present": (
      "以上より, " in pi6_rendered
    ),
    "pi6_japanese_connector_present": (
      "以上より、" in pi6_rendered
    ),
    "pi8_ascii_connector_present": (
      "以上より, " in pi8_rendered
    ),
    "pi8_japanese_connector_present": (
      "以上より、" in pi8_rendered
    ),
  }


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output",
    type=Path,
    default=Path(
      "phase155_r3_3c_r2_contract_audit.json"
    ),
  )
  args = parser.parse_args()

  result = collect_contract()
  args.output.write_text(
    json.dumps(
      result,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  for key, value in result.items():
    print(
      key + ":",
      value,
    )

  expected = {
    "pi16_9_math_present": True,
    "pi16_9_source_theorem": "Toda Proposition 5.15",
    "pi16_9_root_theorem_in_rendered_prefix": False,
    "pi6_ascii_connector_present": True,
    "pi6_japanese_connector_present": False,
    "pi8_ascii_connector_present": True,
    "pi8_japanese_connector_present": False,
  }

  if result != expected:
    print(
      "Current runtime contract differs from the R3-3C-r2 repair assumption."
    )
    return 2

  print(
    "Current runtime contract matches the R3-3C-r2 repair assumption."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
