from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
)


def _render_toda_group_proof_narrative_exactness_map_symbol_latex(
  map_symbol,
) -> str:
  names = {
    "E": "E",
    "H": "H",
    "Δ": r"\Delta",
  }

  name = getattr(
    map_symbol,
    "name",
    None,
  )

  if (
    not isinstance(
      name,
      str,
    )
    or name not in names
  ):
    raise TypeError(
      "unsupported EXACTNESS map symbol"
    )

  return names[
    name
  ]


def render_toda_group_proof_narrative_exactness_method_component_latex(
  component: TodaGroupProofNarrativeExactnessMethodComponent,
) -> str:
  if not isinstance(
    component,
    TodaGroupProofNarrativeExactnessMethodComponent,
  ):
    raise TypeError(
      "component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent"
    )

  first_window = component.windows[
    0
  ]

  latex = (
    render_toda_primary_group_latex(
      first_window.source_term
    )
    + r" \xrightarrow{"
    + _render_toda_group_proof_narrative_exactness_map_symbol_latex(
      first_window.first_map
    )
    + "} "
    + render_toda_primary_group_latex(
      first_window.middle_term
    )
    + r" \xrightarrow{"
    + _render_toda_group_proof_narrative_exactness_map_symbol_latex(
      first_window.second_map
    )
    + "} "
    + render_toda_primary_group_latex(
      first_window.target_term
    )
  )

  for window in component.windows[
    1:
  ]:
    latex += (
      r" \xrightarrow{"
      + _render_toda_group_proof_narrative_exactness_map_symbol_latex(
        window.second_map
      )
      + "} "
      + render_toda_primary_group_latex(
        window.target_term
      )
    )

  return latex
