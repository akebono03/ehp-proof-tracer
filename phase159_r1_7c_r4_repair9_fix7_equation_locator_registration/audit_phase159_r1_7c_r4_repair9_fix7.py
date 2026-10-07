from __future__ import annotations

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  _infer_toda_group_proof_literature_reference_from_rule_name,
)
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
  get_toda_fixed_statement_components,
)


def _render_group(
  n: int,
  k: int,
) -> str:
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

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def main() -> int:
  reference = (
    _infer_toda_group_proof_literature_reference_from_rule_name(
      "Toda Equation 5.7 nu-prime eta_6 Hopf value"
    )
  )

  print(
    "=== inferred Equation locator ==="
  )
  print(
    "locator=",
    None
    if reference is None
    else reference.locator,
    sep="",
  )

  print(
    "=== boundary catalog ==="
  )
  for locator in (
    "(5.7)",
    "(5.8)",
    "(5.13)",
  ):
    components = get_toda_fixed_statement_components(
      locator
    )
    print(
      locator,
      "=",
      tuple(
        component.component_key
        for component in components
      ),
      sep="",
    )

  rendered = _render_group(
    3,
    3,
  )
  reference_section = rendered.split(
    "---",
    1,
  )[0]

  print(
    "=== pi_6^3 Reference headers ==="
  )
  for line in reference_section.splitlines():
    if line.startswith(
      "**[R"
    ):
      print(
        line
      )

  print(
    "has_parenthesized_57=",
    int(
      "(5.7).**"
      in reference_section
    ),
    sep="",
  )
  print(
    "has_equation_word_57=",
    int(
      "Equation 5.7"
      in reference_section
    ),
    sep="",
  )

  return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
