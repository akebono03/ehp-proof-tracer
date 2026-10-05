from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST_RC4_7A = ROOT / "tests" / "test_phase150_rc4_7a_cross_group_reference_normalization.py"
TEST_RC4_7D3 = ROOT / "tests" / "test_phase150_rc4_7d_3_public_narrative_generic_route.py"
NEW_TEST = ROOT / "tests" / "test_phase158_r5_5b_public_generic_order_route.py"


def replace_top_level_function(
  text: str,
  function_name: str,
  replacement: str,
) -> str:
  marker = "def " + function_name + "("
  start = text.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_start = text.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_start < 0:
    end = len(
      text
    )
  else:
    end = next_start + 1

  return (
    text[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + text[
      end:
    ].lstrip(
      "\n"
    )
  )


HELPER = r'''def _phase158_r5_5b_has_ordered_root_argument(
  presentation: TodaGroupProofPresentation,
) -> bool:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if presentation.max_depth < 2:
    return False

  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  return any(
    (
      argument.supporting_blocks
      and presentation.root_step
      in argument.conclusion_block.steps
    )
    for argument in arguments
  )'''


GENERIC_SELECTOR = r'''def _is_phase150_rc4_generic_route_target(
  presentation: TodaGroupProofPresentation,
) -> bool:
  if presentation.max_depth < 2:
    return False

  if _is_phase134_9_pi8_5_presentation(
    presentation
  ):
    return False

  if _phase158_r5_5b_has_ordered_root_argument(
    presentation
  ):
    return True

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  return (
    (
      target.group_dimension == 10
      and target.sphere_dimension == 4
    )
    or (
      target.group_dimension == 12
      and target.sphere_dimension == 5
    )
    or (
      target.group_dimension == 16
      and target.sphere_dimension == 9
    )
  )'''


PI15_RENDERER = r'''def _phase134_24_render_pi15_8_narrative(
  presentation: TodaGroupProofPresentation,
) -> str | None:
  from toda_human_readable_renderer import (
    render_toda_expression_latex,
  )
  from toda_proof_narrative_renderer import (
    render_toda_primary_group_latex,
    render_toda_raw_group_structure_latex,
  )
  from toda_rules import (
    Toda515Sigma8TransportedDecompositionStatement,
  )

  if presentation.max_depth < 2:
    return None

  if _phase158_r5_5b_has_ordered_root_argument(
    presentation
  ):
    return None

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  if (
    target.group_dimension != 15
    or target.sphere_dimension != 8
  ):
    return None

  transported_step = next(
    (
      node.proof_step
      for node in presentation.nodes
      if isinstance(
        node.proof_step.conclusion,
        Toda515Sigma8TransportedDecompositionStatement,
      )
    ),
    None,
  )

  if transported_step is None:
    return None

  statement = transported_step.conclusion
  decomposition_map = (
    statement
    .prop44_isomorphism
    .map
  )

  source_summands = (
    decomposition_map
    .source_group
    .summands
  )

  if len(
    source_summands
  ) != 2:
    return None

  pi14_7_latex = (
    render_repository_conclusion_latex(
      statement.pi14_7_group_relation
    )
  )

  pi15_15_latex = (
    render_repository_conclusion_latex(
      statement.pi15_15_group_relation
    )
  )

  source_left_latex = (
    render_toda_primary_group_latex(
      source_summands[0]
    )
  )

  source_right_latex = (
    render_toda_primary_group_latex(
      source_summands[1]
    )
  )

  target_latex = (
    render_toda_primary_group_latex(
      decomposition_map.target_group
    )
  )

  first_variable_latex = (
    render_toda_expression_latex(
      decomposition_map.beta
    )
  )

  second_variable_latex = (
    render_toda_expression_latex(
      decomposition_map.gamma
    )
  )

  formula_latex = (
    render_toda_expression_latex(
      decomposition_map.formula
    )
  )

  first_source_generator_latex = (
    render_toda_expression_latex(
      statement
      .pi14_7_group_relation
      .rhs
      .generator
    )
  )

  second_source_generator_latex = (
    render_toda_expression_latex(
      statement
      .pi15_15_group_relation
      .rhs
      .generator
    )
  )

  first_image_latex = (
    render_toda_expression_latex(
      statement.first_generator_image
    )
  )

  second_image_latex = (
    render_toda_expression_latex(
      statement.second_generator_image
    )
  )

  transported_group_latex = (
    render_toda_raw_group_structure_latex(
      statement.transported_group
    )
  )

  final_relation_latex = (
    render_repository_conclusion_latex(
      presentation.root_step.conclusion
    )
  )

  lines = [
    *_phase134_26_narrative_start_lines(
      [
        "Toda Proposition 5.15 のうち,",
        "",
        "\\[",
        final_relation_latex,
        "\\]",
        "",
        "を示す.",
      ]
    ),
    *_phase134_28_reference_section_lines(
      (
        (
          "Toda Proposition 4.4 の分解同型",
          (
            "次の写像は同型である.",
            "",
            "\\[",
            (
              source_left_latex
              + r" \oplus "
              + source_right_latex
              + r" \longrightarrow "
              + target_latex
            ),
            "\\]",
            "",
            "\\[",
            (
              "("
              + first_variable_latex
              + ", "
              + second_variable_latex
              + r") \longmapsto "
              + formula_latex
            ),
            "\\]",
          ),
        ),
      )
    ),
    *_phase134_26_narrative_section_header_lines(
      "証明"
    ),
    *_phase134_30_completed_boundary_lines(
      pi14_7_latex,
      closing_text="である.",
    ),
    "また,",
    "",
    "\\[",
    pi15_15_latex,
    "\\]",
    "",
    "である.",
    "",
    "[R1] より, これらの生成元はそれぞれ",
    "",
    "\\[",
    (
      first_source_generator_latex
      + r" \longmapsto "
      + first_image_latex
      + ","
    ),
    "\\qquad",
    (
      second_source_generator_latex
      + r" \longmapsto "
      + second_image_latex
    ),
    "\\]",
    "",
    "と写る.",
    "",
    *_phase134_30_final_conclusion_lines(
      (
        target_latex
        + r" \cong "
        + transported_group_latex
      )
    ),
    "直和因子の順序を入れ替えると,",
    "",
    "\\[",
    final_relation_latex,
    "\\]",
    "",
    "を得る.",
  ]

  return (
    "\n".join(
      lines
    )
    + "\n"
  )'''


RC4_7A_TEST = r'''def test_phase150_rc4_7a_pi15_8_uses_generic_order_contract(
):
  rendered = _render_group(
    8,
    7,
  )

  transported = (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
  )
  final = (
    r"$\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}$"
  )

  assert "Proposition 4.4" in rendered
  assert transported in rendered
  assert final in rendered
  assert rendered.index(
    transported
  ) < rendered.index(
    final
  )'''


RC4_7D3_TEST = r'''def test_phase150_rc4_7d_3_pi15_public_route_uses_generic_order():
  markdown = render_toda_group_proof_narrative_markdown(
    _presentation(8, 7)
  )

  transported = (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
  )
  final = (
    r"$\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}$"
  )

  assert transported in markdown
  assert final in markdown
  assert markdown.index(
    transported
  ) < markdown.index(
    final
  )'''


NEW_TEST_TEXT = r'''import toda_group_proof_narrative_renderer as narrative_renderer
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase158_r5_5b_has_ordered_root_argument,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
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

  return build_toda_group_proof_presentation(
    replay
  )


def _web_text(
  n: int,
  k: int,
) -> str:
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=2,
    mode="narrative",
  )
  parts = []

  for line in view.rendered_lines:
    if line.segments:
      parts.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
    else:
      parts.append(
        line.prefix
        + (
          ""
          if line.statement_latex is None
          else line.statement_latex
        )
        + line.suffix
      )

  return "\n".join(
    parts
  )


def test_phase158_r5_5b_pi7_4_root_argument_uses_generic_order():
  presentation = _presentation(
    4,
    3,
  )

  assert (
    _phase158_r5_5b_has_ordered_root_argument(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  premise = (
    r"$\nu_{4}$ の分解を用いる."
  )
  target = (
    r"$\pi_{7}^{4} = "
    r"\mathbb{Z}\{\nu_{4}\} "
    r"\oplus \mathbb{Z}/4\{E\nu'\}$"
  )

  assert premise in rendered
  assert target in rendered
  assert rendered.index(
    premise
  ) < rendered.index(
    target
  )


def test_phase158_r5_5b_pi15_8_root_argument_uses_generic_order():
  presentation = _presentation(
    8,
    7,
  )

  assert (
    _phase158_r5_5b_has_ordered_root_argument(
      presentation
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  transported = (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
  )
  target = (
    r"$\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}$"
  )

  assert transported in rendered
  assert target in rendered
  assert rendered.index(
    transported
  ) < rendered.index(
    target
  )


def test_phase158_r5_5b_pi15_8_does_not_use_legacy_dedicated_renderer(
  monkeypatch,
):
  presentation = _presentation(
    8,
    7,
  )

  def fail_if_called(
    _presentation,
  ):
    raise AssertionError(
      "legacy pi15_8 renderer was called"
    )

  monkeypatch.setattr(
    narrative_renderer,
    "_phase134_24_render_pi15_8_narrative",
    fail_if_called,
  )

  rendered = (
    narrative_renderer
    .render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert (
    r"\pi_{15}^{8}"
    in rendered
  )


def test_phase158_r5_5b_web_depth2_pi7_4_preserves_premise_before_target():
  rendered = _web_text(
    4,
    3,
  )

  premise = (
    r"\nu_{4} の分解を用いる."
  )
  target = (
    r"\pi_{7}^{4} = "
    r"\mathbb{Z}\{\nu_{4}\} "
    r"\oplus \mathbb{Z}/4\{E\nu'\}"
  )

  assert premise in rendered
  assert target in rendered
  assert rendered.index(
    premise
  ) < rendered.index(
    target
  )


def test_phase158_r5_5b_web_depth2_pi15_8_preserves_transport_before_target():
  rendered = _web_text(
    8,
    7,
  )

  transported = (
    r"\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}"
  )
  target = (
    r"\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}"
  )

  assert transported in rendered
  assert target in rendered
  assert rendered.index(
    transported
  ) < rendered.index(
    target
  )
'''


def main() -> int:
  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase158_r5_5b_backup_"
      + timestamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    RENDERER,
    TEST_RC4_7A,
    TEST_RC4_7D3,
  ):
    if not path.exists():
      raise RuntimeError(
        "missing expected file: "
        + str(
          path
        )
      )

    shutil.copy2(
      path,
      backup_dir
      / path.name,
    )

  renderer_text = RENDERER.read_text(
    encoding="utf-8"
  )

  if (
    "def _phase158_r5_5b_has_ordered_root_argument("
    not in renderer_text
  ):
    anchor = (
      "def _is_phase150_rc4_generic_route_target("
    )
    anchor_index = renderer_text.find(
      anchor
    )

    if anchor_index < 0:
      raise RuntimeError(
        "generic route target anchor not found"
      )

    renderer_text = (
      renderer_text[
        :anchor_index
      ]
      + HELPER
      + "\n\n"
      + renderer_text[
        anchor_index:
      ]
    )

  renderer_text = replace_top_level_function(
    renderer_text,
    "_phase134_24_render_pi15_8_narrative",
    PI15_RENDERER,
  )
  renderer_text = replace_top_level_function(
    renderer_text,
    "_is_phase150_rc4_generic_route_target",
    GENERIC_SELECTOR,
  )

  RENDERER.write_text(
    renderer_text,
    encoding="utf-8",
    newline="\n",
  )

  rc4_7a_text = TEST_RC4_7A.read_text(
    encoding="utf-8"
  )
  rc4_7a_text = replace_top_level_function(
    rc4_7a_text,
    "test_phase150_rc4_7a_pi15_8_special_renderer_is_unchanged",
    RC4_7A_TEST,
  )
  TEST_RC4_7A.write_text(
    rc4_7a_text,
    encoding="utf-8",
    newline="\n",
  )

  rc4_7d3_text = TEST_RC4_7D3.read_text(
    encoding="utf-8"
  )
  rc4_7d3_text = replace_top_level_function(
    rc4_7d3_text,
    "test_phase150_rc4_7d_3_pi15_dedicated_route_is_preserved",
    RC4_7D3_TEST,
  )
  TEST_RC4_7D3.write_text(
    rc4_7d3_text,
    encoding="utf-8",
    newline="\n",
  )

  NEW_TEST.write_text(
    NEW_TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 158-R5-5b applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Production file changed: "
    + RENDERER.name
  )
  print(
    "Existing stale tests updated: 2"
  )
  print(
    "New focused test file: "
    + NEW_TEST.name
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
