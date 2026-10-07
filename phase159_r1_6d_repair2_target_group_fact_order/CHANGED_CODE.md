# Phase 159-R1-6d repair2

## 変更対象

### production
- `toda_group_proof_narrative_renderer.py`
  - 新規 `_phase159_r1_6d_reorder_target_group_fact_after_surjectivity()`
  - `render_toda_group_proof_narrative_markdown()`

import:
- 変更なし

class:
- 変更なし

### tests
- 新規 `tests/test_phase159_r1_6d_target_group_fact_order.py`

## 新規 helper 全体

`render_toda_group_proof_narrative_markdown()` の直前に追加。

```python
def _phase159_r1_6d_reorder_target_group_fact_after_surjectivity(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  reference_number = (
    _phase159_r1_6c_reference_number(
      rendered,
      "(5.1)",
    )
  )

  if reference_number is None:
    return rendered

  all_steps = (
    _phase159_r1_6c_recursive_proof_steps(
      presentation.root_step
    )
  )

  for surjective_step in all_steps:
    if not isinstance(
      surjective_step.conclusion,
      TodaHopfInvariantSurjectiveStatement,
    ):
      continue

    target_group = (
      surjective_step.conclusion.map.target_group
    )

    target_group_step = next(
      (
        proof_step
        for proof_step in all_steps
        if (
          isinstance(
            proof_step.conclusion,
            Relation,
          )
          and proof_step.conclusion.lhs
          == target_group
          and (
            _phase159_r1_6c_step_reference_locator(
              proof_step
            )
            == "(5.1)"
          )
        )
      ),
      None,
    )

    if target_group_step is None:
      continue

    target_group_line = (
      "[R"
      + str(
        reference_number
      )
      + "] より, "
      + _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          target_group_step
        )
      )
    )

    source_paragraph = (
      target_group_line
      + "\n\n"
    )

    if source_paragraph not in rendered:
      continue

    rendered_surjective = (
      _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          surjective_step
        )
      )
    )

    match = re.match(
      r"^\$(?P<math>.+)\$ は全射\.$",
      rendered_surjective,
    )

    if match is None:
      continue

    display_prefix = (
      "\\[\n"
      + match.group(
        "math"
      )
      + r"\quad\text{は全射}. \qquad ("
    )

    display_start = rendered.find(
      display_prefix
    )

    if display_start < 0:
      continue

    display_end = rendered.find(
      "\n\\]",
      display_start,
    )

    if display_end < 0:
      continue

    display_end += len(
      "\n\\]"
    )

    source_index = rendered.find(
      source_paragraph
    )

    if source_index < 0:
      continue

    without_source = (
      rendered[
        :source_index
      ]
      + rendered[
        source_index
        + len(
          source_paragraph
        ):
      ]
    )

    if source_index < display_start:
      display_start = without_source.find(
        display_prefix
      )

      if display_start < 0:
        continue

      display_end = without_source.find(
        "\n\\]",
        display_start,
      )

      if display_end < 0:
        continue

      display_end += len(
        "\n\\]"
      )

    insertion = (
      "\n\n"
      + target_group_line
    )

    return (
      without_source[
        :display_end
      ]
      + insertion
      + without_source[
        display_end:
      ]
    )

  return rendered
```

## 変更後 `render_toda_group_proof_narrative_markdown()` 全体

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
  rendered = (
    _phase159_r1_6d_finalize_reference_and_linkage(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_6d_center_structural_formulas(
      rendered
    )
  )
  rendered = (
    _phase159_r1_6d_reorder_target_group_fact_after_surjectivity(
      presentation,
      rendered,
    )
  )

  return (
    _phase159_inject_foundational_reference_section(
      presentation,
      rendered,
    )
  )
```

## 新規テスト

```python
from toda_calculation_facade import (
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


def _phase159_r1_6d_repair2_pi3_2_presentation():
  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase159_r1_6d_target_group_fact_follows_surjectivity():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6d_repair2_pi3_2_presentation()
    )
  )

  surjective = (
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
  )
  target_group = (
    r"[R1] より, $\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
  )
  isomorphism = (
    r"(1), (2) より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
  )
  eta_definition = (
    r"$H(\eta_{2}) = \iota_{3}$ となる "
    r"$\eta_{2} \in \pi_{3}^{2}$ が一意に存在する."
  )

  assert surjective in rendered
  assert target_group in rendered
  assert isomorphism in rendered
  assert eta_definition in rendered

  assert (
    rendered.index(
      surjective
    )
    < rendered.index(
      target_group
    )
    < rendered.index(
      isomorphism
    )
    < rendered.index(
      eta_definition
    )
  )


def test_phase159_r1_6d_target_group_fact_is_not_before_surjectivity():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6d_repair2_pi3_2_presentation()
    )
  )

  zero_map = (
    r"完全性より, $\Delta: \pi_{3}^{3} "
    r"\to \pi_{1}^{1}$ は零写像."
  )
  target_group = (
    r"[R1] より, $\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
  )
  surjective = (
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
  )

  assert (
    rendered.index(
      zero_map
    )
    < rendered.index(
      surjective
    )
    < rendered.index(
      target_group
    )
  )
```

## 修正内容

Toda `(5.1)` 由来の group-structure fact のうち、
`TodaHopfInvariantSurjectiveStatement` の target group と一致するものを、
その全射 statement の直後へ移動する。

$\pi_3^2$ の場合は:

```text
完全性より,

H: pi_3^2 -> pi_3^3 は全射. (2)

[R1] より, pi_3^3 = Z{iota_3}.

(1), (2) より, H: pi_3^2 -> pi_3^3 は同型.
```

となる。

## 完了条件

- `(2)` より前に `pi_3^3 = Z{iota_3}` が出ない。
- `(2)` の直後に `[R1] より, pi_3^3 = Z{iota_3}`. が出る。
- その後に `(1), (2)` から H 同型。
- eta_2 定義はさらにその後。
- R1-6d / Phase159 focused / related regressions PASS。
- `git diff --check` PASS。
- full pytest は未実行。

## 次 Phase との境界

今回変更するのは public proof order のみ。
Reference 内容、E 同型導出、完全列中央揃え、式番号表示、proof DAG は変更しない。
