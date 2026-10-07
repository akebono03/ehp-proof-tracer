from homotopy_groups import (
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_4_5_zero_fact,
  pi_5_5_free_cyclic_fact,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)
from toda_upstream_bootstrap import (
  _build_phase49_result,
  _build_phase50_result,
)


def _group_data(
  n: int,
  k: int,
  depth: int = 2,
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
    max_depth=depth,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )

  return (
    raw,
    closure,
    rendered,
  )


def _reference_section(
  rendered: str,
) -> str:
  marker = "## 使用する結果"
  assert marker in rendered
  start = rendered.index(
    marker
  )
  end = rendered.index(
    "---",
    start,
  )
  return rendered[
    start:end
  ]


def test_phase159_repair2g_pi4_map_image_and_kernel_are_map_properties():
  phase50 = _build_phase50_result()

  image_step = next(
    step
    for step in phase50[
      "result"
    ].steps
    if isinstance(
      step.conclusion,
      (
        TodaDeltaImageFreeCyclicStatement,
        TodaDeltaImageUpToSignStatement,
      ),
    )
  )
  kernel_step = next(
    step
    for step in phase50[
      "result"
    ].steps
    if isinstance(
      step.conclusion,
      TodaSuspensionKernelFreeCyclicStatement,
    )
  )

  assert (
    classify_toda_proof_step_role(
      image_step
    )
    is TodaProofDependencyRole.MAP_PROPERTY
  )
  assert (
    classify_toda_proof_step_role(
      kernel_step
    )
    is TodaProofDependencyRole.MAP_PROPERTY
  )


def test_phase159_repair2g_phase50_fixed_sources_have_expected_boundaries():
  phase50 = _build_phase50_result()

  pi5_step = next(
    step
    for step in phase50[
      "result"
    ].steps
    if step.conclusion
    == pi_5_5_free_cyclic_fact()
  )
  pi4_zero_step = next(
    step
    for step in phase50[
      "result"
    ].steps
    if step.conclusion
    == pi_4_5_zero_fact()
  )
  delta_step = next(
    step
    for step in phase50[
      "result"
    ].steps
    if isinstance(
      step.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )

  expected_51_components = (
    (
      pi5_step,
      "diagonal_identity_group",
    ),
    (
      pi4_zero_step,
      "sphere_connectivity_zero",
    ),
  )

  for step, expected_component_key in (
    expected_51_components
  ):
    boundary = (
      classify_toda_literature_statement_step(
        step
      )
    )
    reference = (
      extract_toda_group_proof_step_literature_reference(
        step
      )
    )

    assert boundary is not None
    assert (
      boundary.classification
      is TodaLiteratureStatementClassification.FIXED_STATEMENT
    )
    assert boundary.reference_locator == "(5.1)"
    assert (
      boundary.component_key
      == expected_component_key
    )
    assert reference is not None
    assert reference.locator == "(5.1)"

  delta_boundary = (
    classify_toda_literature_statement_step(
      delta_step
    )
  )

  assert delta_boundary is not None
  assert (
    delta_boundary.classification
    is TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert (
    delta_boundary.reference_locator
    == "Proposition 5.1"
  )
  assert (
    delta_boundary.component_key
    == "delta_iota5_relation"
  )


def test_phase159_repair2g_phase49_keeps_given_contract_with_51_metadata():
  phase49 = _build_phase49_result()

  assert all(
    step.rule.value == "given"
    for step in phase49[
      "premise_steps"
    ]
  )

  fixed_51_steps = tuple(
    step
    for step in phase49[
      "premise_steps"
    ]
    if (
      extract_toda_group_proof_step_literature_reference(
        step
      )
      is not None
      and (
        extract_toda_group_proof_step_literature_reference(
          step
        ).locator
        == "(5.1)"
      )
    )
  )
  fixed_51_conclusions = tuple(
    step.conclusion
    for step in fixed_51_steps
  )

  from low_dimensional_facts import (
    pi_2_1_zero_fact,
    pi_3_3_free_cyclic_fact,
  )

  assert (
    pi_2_1_zero_fact()
    in fixed_51_conclusions
  )
  assert (
    pi_3_3_free_cyclic_fact()
    in fixed_51_conclusions
  )
def test_phase159_repair2g_pi4_depth2_closure_reaches_delta_reference_sources():
  _, closure, _ = _group_data(
    3,
    1,
  )

  conclusions = tuple(
    node.proof_step.conclusion
    for node in closure.nodes
  )

  assert any(
    isinstance(
      conclusion,
      (
        TodaDeltaImageFreeCyclicStatement,
        TodaDeltaImageUpToSignStatement,
      ),
    )
    for conclusion in conclusions
  )
  assert any(
    isinstance(
      conclusion,
      TodaSuspensionKernelFreeCyclicStatement,
    )
    for conclusion in conclusions
  )
  assert any(
    isinstance(
      conclusion,
      TodaDeltaImageUpToSignStatement,
    )
    for conclusion in conclusions
  )
  assert (
    pi_5_5_free_cyclic_fact()
    in conclusions
  )
  assert (
    pi_4_5_zero_fact()
    in conclusions
  )


def test_phase159_repair2g_pi4_public_reference_policy_is_51_then_prop51():
  _, _, rendered = _group_data(
    3,
    1,
  )
  reference = _reference_section(
    rendered
  )

  assert "**[R1] (5.1).**" in reference
  assert (
    "**[R2] Proposition 5.1.**"
    in reference
  )

  assert (
    r"\pi_{5}^{5}"
    in reference
  )
  assert (
    r"\mathbb{Z}\{\iota_{5}\}"
    in reference
  )
  assert (
    r"\pi_{4}^{5} = 0"
    in reference
  )

  assert (
    r"\pi_{3}^{2}"
    in reference
  )
  assert (
    r"\mathbb{Z}\{\eta_{2}\}"
    in reference
  )
  assert (
    r"\Delta"
    in reference
  )
  assert (
    r"\iota_{5}"
    in reference
  )
  assert (
    r"2\eta_{2}"
    in reference
  )

  assert "Proposition 4.2" not in reference
  assert r"\xrightarrow" not in reference


def test_phase159_repair2g_pi3_keeps_single_51_reference_policy():
  _, _, rendered = _group_data(
    2,
    1,
  )
  reference = _reference_section(
    rendered
  )

  assert "**[R1] (5.1).**" in reference
  assert "Proposition 5.1" not in reference
  assert (
    reference.count(
      "**[R"
    )
    == 1
  )


def test_phase159_repair2g_ehp_exactness_is_not_a_reference():
  _, _, rendered = _group_data(
    3,
    1,
  )
  reference = _reference_section(
    rendered
  )

  assert "Proposition 4.2" not in reference
  assert "EHP" not in reference
  assert "完全" not in reference
