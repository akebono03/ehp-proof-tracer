
from pathlib import Path

TARGET = Path(
  "toda_group_proof_narrative_contribution_renderer.py"
)
R56_TEST = Path(
  "tests/test_phase157_r5_r6_53_bracket_definition_reference.py"
)
P144_TEST = Path(
  "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py"
)
R59_TEST = Path(
  "tests/test_phase157_r5_r9_fixed_definition_body_suppression.py"
)
OUTPUT_DIR = Path(
  "phase157_r5_r9_output"
)

OLD_SEMANTICS_IMPORT = '''from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
'''

NEW_SEMANTICS_IMPORT = '''from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeSemanticSidecar,
)
'''

HELPER = r'''def _phase157_r5_r9_selected_fixed_definition_step_ids(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> frozenset[
  int
]:
  selected_definition_step_ids = set()

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if (
        rendered_statement
        in seen_rendered_statements
      ):
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    for proof_step in selected_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is None
        or boundary.classification
        is not TodaLiteratureStatementClassification
        .FIXED_STATEMENT
        or boundary.component_key is None
        or not boundary.component_key.endswith(
          "_definition"
        )
      ):
        continue

      selected_definition_step_ids.add(
        id(
          proof_step
        )
      )

  return frozenset(
    selected_definition_step_ids
  )
'''

NEW_SUPPRESSION = r'''def suppress_toda_group_proof_narrative_reference_internal_body(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    semantic_sidecar,
    TodaGroupProofNarrativeSemanticSidecar,
  ):
    raise TypeError(
      "semantic_sidecar must be a "
      "TodaGroupProofNarrativeSemanticSidecar"
    )

  if (
    semantic_sidecar.presentation
    is not presentation
  ):
    raise ValueError(
      "semantic_sidecar must belong to presentation"
    )

  internal_step_ids = (
    _toda_group_proof_narrative_reference_internal_step_ids(
      presentation,
      reference_entries,
    )
  )
  fixed_definition_step_ids = (
    _phase157_r5_r9_selected_fixed_definition_step_ids(
      presentation,
      reference_entries,
    )
  )
  fixed_definition_precondition_step_ids = {
    id(
      dependency.prerequisite_step
    )
    for dependency
    in semantic_sidecar.dependency_semantics
    if (
      dependency.role
      is TodaGroupProofNarrativeDependencySemanticRole
      .PRECONDITION_FOR_DEFINITION
      and id(
        dependency.dependent_step
      )
      in fixed_definition_step_ids
    )
  }

  suppressed_step_ids = (
    set(
      internal_step_ids
    )
    | set(
      fixed_definition_step_ids
    )
    | fixed_definition_precondition_step_ids
  )

  if not suppressed_step_ids:
    return body_markdown

  suppressed_statement_lines = {
    rendered
    for node in presentation.nodes
    for proof_step in (
      node.proof_step,
    )
    if id(
      proof_step
    )
    in suppressed_step_ids
    for rendered in (
      _render_generic_narrative_step(
        proof_step
      ),
    )
    if rendered
  }

  suppressed_purpose_sentences = set()

  for argument in arguments:
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )

    if (
      conclusion_step is None
      or id(
        conclusion_step
      )
      not in suppressed_step_ids
    ):
      continue

    purpose = (
      render_toda_group_proof_narrative_argument_purpose_sentence(
        argument
      )
    )

    if purpose is not None:
      suppressed_purpose_sentences.add(
        purpose
      )

  retained_lines = []

  for line in body_markdown.splitlines():
    stripped = line.strip()

    if stripped in suppressed_statement_lines:
      continue

    if any(
      stripped.endswith(
        purpose
      )
      for purpose in suppressed_purpose_sentences
    ):
      continue

    retained_lines.append(
      line
    )

  compacted_lines = []
  previous_blank = False

  for line in retained_lines:
    is_blank = not line.strip()

    if (
      is_blank
      and previous_blank
    ):
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()
'''

R59_TEST_TEXT = r'''from toda_calculation_facade import (
  build_standard_toda_report,
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


def _pi6_3_rendered() -> str:
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _reference_and_body() -> tuple[
  str,
  str,
]:
  rendered = _pi6_3_rendered()
  reference_part, body_tail = (
    rendered.split(
      "次に",
      1,
    )
  )

  return (
    reference_part,
    "次に" + body_tail,
  )


def test_phase157_r5_r9_fixed_definition_remains_in_reference():
  rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "次に",
    1,
  )[
    0
  ]

  assert (
    (
      r"$\nu' \in "
      r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$"
      " とすると,"
    )
    in reference_part
  )
  assert (
    r"$\nu' \in \pi_{6}^{3}$,"
    in reference_part
  )
  assert (
    (
      r"$2\nu' = "
      r"\eta_{3}\eta_{4}\eta_{5}$."
    )
    in reference_part
  )


def test_phase157_r5_r9_fixed_definition_introduction_is_removed_from_body():
  rendered = _pi6_3_rendered()

  assert (
    r"$\nu'$ を定める."
    not in rendered
  )


def test_phase157_r5_r9_definition_only_precondition_is_removed_from_body():
  rendered = _pi6_3_rendered()

  assert (
    r"$2\eta_{3} = 0$"
    not in rendered
  )


def test_phase157_r5_r9_fixed_definition_statement_is_not_repeated_in_body():
  rendered = _pi6_3_rendered()
  definition = (
    r"\nu' \in "
    r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
  )

  assert (
    rendered.count(
      definition
    )
    == 1
  )


def test_phase157_r5_r9_body_starts_with_next_argument_after_reference_boundary():
  rendered = _pi6_3_rendered()
  body = rendered.split(
    "**[R3] Proposition 5.6.**",
    1,
  )[
    1
  ]

  assert (
    "次に, "
    r"$\nu'$ の位数を決定するために"
    in body
  )
'''


NEW_R56_TEST = r'''def test_phase157_r5_r6_pi6_hides_fixed_definition_internal_body():
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
  assert (
    r"$2\eta_{3} = 0$"
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
      "次に",
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
    r"$2\eta_{3} = 0$"
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
    r"$2\eta_{3} = 0$"
    not in output
  )
  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in output
  )
'''


def extract_function(
  text: str,
  function_name: str,
) -> str:
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


def main() -> None:
  for path in (
    TARGET,
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

  text = TARGET.read_text(
    encoding="utf-8"
  )

  if (
    "TodaGroupProofNarrativeDependencySemanticRole"
    not in text
  ):
    if OLD_SEMANTICS_IMPORT not in text:
      raise SystemExit(
        "semantic import block does not match expected current code"
      )

    text = text.replace(
      OLD_SEMANTICS_IMPORT,
      NEW_SEMANTICS_IMPORT,
      1,
    )

  helper_name = (
    "_phase157_r5_r9_selected_fixed_definition_step_ids"
  )

  if (
    "def "
    + helper_name
    + "("
    not in text
  ):
    suppression_marker = (
      "def suppress_toda_group_proof_narrative_reference_internal_body("
    )
    insertion_index = text.find(
      suppression_marker
    )

    if insertion_index < 0:
      raise SystemExit(
        "suppression function marker not found"
      )

    text = (
      text[
        :insertion_index
      ]
      + HELPER
      + "\n\n"
      + text[
        insertion_index:
      ]
    )

  text = replace_function(
    text,
    "suppress_toda_group_proof_narrative_reference_internal_body",
    NEW_SUPPRESSION,
  )

  render_name = (
    "render_toda_group_proof_narrative_"
    "multi_argument_with_contributions_markdown"
  )
  render_function = extract_function(
    text,
    render_name,
  )

  old_call = '''    suppress_toda_group_proof_narrative_reference_internal_body(
      presentation,
      rendered,
      reference_entries,
      arguments,
    )
'''

  new_call = '''    suppress_toda_group_proof_narrative_reference_internal_body(
      presentation,
      rendered,
      reference_entries,
      arguments,
      semantic_sidecar,
    )
'''

  if old_call in render_function:
    updated_render_function = (
      render_function.replace(
        old_call,
        new_call,
        1,
      )
    )
    text = text.replace(
      render_function,
      updated_render_function,
      1,
    )
  elif new_call not in render_function:
    raise SystemExit(
      "suppression call does not match expected current code"
    )

  TARGET.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  r56_text = R56_TEST.read_text(
    encoding="utf-8"
  )

  old_r56_names = (
    "test_phase157_r5_r6_pi6_keeps_definition_intro_but_hides_lemma52_internal_derivation",
    "test_phase157_r5_r6_pi6_keeps_53_internal_derivation_out_of_body",
  )
  replaced = False

  for old_name in old_r56_names:
    if (
      "def "
      + old_name
      + "("
      in r56_text
    ):
      r56_text = replace_function(
        r56_text,
        old_name,
        NEW_R56_TEST,
      )
      replaced = True
      break

  if not replaced:
    raise SystemExit(
      "R5-R6 body expectation test not found"
    )

  R56_TEST.write_text(
    r56_text,
    encoding="utf-8",
    newline="\n",
  )

  p144_text = P144_TEST.read_text(
    encoding="utf-8"
  )
  p144_text = replace_function(
    p144_text,
    "test_phase144_6_r25_9b_depth2_narrative_has_definition",
    NEW_P144_DEPTH2_TEST,
  )
  p144_text = replace_function(
    p144_text,
    "test_phase144_6_r25_9b_cli_depth2_narrative_has_definition",
    NEW_P144_CLI_TEST,
  )

  P144_TEST.write_text(
    p144_text,
    encoding="utf-8",
    newline="\n",
  )

  R59_TEST.write_text(
    R59_TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    OUTPUT_DIR
    / "semantic_import_after.txt"
  ).write_text(
    NEW_SEMANTICS_IMPORT,
    encoding="utf-8",
    newline="\n",
  )

  (
    OUTPUT_DIR
    / "selected_fixed_definition_helper_after.txt"
  ).write_text(
    extract_function(
      text,
      helper_name,
    ),
    encoding="utf-8",
    newline="\n",
  )

  (
    OUTPUT_DIR
    / "reference_internal_body_suppression_after.txt"
  ).write_text(
    extract_function(
      text,
      "suppress_toda_group_proof_narrative_reference_internal_body",
    ),
    encoding="utf-8",
    newline="\n",
  )

  (
    OUTPUT_DIR
    / "render_multi_argument_with_contributions_after.txt"
  ).write_text(
    extract_function(
      text,
      render_name,
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R5-R9 fixed-definition body suppression applied."
  )
  print(
    "Production file: "
    + str(
      TARGET
    )
  )
  print(
    "New focused test: "
    + str(
      R59_TEST
    )
  )


if __name__ == "__main__":
  main()
