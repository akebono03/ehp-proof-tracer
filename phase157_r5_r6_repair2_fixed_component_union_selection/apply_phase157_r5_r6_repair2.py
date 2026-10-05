
from __future__ import annotations

from pathlib import Path


REFERENCES = Path("toda_group_proof_narrative_references.py")
R2_TEST = Path("tests/test_phase157_r2_literature_statement_boundary.py")
R56_TEST = Path("tests/test_phase157_r5_r6_53_bracket_definition_reference.py")
P144_TEST = Path("tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py")
OUTPUT_DIR = Path("phase157_r5_r6_repair2_output")


def extract_function(
  text: str,
  function_name: str,
) -> str:
  marker = "def " + function_name + "("
  start = text.find(
    marker
  )

  if start < 0:
    raise SystemExit(
      "function not found: "
      + function_name
    )

  next_function = text.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_function < 0:
    return text[
      start:
    ]

  return text[
    start:
    next_function + 1
  ]


def replace_function(
  text: str,
  function_name: str,
  replacement: str,
) -> str:
  current = extract_function(
    text,
    function_name,
  )

  return text.replace(
    current,
    replacement.rstrip()
    + "\n",
    1,
  )


NEW_SELECT_FUNCTION = r'''def select_toda_group_proof_narrative_reference_statement_steps(
  entry: TodaGroupProofNarrativeReferenceEntry,
  candidate_steps: tuple[ProofStep, ...],
  proof_edges: tuple[TodaProofEdge, ...],
  root_step: ProofStep | None = None,
) -> tuple[ProofStep, ...]:
  if not isinstance(
    entry,
    TodaGroupProofNarrativeReferenceEntry,
  ):
    raise TypeError(
      "entry must be a "
      "TodaGroupProofNarrativeReferenceEntry"
    )

  if not isinstance(
    candidate_steps,
    tuple,
  ):
    raise TypeError(
      "candidate_steps must be a tuple"
    )

  if not all(
    isinstance(
      step,
      ProofStep,
    )
    for step in candidate_steps
  ):
    raise TypeError(
      "candidate_steps must contain only "
      "ProofStep objects"
    )

  if (
    root_step is not None
    and not isinstance(
      root_step,
      ProofStep,
    )
  ):
    raise TypeError(
      "root_step must be a ProofStep or None"
    )

  entry_step_ids = {
    id(
      step
    )
    for step in entry.proof_steps
  }
  seen_candidate_step_ids = set()

  for step in candidate_steps:
    step_id = id(
      step
    )

    if step_id not in entry_step_ids:
      raise ValueError(
        "candidate_steps must contain only "
        "steps from entry.proof_steps"
      )

    if step_id in seen_candidate_step_ids:
      raise ValueError(
        "candidate_steps must not contain "
        "the same ProofStep more than once"
      )

    seen_candidate_step_ids.add(
      step_id
    )

  if not isinstance(
    proof_edges,
    tuple,
  ):
    raise TypeError(
      "proof_edges must be a tuple"
    )

  if not all(
    isinstance(
      edge,
      TodaProofEdge,
    )
    for edge in proof_edges
  ):
    raise TypeError(
      "proof_edges must contain only "
      "TodaProofEdge objects"
    )

  eligible_candidates = tuple(
    step
    for step in candidate_steps
    if step is not root_step
  )

  if not eligible_candidates:
    return ()

  boundary_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in proof_edges
    if (
      edge.premise_step
      is not root_step
      and extract_toda_group_proof_step_literature_reference(
        edge.premise_step
      )
      == entry.reference
      and extract_toda_group_proof_step_literature_reference(
        edge.parent_step
      )
      != entry.reference
    )
  }

  entry_external_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in proof_edges
    if id(
      edge.parent_step
    ) not in entry_step_ids
  }

  used_candidate_step_ids = (
    boundary_used_step_ids
    | entry_external_used_step_ids
  )

  used_candidates = tuple(
    step
    for step in eligible_candidates
    if id(
      step
    ) in used_candidate_step_ids
  )

  if used_candidates:
    return used_candidates

  return (
    eligible_candidates[
      0
    ],
  )
'''


NEW_R2_INVENTORY_TEST = r'''def test_phase157_r2_equation53_inventory_has_no_group_order_policy():
  components = get_toda_fixed_statement_components(
    "(5.3)"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "nu_prime_bracket_definition",
    "nu_prime_membership",
    "nu_prime_hopf_relation",
    "nu_prime_double_relation",
  )
  assert all(
    component.order is None
    for component in components
  )
  assert tuple(
    component.statement_role
    for component in components
  ) == (
    TodaLiteratureStatementRole.MEMBERSHIP,
    TodaLiteratureStatementRole.MEMBERSHIP,
    TodaLiteratureStatementRole.MAP_VALUE,
    TodaLiteratureStatementRole.RELATION,
  )
'''


R56_TEST_TEXT = r'''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
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
  get_toda_fixed_statement_components,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)


def _pi6_3_presentation():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[
      0
    ]
    .source_candidate
    .group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def test_phase157_r5_r6_53_catalog_contains_bracket_definition_component():
  components = (
    get_toda_fixed_statement_components(
      "(5.3)"
    )
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "nu_prime_bracket_definition",
    "nu_prime_membership",
    "nu_prime_hopf_relation",
    "nu_prime_double_relation",
  )


def test_phase157_r5_r6_53_bracket_definition_source_is_fixed_statement():
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      _pi6_3_presentation()
    )
  )

  bracket_step = next(
    node.proof_step
    for node in closure.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaBracketMembershipStatement,
    )
  )

  boundary = (
    classify_toda_literature_statement_step(
      bracket_step
    )
  )

  assert boundary is not None
  assert (
    boundary.classification
    == TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert (
    boundary.reference_locator
    == "(5.3)"
  )
  assert (
    boundary.component_key
    == "nu_prime_bracket_definition"
  )


def test_phase157_r5_r6_53_specialization_remains_proof_internal():
  presentation = (
    _pi6_3_presentation()
  )

  specialization_step = next(
    node.proof_step
    for node in presentation.nodes
    if (
      node.proof_step.inference_rule
      is not None
      and node.proof_step.inference_rule.name
      == (
        "Toda 5.3 nu-prime Lemma 5.2 "
        "bracket specialization"
      )
    )
  )

  boundary = (
    classify_toda_literature_statement_step(
      specialization_step
    )
  )

  assert boundary is not None
  assert (
    boundary.classification
    == TodaLiteratureStatementClassification.PROOF_INTERNAL
  )


def test_phase157_r5_r6_pi6_reference_53_displays_bracket_definition():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi6_3_presentation()
    )
  )
  reference_part = (
    rendered.split(
      "まず",
      1,
    )[
      0
    ]
  )

  assert (
    "**[R1] (5.3).**"
    in reference_part
  )
  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in reference_part
    or
    r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"
    in reference_part
  )


def test_phase157_r5_r6_pi6_keeps_53_internal_derivation_out_of_body():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi6_3_presentation()
    )
  )

  assert (
    "Lemma 5.2"
    not in rendered
  )
  assert (
    r"$\nu'$ を定める."
    not in rendered
  )
'''


NEW_P144_DEPTH2_TEST = r'''def test_phase144_6_r25_9b_depth2_narrative_has_definition():
  _, presentation = (
    _pi6_3_depth2()
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  reference_part = (
    rendered.split(
      "まず",
      1,
    )[
      0
    ]
  )

  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in reference_part
    or
    r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"
    in reference_part
  )
  assert (
    r"$\nu'$ を定める."
    not in rendered
  )
  assert (
    r"2\nu' = \eta_{3}^{3}"
    in rendered
  )
  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in rendered
  )
'''


NEW_P144_CLI_TEST = r'''def test_phase144_6_r25_9b_cli_depth2_narrative_has_definition(
  capsys,
):
  exit_code = (
    _run_group_proof_command(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )
  output = (
    capsys.readouterr().out
  )

  assert exit_code == 0
  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in output
    or
    r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"
    in output
  )
  assert (
    r"$\nu'$ を定める."
    not in output
  )
  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in output
  )
'''


def main() -> None:
  for path in (
    REFERENCES,
    R2_TEST,
    R56_TEST,
    P144_TEST,
  ):
    if not path.exists():
      raise SystemExit(
        "target not found: "
        + str(
          path
        )
      )

  references_text = (
    REFERENCES.read_text(
      encoding="utf-8"
    )
  )
  references_text = replace_function(
    references_text,
    (
      "select_toda_group_proof_narrative_"
      "reference_statement_steps"
    ),
    NEW_SELECT_FUNCTION,
  )
  REFERENCES.write_text(
    references_text,
    encoding="utf-8",
    newline="\n",
  )

  r2_text = (
    R2_TEST.read_text(
      encoding="utf-8"
    )
  )
  r2_text = replace_function(
    r2_text,
    (
      "test_phase157_r2_equation53_"
      "inventory_has_no_group_order_policy"
    ),
    NEW_R2_INVENTORY_TEST,
  )
  R2_TEST.write_text(
    r2_text,
    encoding="utf-8",
    newline="\n",
  )

  R56_TEST.write_text(
    R56_TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  p144_text = (
    P144_TEST.read_text(
      encoding="utf-8"
    )
  )
  p144_text = replace_function(
    p144_text,
    (
      "test_phase144_6_r25_9b_"
      "depth2_narrative_has_definition"
    ),
    NEW_P144_DEPTH2_TEST,
  )
  p144_text = replace_function(
    p144_text,
    (
      "test_phase144_6_r25_9b_cli_"
      "depth2_narrative_has_definition"
    ),
    NEW_P144_CLI_TEST,
  )
  P144_TEST.write_text(
    p144_text,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    OUTPUT_DIR
    / "select_reference_statement_steps_after.txt"
  ).write_text(
    extract_function(
      references_text,
      (
        "select_toda_group_proof_narrative_"
        "reference_statement_steps"
      ),
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R5-R6 repair2 applied."
  )
  print(
    "Reference selector now keeps the union of "
    "boundary-used and entry-external-used fixed components."
  )
  print(
    "Phase156 public-boundary behavior is preserved: "
    "Lemma 5.2 internal derivation stays out of the body."
  )


if __name__ == "__main__":
  main()
