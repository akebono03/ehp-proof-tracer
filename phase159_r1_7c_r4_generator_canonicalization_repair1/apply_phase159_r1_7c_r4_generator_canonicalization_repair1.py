from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

PROD = ROOT / "toda_group_proof_generic_narrative_renderer.py"
STALE_TEST = ROOT / "tests" / "test_phase143_3_generic_eta_normalization.py"
NEW_TEST = ROOT / "tests" / "test_phase159_r1_7c_r4_generator_canonicalization_repair1.py"


OLD_TRY = '''def _try_render_generic_narrative_expression_latex(
  expression,
) -> str | None:
  try:
    return render_toda_expression_latex(
      expression
    )
  except TypeError:
    return None
'''


NEW_TRY = '''def _try_render_generic_narrative_expression_latex(
  expression,
) -> str | None:
  try:
    return render_toda_expression_latex(
      expression
    )
  except TypeError:
    return None


def _try_render_generic_narrative_group_structure_latex(
  group,
) -> str | None:
  try:
    return render_toda_raw_group_structure_latex(
      group
    )
  except (
    TypeError,
    ValueError,
  ):
    return None
'''


OLD_NORMALIZE = '''def _normalize_generic_narrative_statement_latex(
  statement,
  latex: str,
) -> str:
  if not isinstance(
    latex,
    str,
  ):
    raise TypeError(
      "latex must be a str"
    )

  if not hasattr(
    statement,
    "lhs",
  ):
    return (
      _normalize_generic_eta_family_latex(
        latex
      )
    )

  if not hasattr(
    statement,
    "rhs",
  ):
    return (
      _normalize_generic_eta_family_latex(
        latex
      )
    )

  replacements = []
  search_start = 0

  for expression in (
    statement.lhs,
    statement.rhs,
  ):
    rendered_expression = (
      _try_render_generic_narrative_expression_latex(
        expression
      )
    )

    if rendered_expression is None:
      continue

    normalized_expression = (
      _render_generic_narrative_expression_latex(
        expression
      )
    )

    expression_start = latex.find(
      rendered_expression,
      search_start,
    )

    if expression_start < 0:
      continue

    expression_end = (
      expression_start
      + len(
        rendered_expression
      )
    )
    search_start = expression_end

    if (
      normalized_expression
      == rendered_expression
    ):
      continue

    replacements.append(
      (
        expression_start,
        expression_end,
        normalized_expression,
      )
    )

  normalized = latex

  for (
    expression_start,
    expression_end,
    normalized_expression,
  ) in reversed(
    replacements
  ):
    normalized = (
      normalized[
        :expression_start
      ]
      + normalized_expression
      + normalized[
        expression_end:
      ]
    )

  return normalized
'''


NEW_NORMALIZE = '''def _normalize_generic_narrative_statement_latex(
  statement,
  latex: str,
) -> str:
  if not isinstance(
    latex,
    str,
  ):
    raise TypeError(
      "latex must be a str"
    )

  if not hasattr(
    statement,
    "lhs",
  ):
    return (
      _normalize_generic_eta_family_latex(
        latex
      )
    )

  if not hasattr(
    statement,
    "rhs",
  ):
    return (
      _normalize_generic_eta_family_latex(
        latex
      )
    )

  replacements = []
  search_start = 0

  for expression in (
    statement.lhs,
    statement.rhs,
  ):
    rendered_expression = (
      _try_render_generic_narrative_expression_latex(
        expression
      )
    )
    normalized_expression = None

    if rendered_expression is not None:
      normalized_expression = (
        _render_generic_narrative_expression_latex(
          expression
        )
      )
    else:
      rendered_expression = (
        _try_render_generic_narrative_group_structure_latex(
          expression
        )
      )

      if rendered_expression is not None:
        normalized_expression = (
          _normalize_generic_eta_family_latex(
            rendered_expression
          )
        )

    if (
      rendered_expression is None
      or normalized_expression is None
    ):
      continue

    expression_start = latex.find(
      rendered_expression,
      search_start,
    )

    if expression_start < 0:
      continue

    expression_end = (
      expression_start
      + len(
        rendered_expression
      )
    )
    search_start = expression_end

    if (
      normalized_expression
      == rendered_expression
    ):
      continue

    replacements.append(
      (
        expression_start,
        expression_end,
        normalized_expression,
      )
    )

  normalized = latex

  for (
    expression_start,
    expression_end,
    normalized_expression,
  ) in reversed(
    replacements
  ):
    normalized = (
      normalized[
        :expression_start
      ]
      + normalized_expression
      + normalized[
        expression_end:
      ]
    )

  return normalized
'''


OLD_STALE_TEST = '''def test_phase143_3_pi6_3_generic_step_uses_eta_cube():
  rendered_steps = tuple(
    _render_generic_narrative_step(step)
    for step in _pi6_3_steps()
  )
  assert any(r"\\\\eta_{3}^{3}" in rendered for rendered in rendered_steps)
  assert all(
    r"\\\\eta_{3}\\\\eta_{4}\\\\eta_{5}" not in rendered
    for rendered in rendered_steps
  )
'''


NEW_STALE_TEST = '''def test_phase143_3_pi6_3_generic_step_uses_eta_cube():
  rendered_steps = tuple(
    _render_generic_narrative_step(step)
    for step in _pi6_3_steps()
  )

  assert any(
    r"\\\\eta_{3}^{3}"
    in rendered
    for rendered in rendered_steps
  )
  assert any(
    (
      r"\\\\eta_{3}\\\\eta_{4}\\\\eta_{5}"
      in rendered
    )
    and (
      r"\\\\eta_{3}^{3}"
      in rendered
    )
    for rendered in rendered_steps
  )
'''


NEW_TEST_SOURCE = r'''from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _normalize_generic_narrative_statement_latex,
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
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def _eta(
  index: int,
) -> HomotopyElement:
  return HomotopyElement(
    name=(
      "η"
      + str(
        index
      )
    ),
    dimension=index,
    source=index + 1,
    target=index,
    generator=GeneratorSymbol(
      family="η",
      index=index,
    ),
  )


def _pi6_3_public_narrative() -> str:
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

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_r1_7c_r4_repair1_group_generator_uses_eta_power_notation():
  eta_5 = _eta(
    5
  )
  eta_6 = _eta(
    6
  )
  statement = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=5,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=eta_5,
        right=eta_6,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )
  raw = render_toda_proof_statement_latex(
    statement
  )

  assert (
    raw
    == (
      r"\pi_{7}^{5} = "
      r"\mathbb{Z}/2\{\eta_{5}\eta_{6}\}"
    )
  )

  normalized = (
    _normalize_generic_narrative_statement_latex(
      statement,
      raw,
    )
  )

  assert (
    normalized
    == (
      r"\pi_{7}^{5} = "
      r"\mathbb{Z}/2\{\eta_{5}^{2}\}"
    )
  )


def test_phase159_r1_7c_r4_repair1_public_pi6_3_reference_uses_eta5_squared():
  rendered = _pi6_3_public_narrative()

  canonical = (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}$."
  )
  expanded = (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\eta_{6}\}$."
  )

  assert canonical in rendered
  assert expanded not in rendered


def test_phase159_r1_7c_r4_repair1_derivation_equality_keeps_expanded_left_side():
  rendered = _pi6_3_public_narrative()

  assert (
    r"\eta_{3}\eta_{4}\eta_{5}"
    in rendered
  )
  assert (
    r"\eta_{3}^{3}"
    in rendered
  )


def test_phase159_r1_7c_r4_repair1_hopf_calculation_keeps_eta5_squared_result():
  rendered = _pi6_3_public_narrative()

  assert (
    r"H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}"
    in rendered
  )
'''


def replace_once(
    path: Path,
    old: str,
    new: str,
    description: str,
) -> None:
    text = path.read_text(
        encoding="utf-8"
    )

    count = text.count(
        old
    )
    if count != 1:
        raise SystemExit(
            f"{description}: expected exactly one match in {path}, found {count}"
        )

    path.write_text(
        text.replace(
            old,
            new,
            1,
        ),
        encoding="utf-8",
    )


def main() -> None:
    BACKUP.mkdir(
        parents=True,
        exist_ok=True,
    )

    for path in (
        PROD,
        STALE_TEST,
    ):
        shutil.copy2(
            path,
            BACKUP / path.name,
        )

    replace_once(
        PROD,
        OLD_TRY,
        NEW_TRY,
        "insert group-structure render fallback",
    )
    replace_once(
        PROD,
        OLD_NORMALIZE,
        NEW_NORMALIZE,
        "normalize group-structure relation side",
    )
    replace_once(
        STALE_TEST,
        OLD_STALE_TEST,
        NEW_STALE_TEST,
        "repair stale Phase 143 expectation",
    )

    if NEW_TEST.exists():
        raise SystemExit(
            f"new test already exists: {NEW_TEST}"
        )

    NEW_TEST.write_text(
        NEW_TEST_SOURCE,
        encoding="utf-8",
    )

    print(
        "Phase 159 R1-7c R4 generator canonicalization repair1 applied."
    )
    print(
        "Modified: toda_group_proof_generic_narrative_renderer.py"
    )
    print(
        "Modified: tests/test_phase143_3_generic_eta_normalization.py"
    )
    print(
        "Added: tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py"
    )


if __name__ == "__main__":
    main()
