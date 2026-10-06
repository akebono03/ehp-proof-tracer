# Phase 159 R1-7c R4 equation-reference order repair1

## 変更対象

### production

`toda_group_proof_narrative_renderer.py`

新規関数追加位置:
`render_toda_group_proof_narrative_markdown()` の直前。

```python
def _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\n\n"
  marker_index = rendered.find(
    proof_marker
  )

  if marker_index < 0:
    return rendered

  proof_start = (
    marker_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :proof_start
  ]
  proof_body = rendered[
    proof_start:
  ]

  had_trailing_newline = (
    rendered.endswith(
      "\n"
    )
  )
  paragraphs = proof_body.rstrip(
    "\n"
  ).split(
    "\n\n"
  )

  tag_pattern = re.compile(
    r"\\tag\{(\d+)\}"
  )
  reference_pattern = re.compile(
    (
      r"^"
      r"((?:\(\d+\)"
      r"(?:,\s*|\s+と\s+)?)+)"
      r"\s*より,"
    )
  )
  parenthesized_number_pattern = re.compile(
    r"\((\d+)\)"
  )

  changed = True

  while changed:
    changed = False
    tag_paragraph_by_number = {}

    for paragraph_index, paragraph in enumerate(
      paragraphs
    ):
      for match in tag_pattern.finditer(
        paragraph
      ):
        number = int(
          match.group(
            1
          )
        )
        tag_paragraph_by_number.setdefault(
          number,
          paragraph_index,
        )

    for conclusion_index, paragraph in enumerate(
      paragraphs
    ):
      stripped = paragraph.strip()
      reference_match = reference_pattern.match(
        stripped
      )

      if reference_match is None:
        continue

      reference_numbers = tuple(
        int(
          number
        )
        for number in parenthesized_number_pattern.findall(
          reference_match.group(
            1
          )
        )
      )

      if not reference_numbers:
        continue

      referenced_indices = tuple(
        tag_paragraph_by_number.get(
          number
        )
        for number in reference_numbers
      )

      if any(
        index is None
        for index in referenced_indices
      ):
        continue

      target_index = max(
        index
        for index in referenced_indices
        if index is not None
      )

      if target_index < conclusion_index:
        continue

      conclusion = paragraphs.pop(
        conclusion_index
      )

      if conclusion_index < target_index:
        target_index -= 1

      paragraphs.insert(
        target_index + 1,
        conclusion,
      )
      changed = True
      break

  result = (
    prefix
    + "\n\n".join(
      paragraphs
    )
  )

  if had_trailing_newline:
    result += "\n"

  return result
```

変更関数全体:

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
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  return (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )
```

import の変更はありません。

### test

新規:
`tests/test_phase159_r1_7c_r4_equation_reference_order_repair1.py`

必要な import とテスト関数全文:

```python
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _public_narrative(
  n: int,
  k: int,
) -> str:
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_r1_7c_r4_pi5_3_places_isomorphism_after_both_numbered_premises():
  rendered = _public_narrative(
    3,
    2,
  )

  injective = (
    r"$E: \pi_{4}^{2} \to \pi_{5}^{3}\tag{1}$ は単射."
  )
  surjective = (
    r"これより, $E: \pi_{4}^{2} \to \pi_{5}^{3}\tag{2}$ は全射."
  )
  isomorphism = (
    r"(1), (2) より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型."
  )

  assert injective in rendered
  assert surjective in rendered
  assert isomorphism in rendered
  assert (
    rendered.index(
      injective
    )
    < rendered.index(
      surjective
    )
    < rendered.index(
      isomorphism
    )
  )


def test_phase159_r1_7c_r4_pi3_2_keeps_valid_backward_equation_references():
  rendered = _public_narrative(
    2,
    1,
  )

  injective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{1}$ は単射."
  )
  surjective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{2}$ は全射."
  )
  isomorphism = (
    r"(1), (2) より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
  )

  assert (
    rendered.index(
      injective
    )
    < rendered.index(
      surjective
    )
    < rendered.index(
      isomorphism
    )
  )


def test_phase159_r1_7c_r4_reorder_helper_moves_only_forward_reference_conclusion():
  rendered = (
    "# Group proof narrative\n\n"
    "## 証明\n\n"
    "(1), (2) より, $F: A \\to B$ は同型.\n\n"
    "$F: A \\to B\\tag{1}$ は単射.\n\n"
    "$F: A \\to B\\tag{2}$ は全射.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )

  injective = (
    r"$F: A \to B\tag{1}$ は単射."
  )
  surjective = (
    r"$F: A \to B\tag{2}$ は全射."
  )
  isomorphism = (
    r"(1), (2) より, $F: A \to B$ は同型."
  )

  assert (
    normalized.index(
      injective
    )
    < normalized.index(
      surjective
    )
    < normalized.index(
      isomorphism
    )
  )


def test_phase159_r1_7c_r4_reorder_helper_leaves_missing_reference_untouched():
  rendered = (
    "# Group proof narrative\n\n"
    "## 証明\n\n"
    "(1), (2) より, $F: A \\to B$ は同型.\n\n"
    "$F: A \\to B\\tag{1}$ は単射.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )

  assert normalized == rendered
```

## 変更理由

cross-output audit で forward equation reference は
$\pi_5^3$ の2参照だけ確認された。

現状:
`(1), (2) より, E は同型.` が
`E\tag{1} は単射.` と
`E\tag{2} は全射.` より前にある。

一般規則として、参照番号を含む結論 paragraph が
参照元 paragraph より前にある場合だけ、
最後の参照元の直後へ移動する。

既に正しい backward reference は移動しない。
参照 tag が欠ける場合も移動しない。

## 実行する pytest

- `tests/test_phase159_r1_7c_r4_equation_reference_order_repair1.py`
- `tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`
- `tests/test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py`
- `tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py`
- `tests/test_phase157_r20_repair32_exactness_intro_anchor.py`
- `tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py`

## 完了条件

- $\pi_5^3$ の同型結論が (1), (2) の後へ移動
- $\pi_3^2$ 等の既存 backward reference を維持
- numbered reasoning 4 trio を維持
- $\pi_9^3$, $\pi_{10}^3$ の $\Delta$ に同型を追加しない
- map-property prose / exact-sequence / generator canonicalization に回帰なし
- full pytest は実行しない

## 次 Phase との境界

この repair は public equation-reference order のみを扱う。

semantic inference、Reference selection、$\Delta$ 同型規則、
$\eta_2$ 文言、stable 判定には触れない。
