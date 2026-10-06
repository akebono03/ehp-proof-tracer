from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

PROD = ROOT / "toda_group_proof_generic_narrative_renderer.py"
PHASE143 = ROOT / "tests" / "test_phase143_3_generic_eta_normalization.py"
PHASE157 = ROOT / "tests" / "test_phase157_r20_generic_dependency_rendering.py"
NEW_TEST = ROOT / "tests" / "test_phase159_r1_7c_r4_generator_canonicalization_repair1.py"


def replace_function(
    path: Path,
    function_name: str,
    new_source: str,
) -> None:
    text = path.read_text(
        encoding="utf-8"
    )
    marker = (
        "def "
        + function_name
        + "("
    )
    start = text.find(
        marker
    )
    if start < 0:
        raise SystemExit(
            f"function not found: {function_name} in {path}"
        )

    next_start = text.find(
        "\ndef ",
        start + len(marker),
    )
    if next_start < 0:
        end = len(
            text
        )
    else:
        end = (
            next_start
            + 1
        )

    replacement = (
        new_source.rstrip()
        + "\n\n"
    )

    updated = (
        text[
            :start
        ]
        + replacement
        + text[
            end:
        ]
    )
    path.write_text(
        updated,
        encoding="utf-8",
    )


def ensure_production_repair_present() -> None:
    text = PROD.read_text(
        encoding="utf-8"
    )

    helper_marker = (
        "def _try_render_generic_narrative_group_structure_latex("
    )
    fallback_marker = (
        "_try_render_generic_narrative_group_structure_latex(\n"
        "          expression\n"
        "        )"
    )

    if (
        helper_marker
        not in text
        or fallback_marker
        not in text
    ):
        raise SystemExit(
            "repair1 production change is not fully present. "
            "Do not continue with fix1; inspect the local production file."
        )


PHASE143_TEST = r'''def test_phase143_3_pi6_3_generic_step_uses_eta_cube():
  rendered_steps = tuple(
    _render_generic_narrative_step(step)
    for step in _pi6_3_steps()
  )

  assert any(
    r"\eta_{3}^{3}"
    in rendered
    for rendered in rendered_steps
  )
  assert any(
    (
      r"\eta_{3}\eta_{4}\eta_{5}"
      in rendered
    )
    and (
      r"\eta_{3}^{3}"
      in rendered
    )
    for rendered in rendered_steps
  )
'''


PHASE157_REFERENCE_TEST = r'''def test_phase157_r20_reference_dependencies_are_recovered_from_graph():
  rendered = _render_pi6_3_r20()

  for reference in (
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "(5.7)",
  ):
    assert reference in rendered

  assert (
    rendered.index(
      "[R5]より"
    )
    < rendered.index(
      "[R3]より"
    )
  )
'''


PHASE157_ETA_TEST = r'''def test_phase157_r20_eta_family_is_canonicalized_generically():
  rendered = _render_pi6_3_r20()

  assert r"\eta_{2}^{3}" in rendered
  assert r"\eta_{3}^{3}" in rendered
  assert r"\eta_{5}" in rendered
  assert r"\eta_{5}^{2}" in rendered

  assert (
    r"\eta_{2}\eta_{3}\eta_{4}"
    not in rendered
  )
  assert (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\eta_{6}\}$."
    not in rendered
  )
  assert (
    r"E^{2}\eta_{3}"
    not in rendered
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


def main() -> None:
    ensure_production_repair_present()

    BACKUP.mkdir(
        parents=True,
        exist_ok=True,
    )

    for path in (
        PHASE143,
        PHASE157,
    ):
        shutil.copy2(
            path,
            BACKUP / path.name,
        )

    replace_function(
        PHASE143,
        "test_phase143_3_pi6_3_generic_step_uses_eta_cube",
        PHASE143_TEST,
    )
    replace_function(
        PHASE157,
        "test_phase157_r20_reference_dependencies_are_recovered_from_graph",
        PHASE157_REFERENCE_TEST,
    )
    replace_function(
        PHASE157,
        "test_phase157_r20_eta_family_is_canonicalized_generically",
        PHASE157_ETA_TEST,
    )

    NEW_TEST.write_text(
        NEW_TEST_SOURCE,
        encoding="utf-8",
    )

    print(
        "Phase 159 R1-7c R4 generator canonicalization repair1 fix1 applied."
    )
    print(
        "Production repair1 was detected and preserved."
    )
    print(
        "Updated stale tests:"
    )
    print(
        "  tests/test_phase143_3_generic_eta_normalization.py"
    )
    print(
        "  tests/test_phase157_r20_generic_dependency_rendering.py"
    )
    print(
        "Added/refreshed:"
    )
    print(
        "  tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py"
    )


if __name__ == "__main__":
    main()
