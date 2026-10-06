# Phase 159-R1-6c

## 変更対象

### production

- `toda_group_proof_narrative_renderer.py`
  - 新規 `_phase159_r1_6c_recursive_proof_steps()`
  - 新規 `_phase159_r1_6c_step_reference_locator()`
  - 新規 `_phase159_r1_6c_compact_map_property_line()`
  - 新規 `_phase159_r1_6c_statement_match_key()`
  - 新規 `_phase159_r1_6c_reference_number()`
  - 新規 `_phase159_r1_6c_canonicalize_toda_51_reference()`
  - 新規 `_phase159_r1_6c_remove_redundant_exactness_sentence()`
  - 新規 `_phase159_r1_6c_link_proof_reasons()`
  - 新規 `_phase159_r1_6c_render_statement_numbers()`
  - `render_toda_group_proof_narrative_markdown()`

import:
- 変更なし

### tests

- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py`
  - `test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically()`
- `tests/test_phase159_r1_6b_toda51_attribution.py`
  - `test_phase159_r1_6b_pi3_2_number_tags_include_map_property_statement()`
- 新規 `tests/test_phase159_r1_6c_source_faithful_reference_linkage.py`

## 新規 helper 群

`render_toda_group_proof_narrative_markdown()` の直前に追加。

```python
def _phase159_r1_6c_recursive_proof_steps(
  root_step: ProofStep,
) -> tuple[ProofStep, ...]:
  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  steps = []
  seen_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    step_id = id(
      proof_step
    )

    if step_id in seen_step_ids:
      return

    seen_step_ids.add(
      step_id
    )
    steps.append(
      proof_step
    )

    for premise in proof_step.premises:
      if isinstance(
        premise,
        ProofStep,
      ):
        visit(
          premise
        )

  visit(
    root_step
  )

  return tuple(
    steps
  )


def _phase159_r1_6c_step_reference_locator(
  proof_step: ProofStep,
) -> str | None:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  inference_rule = (
    proof_step.inference_rule
  )

  if inference_rule is None:
    return None

  reference = (
    inference_rule.literature_reference
  )

  if reference is None:
    return None

  return reference.locator


def _phase159_r1_6c_compact_map_property_line(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  replacements = (
    (
      " は単射である.",
      " は単射.",
    ),
    (
      " は全射である.",
      " は全射.",
    ),
    (
      " は同型写像である.",
      " は同型.",
    ),
    (
      " は零写像である.",
      " は零写像.",
    ),
  )

  normalized = rendered.strip()

  for old, new in replacements:
    if normalized.endswith(
      old
    ):
      return (
        normalized[
          :-len(
            old
          )
        ]
        + new
      )

  return normalized


def _phase159_r1_6c_statement_match_key(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  normalized = rendered.strip()

  normalized = re.sub(
    r"\\tag\{[0-9]+\}",
    "",
    normalized,
  )
  normalized = re.sub(
    r"\s+",
    " ",
    normalized,
  )

  return normalized


def _phase159_r1_6c_reference_number(
  rendered: str,
  locator: str,
) -> int | None:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if not isinstance(
    locator,
    str,
  ):
    raise TypeError(
      "locator must be a str"
    )

  match = re.search(
    r"^\*\*\[R([0-9]+)\] "
    + re.escape(
      locator
    )
    + r"\.\*\*$",
    rendered,
    flags=re.MULTILINE,
  )

  if match is None:
    return None

  return int(
    match.group(
      1
    )
  )


def _phase159_r1_6c_canonicalize_toda_51_reference(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  reference_marker = (
    "## 使用する結果\n\n"
  )
  proof_boundary = (
    "\n---\n\n## 証明"
  )
  reference_start = rendered.find(
    reference_marker
  )

  if reference_start < 0:
    return rendered

  content_start = (
    reference_start
    + len(
      reference_marker
    )
  )
  boundary_index = rendered.find(
    proof_boundary,
    content_start,
  )

  if boundary_index < 0:
    return rendered

  reference_body = rendered[
    content_start:
    boundary_index
  ]
  lines = reference_body.splitlines()
  output = []
  index = 0

  while index < len(
    lines
  ):
    match = re.match(
      r"^\*\*\[R([0-9]+)\] "
      r"\(5\.1\)\.\*\*$",
      lines[
        index
      ].strip(),
    )

    if match is None:
      output.append(
        lines[
          index
        ]
      )
      index += 1
      continue

    output.append(
      lines[
        index
      ]
    )
    output.append(
      (
        r"$\pi_{i}^{1} = 0\ (i > 1),"
        r"\qquad "
        r"\pi_{i}^{n} = 0\ (i < n)$."
      )
    )
    output.append(
      (
        r"$\pi_{n}^{n} = "
        r"\langle \iota_{n} \rangle "
        r"\cong \mathbb{Z}$."
      )
    )

    index += 1

    while (
      index < len(
        lines
      )
      and not lines[
        index
      ].strip().startswith(
        "**[R"
      )
    ):
      index += 1

  normalized_reference = "\n".join(
    output
  ).rstrip()

  return (
    rendered[
      :content_start
    ]
    + normalized_reference
    + rendered[
      boundary_index:
    ]
  )


def _phase159_r1_6c_remove_redundant_exactness_sentence(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  lines = rendered.splitlines()
  result = []

  for index, line in enumerate(
    lines
  ):
    stripped = line.strip()

    if not (
      stripped.startswith(
        "$"
      )
      and stripped.endswith(
        "$ は完全である."
      )
    ):
      result.append(
        line
      )
      continue

    previous_nonblank = next(
      (
        lines[
          previous_index
        ].strip()
        for previous_index in range(
          index - 1,
          -1,
          -1,
        )
        if lines[
          previous_index
        ].strip()
      ),
      "",
    )

    if not previous_nonblank.endswith(
      "次の完全列を考える."
    ):
      result.append(
        line
      )
      continue

    result.append(
      line.replace(
        "$ は完全である.",
        "$.",
        1,
      )
    )

  return "\n".join(
    result
  )


def _phase159_r1_6c_link_proof_reasons(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = (
    "## 証明\n\n"
  )
  proof_start = rendered.find(
    proof_marker
  )

  if proof_start < 0:
    return rendered

  body_start = (
    proof_start
    + len(
      proof_marker
    )
  )
  body = rendered[
    body_start:
  ]
  body_lines = body.splitlines()

  all_steps = (
    _phase159_r1_6c_recursive_proof_steps(
      presentation.root_step
    )
  )

  exactness_derived_keys = set()

  for proof_step in all_steps:
    if not any(
      (
        isinstance(
          premise,
          ProofStep,
        )
        and isinstance(
          premise.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      for premise in proof_step.premises
    ):
      continue

    rendered_step = (
      _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          proof_step
        )
      )
    )

    exactness_derived_keys.add(
      _phase159_r1_6c_statement_match_key(
        rendered_step
      )
    )

  suspension_pairs = []

  for proof_step in all_steps:
    if not isinstance(
      proof_step.conclusion,
      TodaSuspensionInjectiveStatement,
    ):
      continue

    source_step = next(
      (
        premise
        for premise in proof_step.premises
        if (
          isinstance(
            premise,
            ProofStep,
          )
          and isinstance(
            premise.conclusion,
            TodaSuspensionIsomorphismStatement,
          )
          and (
            _phase159_r1_6c_step_reference_locator(
              premise
            )
            == "(5.1)"
          )
        )
      ),
      None,
    )

    if source_step is None:
      continue

    source_line = (
      _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          source_step
        )
      )
    )
    target_line = (
      _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          proof_step
        )
      )
    )

    suspension_pairs.append(
      (
        _phase159_r1_6c_statement_match_key(
          target_line
        ),
        source_line,
      )
    )

  reference_number = (
    _phase159_r1_6c_reference_number(
      rendered,
      "(5.1)",
    )
  )

  linked_lines = []
  inserted_source_keys = set()

  for line in body_lines:
    stripped = line.strip()
    key = (
      _phase159_r1_6c_statement_match_key(
        stripped
      )
    )

    suspension_pair = next(
      (
        pair
        for pair in suspension_pairs
        if pair[
          0
        ] == key
      ),
      None,
    )

    if (
      suspension_pair is not None
      and reference_number is not None
    ):
      source_line = (
        suspension_pair[
          1
        ]
      )
      source_key = (
        _phase159_r1_6c_statement_match_key(
          source_line
        )
      )

      if source_key not in inserted_source_keys:
        if (
          linked_lines
          and linked_lines[
            -1
          ].strip()
        ):
          linked_lines.append(
            ""
          )

        linked_lines.append(
          (
            "[R"
            + str(
              reference_number
            )
            + "]より, "
            + source_line
          )
        )
        linked_lines.append(
          ""
        )
        inserted_source_keys.add(
          source_key
        )

      linked_lines.append(
        (
          "したがって, "
          + stripped
        )
      )
      continue

    if (
      key in exactness_derived_keys
      and not stripped.startswith(
        "完全性より,"
      )
    ):
      linked_lines.append(
        (
          "完全性より, "
          + stripped
        )
      )
      continue

    linked_lines.append(
      line
    )

  return (
    rendered[
      :body_start
    ]
    + "\n".join(
      linked_lines
    )
  )


def _phase159_r1_6c_render_statement_numbers(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  pattern = re.compile(
    r"^(?P<prefix>.*)"
    r"\$(?P<map>.+?)"
    r"\\tag\{(?P<number>[0-9]+)\}"
    r"\$ は"
    r"(?P<property>単射|全射|同型|零写像)"
    r"\.$"
  )

  result = []

  for line in rendered.splitlines():
    match = pattern.match(
      line
    )

    if match is None:
      result.append(
        line
      )
      continue

    result.append(
      (
        match.group(
          "prefix"
        )
        + "$"
        + match.group(
          "map"
        )
        + "$ は"
        + match.group(
          "property"
        )
        + ". ("
        + match.group(
          "number"
        )
        + ")"
      )
    )

  return "\n".join(
    result
  )
```

## 変更後 public render 関数全体

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_normalize_public_map_property_wording(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_normalize_public_reference_map_property_wording(
      rendered
    )
  )
  rendered = (
    _phase159_r1_6c_canonicalize_toda_51_reference(
      rendered
    )
  )
  rendered = (
    _phase159_r1_6c_remove_redundant_exactness_sentence(
      rendered
    )
  )
  rendered = (
    _phase159_r1_6c_link_proof_reasons(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_6c_render_statement_numbers(
      rendered
    )
  )

  return (
    _phase159_inject_foundational_reference_section(
      presentation,
      rendered,
    )
  )
```

## 変更後 R1-4 test 関数全体

```python
def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  injective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は単射. (1)"
  )
  surjective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は全射. (2)"
  )
  isomorphism = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は同型."
  )

  assert injective in rendered
  assert surjective in rendered
  assert isomorphism in rendered

  assert rendered.index(
    injective
  ) < rendered.index(
    isomorphism
  )
  assert rendered.index(
    surjective
  ) < rendered.index(
    isomorphism
  )

  assert r"\tag{1}" not in rendered
  assert r"\tag{2}" not in rendered
  assert r"\text{ は単射}" not in rendered
  assert r"\text{ は全射}" not in rendered

  assert (
    "(1), (2) より, "
    + isomorphism
    in rendered
  )
```

## 変更後 R1-6b numbering test 関数全体

```python
def test_phase159_r1_6b_pi3_2_number_tags_include_map_property_statement():
  presentation = (
    _phase159_r1_6b_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は単射. (1)"
    in rendered
  )
  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は全射. (2)"
    in rendered
  )

  assert r"\tag{1}" not in rendered
  assert r"\tag{2}" not in rendered

  assert (
    "(1), (2) より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
    in rendered
  )
```

## R1-6c の表示契約

Reference:

```text
[R1] (5.1).
π_i^1 = 0 (i>1),  π_i^n = 0 (i<n).
π_n^n = <ι_n> ≅ Z.
```

本文:

```text
π_3^2 の群構造を決定するために, 次の完全列を考える.

π_2^1 → π_3^2 → π_3^3 → π_1^1 → π_2^2.

[R1]より, π_2^1=0.

完全性より, H:π_3^2→π_3^3 は単射. (1)

[R1]より, E:π_1^1→π_2^2 は同型.

したがって, E:π_1^1→π_2^2 は単射.

完全性より, Δ:π_3^3→π_1^1 は零写像.

[R1]より, π_3^3=Z{ι_3}.

完全性より, H:π_3^2→π_3^3 は全射. (2)
```

## 実行する pytest

runner に以下を含む。

- R1-6c focused
- R1-6a/R1-6b focused
- Phase159 focused
- Phase157 boundary + Phase49 related regressions
- `git diff --check`

full pytest は実行しない。

## 完了条件

- `(5.1)` Reference が specialization の寄せ集めではなく原文の一般式になる。
- E 同型は Reference statement から本文導出へ移る。
- 完全列導入後の `は完全である.` を削除。
- exactness 由来の単射・零写像・全射に `完全性より,` が付く。
- `(1)`, `(2)` は `\tag` を使わず statement 後尾に表示。
- focused / related tests PASS。
- `git diff --check` PASS。

## 次 Phase との境界

R1-6c は `(5.1)` と低次元 EHP chain の public prose contract のみ。
他の Reference locator の source-faithful canonicalization や全群再監査は先取りしない。
Phase 159 最後まで full pytest は実行しない。
