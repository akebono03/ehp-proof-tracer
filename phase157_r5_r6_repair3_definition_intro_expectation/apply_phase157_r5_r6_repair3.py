
from __future__ import annotations

from pathlib import Path


R56_TEST = Path(
  "tests/test_phase157_r5_r6_53_bracket_definition_reference.py"
)
P144_TEST = Path(
  "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py"
)


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
    return text[start:]

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


NEW_R56_TEST = r'''def test_phase157_r5_r6_pi6_keeps_definition_intro_but_hides_lemma52_internal_derivation():
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
    in rendered
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
    in rendered
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
    in output
  )
  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in output
  )
'''


def main() -> None:
  for path in (
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

  r56_text = R56_TEST.read_text(
    encoding="utf-8"
  )
  r56_text = replace_function(
    r56_text,
    "test_phase157_r5_r6_pi6_keeps_53_internal_derivation_out_of_body",
    NEW_R56_TEST,
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

  print(
    "Phase157-R5-R6 repair3 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Updated only three test expectations."
  )
  print(
    "Definition introduction remains visible; "
    "Lemma 5.2 internal derivation remains hidden."
  )


if __name__ == "__main__":
  main()
