from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  MapSymbol,
  Multiple,
  ScalarPower,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  SmashProduct,
  Sum,
  Suspension,
  TodaBracket,
  WhiteheadProduct,
  Zero,
)
from toda_end_to_end_presentation import (
  TodaEndToEndCandidatePresentation,
)
from toda_ehp_presentation import (
  TodaEHPSequencePresentation,
)
from toda_presentation import (
  TodaGroupResultPresentation,
  TodaGroupStructureKind,
  TodaGroupStructurePresentation,
  TodaTargetPresentation,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
)


_GREEK_LATEX = {
  "η": r"\eta",
  "ν": r"\nu",
  "σ": r"\sigma",
  "ι": r"\iota",
  "Δ": r"\Delta",
}

_SUBSCRIPT_DIGITS = {
  "₀": "0",
  "₁": "1",
  "₂": "2",
  "₃": "3",
  "₄": "4",
  "₅": "5",
  "₆": "6",
  "₇": "7",
  "₈": "8",
  "₉": "9",
}

_SUPERSCRIPT_DIGITS = {
  "⁰": "0",
  "¹": "1",
  "²": "2",
  "³": "3",
  "⁴": "4",
  "⁵": "5",
  "⁶": "6",
  "⁷": "7",
  "⁸": "8",
  "⁹": "9",
}

_PRIME_CHARS = {
  "'",
  "′",
  "″",
  "‴",
}

_ROLE_LABELS = {
  TodaProofDependencyRole.EHP_EXACTNESS: "EHP exactness",
  TodaProofDependencyRole.EHP_WINDOW: "EHP window",
  TodaProofDependencyRole.GROUP_STRUCTURE: "group structure",
  TodaProofDependencyRole.RELATION: "relation",
  TodaProofDependencyRole.ORDER: "order",
  TodaProofDependencyRole.MAP_PROPERTY: "map property",
  TodaProofDependencyRole.DEFINITION: "definition",
  TodaProofDependencyRole.LITERATURE: "literature",
  TodaProofDependencyRole.OTHER: "other",
}


def _render_unicode_math_name_latex(
  name: str,
) -> str:
  if not isinstance(
    name,
    str,
  ):
    raise TypeError(
      "name must be a str"
    )

  if not name:
    raise ValueError(
      "name must not be empty"
    )

  pieces: list[str] = []
  subscript_digits: list[str] = []
  superscript_digits: list[str] = []
  prime_count = 0

  def flush_scripts() -> None:
    nonlocal subscript_digits
    nonlocal superscript_digits

    if subscript_digits:
      pieces.append(
        "_{"
        + "".join(
          subscript_digits
        )
        + "}"
      )
      subscript_digits = []

    if superscript_digits:
      pieces.append(
        "^{"
        + "".join(
          superscript_digits
        )
        + "}"
      )
      superscript_digits = []

  for character in name:
    if character in _SUBSCRIPT_DIGITS:
      subscript_digits.append(
        _SUBSCRIPT_DIGITS[
          character
        ]
      )
      continue

    if character in _SUPERSCRIPT_DIGITS:
      superscript_digits.append(
        _SUPERSCRIPT_DIGITS[
          character
        ]
      )
      continue

    if character in _PRIME_CHARS:
      flush_scripts()

      if character == "″":
        prime_count += 2
      elif character == "‴":
        prime_count += 3
      else:
        prime_count += 1
      continue

    flush_scripts()

    pieces.append(
      _GREEK_LATEX.get(
        character,
        character,
      )
    )

  flush_scripts()

  if prime_count:
    pieces.append(
      "'" * prime_count
    )

  return "".join(
    pieces
  )


def _render_scalar_latex(
  value,
) -> str:
  if isinstance(
    value,
    bool,
  ):
    raise TypeError(
      "scalar bool is not supported"
    )

  if isinstance(
    value,
    int,
  ):
    return str(
      value
    )

  if isinstance(
    value,
    ScalarSymbol,
  ):
    return _render_unicode_math_name_latex(
      value.name
    )

  if isinstance(
    value,
    ScalarSum,
  ):
    if (
      isinstance(
        value.right,
        int,
      )
      and not isinstance(
        value.right,
        bool,
      )
      and value.right < 0
    ):
      return (
        _render_scalar_latex(
          value.left
        )
        + " - "
        + _render_scalar_latex(
          -value.right
        )
      )

    if (
      isinstance(
        value.right,
        ScalarProduct,
      )
      and value.right.left == -1
    ):
      return (
        _render_scalar_latex(
          value.left
        )
        + " - "
        + _render_scalar_latex(
          value.right.right
        )
      )

    return (
      _render_scalar_latex(
        value.left
      )
      + " + "
      + _render_scalar_latex(
        value.right
      )
    )

  if isinstance(
    value,
    ScalarProduct,
  ):
    return (
      _render_scalar_latex(
        value.left
      )
      + r"\,"
      + _render_scalar_latex(
        value.right
      )
    )

  if isinstance(
    value,
    ScalarPower,
  ):
    return (
      "{"
      + _render_scalar_latex(
        value.base
      )
      + "}^{"
      + _render_scalar_latex(
        value.exponent
      )
      + "}"
    )

  raise TypeError(
    "unsupported scalar value for LaTeX rendering"
  )


def _render_generator_symbol_latex(
  symbol: GeneratorSymbol,
) -> str:
  if not isinstance(
    symbol,
    GeneratorSymbol,
  ):
    raise TypeError(
      "symbol must be a GeneratorSymbol"
    )

  latex = (
    _render_unicode_math_name_latex(
      symbol.family
    )
  )

  if symbol.index is not None:
    latex += (
      "_{"
      + _render_scalar_latex(
        symbol.index
      )
      + "}"
    )

  if symbol.decoration is not None:
    latex += (
      _render_unicode_math_name_latex(
        symbol.decoration
      )
    )

  return latex


def _render_map_symbol_latex(
  map_symbol: MapSymbol,
) -> str:
  if not isinstance(
    map_symbol,
    MapSymbol,
  ):
    raise TypeError(
      "map_symbol must be a MapSymbol"
    )

  return _render_unicode_math_name_latex(
    map_symbol.name
  )


def render_toda_expression_latex(
  expression,
) -> str:
  if isinstance(
    expression,
    Zero,
  ):
    return "0"

  if isinstance(
    expression,
    HomotopyElement,
  ):
    if expression.generator is not None:
      return (
        _render_generator_symbol_latex(
          expression.generator
        )
      )

    return (
      _render_unicode_math_name_latex(
        expression.name
      )
    )

  if isinstance(
    expression,
    Multiple,
  ):
    if expression.coefficient == -1:
      return (
        "-"
        + render_toda_expression_latex(
          expression.expression
        )
      )

    coefficient = (
      _render_scalar_latex(
        expression.coefficient
      )
    )

    return (
      coefficient
      + render_toda_expression_latex(
        expression.expression
      )
    )

  if isinstance(
    expression,
    Sum,
  ):
    left_latex = (
      render_toda_expression_latex(
        expression.left
      )
    )

    if (
      isinstance(
        expression.right,
        Multiple,
      )
      and isinstance(
        expression.right.coefficient,
        int,
      )
      and not isinstance(
        expression.right.coefficient,
        bool,
      )
      and expression.right.coefficient < 0
    ):
      magnitude = -expression.right.coefficient

      right_latex = (
        render_toda_expression_latex(
          expression.right.expression
        )
      )

      if magnitude != 1:
        right_latex = (
          str(
            magnitude
          )
          + right_latex
        )

      return (
        left_latex
        + " - "
        + right_latex
      )

    return (
      left_latex
      + " + "
      + render_toda_expression_latex(
        expression.right
      )
    )

  if isinstance(
    expression,
    SmashProduct,
  ):
    return (
      render_toda_expression_latex(
        expression.left
      )
      + r" \wedge "
      + render_toda_expression_latex(
        expression.right
      )
    )

  if isinstance(
    expression,
    WhiteheadProduct,
  ):
    return (
      "["
      + render_toda_expression_latex(
        expression.left
      )
      + ", "
      + render_toda_expression_latex(
        expression.right
      )
      + "]"
    )

  if isinstance(
    expression,
    Composition,
  ):
    return (
      render_toda_expression_latex(
        expression.left
      )
      + render_toda_expression_latex(
        expression.right
      )
    )

  if isinstance(
    expression,
    MapApplication,
  ):
    return (
      _render_map_symbol_latex(
        expression.map
      )
      + r"\left("
      + render_toda_expression_latex(
        expression.expression
      )
      + r"\right)"
    )

  if isinstance(
    expression,
    Suspension,
  ):
    return (
      "E"
      + render_toda_expression_latex(
        expression.expression
      )
    )

  if isinstance(
    expression,
    IteratedSuspension,
  ):
    return (
      "E^{"
      + _render_scalar_latex(
        expression.exponent
      )
      + "}"
      + render_toda_expression_latex(
        expression.expression
      )
    )

  if isinstance(
    expression,
    TodaBracket,
  ):
    latex = (
      r"\{"
      + render_toda_expression_latex(
        expression.first
      )
      + ", "
      + render_toda_expression_latex(
        expression.second
      )
      + ", "
      + render_toda_expression_latex(
        expression.third
      )
      + r"\}"
    )

    if expression.index is not None:
      latex += (
        "_{"
        + _render_scalar_latex(
          expression.index
        )
        + "}"
      )

    return latex

  raise TypeError(
    "unsupported expression for LaTeX rendering"
  )


def render_toda_target_latex(
  target: TodaTargetPresentation,
) -> str:
  if not isinstance(
    target,
    TodaTargetPresentation,
  ):
    raise TypeError(
      "target must be a "
      "TodaTargetPresentation"
    )

  return (
    r"\pi_{"
    + _render_scalar_latex(
      target.group_dimension
    )
    + "}^{"
    + _render_scalar_latex(
      target.sphere_dimension
    )
    + "}"
  )


def render_toda_group_structure_latex(
  group_structure: TodaGroupStructurePresentation,
) -> str:
  if not isinstance(
    group_structure,
    TodaGroupStructurePresentation,
  ):
    raise TypeError(
      "group_structure must be a "
      "TodaGroupStructurePresentation"
    )

  if (
    group_structure.kind
    is TodaGroupStructureKind.ZERO
  ):
    return "0"

  if (
    group_structure.kind
    is TodaGroupStructureKind.FREE_CYCLIC
  ):
    return (
      r"\mathbb{Z}\{"
      + render_toda_expression_latex(
        group_structure
        .generator
        .source_generator
      )
      + r"\}"
    )

  if (
    group_structure.kind
    is TodaGroupStructureKind.FINITE_CYCLIC
  ):
    return (
      r"\mathbb{Z}/"
      + str(
        group_structure
        .generator
        .order
        .value
      )
      + r"\{"
      + render_toda_expression_latex(
        group_structure
        .generator
        .source_generator
      )
      + r"\}"
    )

  if (
    group_structure.kind
    is TodaGroupStructureKind.DIRECT_SUM
  ):
    return r" \oplus ".join(
      render_toda_group_structure_latex(
        summand
      )
      for summand in (
        group_structure.summands
      )
    )

  raise ValueError(
    "unsupported group structure kind"
  )


def render_toda_group_result_latex(
  group: TodaGroupResultPresentation,
) -> str:
  if not isinstance(
    group,
    TodaGroupResultPresentation,
  ):
    raise TypeError(
      "group must be a "
      "TodaGroupResultPresentation"
    )

  return (
    render_toda_target_latex(
      group.target
    )
    + r" \cong "
    + render_toda_group_structure_latex(
      group.group_structure
    )
  )


def render_toda_ehp_sequence_latex(
  sequence: TodaEHPSequencePresentation,
) -> str:
  if not isinstance(
    sequence,
    TodaEHPSequencePresentation,
  ):
    raise TypeError(
      "sequence must be a "
      "TodaEHPSequencePresentation"
    )

  pieces = [
    render_toda_target_latex(
      sequence.terms[
        0
      ]
    )
  ]

  for map_presentation, term in zip(
    sequence.maps,
    sequence.terms[
      1:
    ],
  ):
    pieces.append(
      (
        r"\xrightarrow{"
        + _render_map_symbol_latex(
          map_presentation.source_map
        )
        + "} "
        + render_toda_target_latex(
          term
        )
      )
    )

  return " ".join(
    pieces
  )


def _role_label(
  role: TodaProofDependencyRole,
) -> str:
  if not isinstance(
    role,
    TodaProofDependencyRole,
  ):
    raise TypeError(
      "role must be a "
      "TodaProofDependencyRole"
    )

  return _ROLE_LABELS[
    role
  ]


def _render_source_markdown(
  presentation: TodaEndToEndCandidatePresentation,
) -> tuple[
  str,
  ...,
]:
  goal_source = (
    presentation
    .source
    .goal_source
  )

  if goal_source is None:
    return (
      "- Discovery source: direct repository result",
    )

  repository_source = (
    goal_source.repository_source
  )

  lines = [
    (
      "- Phase: "
      + (
        repository_source.phase
        if repository_source.phase
        is not None
        else "unknown"
      )
    ),
    (
      "- Theorem: "
      + (
        repository_source.theorem
        if repository_source.theorem
        is not None
        else "unknown"
      )
    ),
    (
      "- Branch: `"
      + goal_source.branch_name
      + "`"
    ),
  ]

  return tuple(
    lines
  )


def _render_exactness_markdown(
  presentation: TodaEndToEndCandidatePresentation,
) -> tuple[
  str,
  ...,
]:
  if presentation.exactness is None:
    return (
      "No EHP exactness presentation is attached.",
    )

  lines: list[str] = []

  for index, use in enumerate(
    presentation.exactness.uses,
    start=1,
  ):
    window = use.window

    window_latex = (
      render_toda_target_latex(
        window.source_term
      )
      + r" \xrightarrow{"
      + _render_map_symbol_latex(
        window.first_map.source_map
      )
      + "} "
      + render_toda_target_latex(
        window.middle_term
      )
      + r" \xrightarrow{"
      + _render_map_symbol_latex(
        window.second_map.source_map
      )
      + "} "
      + render_toda_target_latex(
        window.target_term
      )
    )

    lines.append(
      (
        str(index)
        + ". $"
        + window_latex
        + "$"
        + " — direct consumers: "
        + str(
          len(
            use.consumer_steps
          )
        )
      )
    )

  return tuple(
    lines
  )


def _render_proof_flow_markdown(
  presentation: TodaEndToEndCandidatePresentation,
) -> tuple[
  str,
  ...,
]:
  lines: list[str] = []

  for index, node in enumerate(
    presentation.proof_flow.nodes,
    start=1,
  ):
    conclusion_type = (
      type(
        node.step.conclusion
      ).__name__
    )

    shared_suffix = ""

    if node.is_shared_dependency:
      shared_suffix = (
        " — shared dependency, used "
        + str(
          node.incoming_use_count
        )
        + " times"
      )

    lines.append(
      (
        str(index)
        + ". **"
        + _role_label(
          node.step.role
        )
        + "** — `"
        + conclusion_type
        + "`"
        + shared_suffix
      )
    )

  return tuple(
    lines
  )


def render_toda_end_to_end_markdown(
  presentation: TodaEndToEndCandidatePresentation,
) -> str:
  if not isinstance(
    presentation,
    TodaEndToEndCandidatePresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaEndToEndCandidatePresentation"
    )

  target_latex = (
    render_toda_target_latex(
      presentation.group.target
    )
  )

  lines = [
    (
      "# $"
      + target_latex
      + "$"
    ),
    "",
    "## Result",
    "",
    r"\[",
    render_toda_group_result_latex(
      presentation.group
    ),
    r"\]",
    "",
    "## Source",
    "",
    *_render_source_markdown(
      presentation
    ),
  ]

  if presentation.ehp is not None:
    lines.extend(
      (
        "",
        "## EHP sequence",
        "",
        r"\[",
        render_toda_ehp_sequence_latex(
          presentation.ehp
        ),
        r"\]",
      )
    )

  lines.extend(
    (
      "",
      "## Exactness",
      "",
      *_render_exactness_markdown(
        presentation
      ),
      "",
      "## Proof flow",
      "",
      *_render_proof_flow_markdown(
        presentation
      ),
    )
  )

  return "\n".join(
    lines
  ) + "\n"
