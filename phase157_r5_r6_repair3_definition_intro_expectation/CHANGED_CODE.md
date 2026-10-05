# Phase157-R5-R6 repair3 changed tests

Production code changes: none.

Import changes: none.

## `tests/test_phase157_r5_r6_53_bracket_definition_reference.py`

```python
def test_phase157_r5_r6_pi6_keeps_definition_intro_but_hides_lemma52_internal_derivation():
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
```

## `tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py`

```python
def test_phase144_6_r25_9b_depth2_narrative_has_definition():
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
```

```python
def test_phase144_6_r25_9b_cli_depth2_narrative_has_definition(
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
```
