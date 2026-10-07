# Phase 159 R1-7c R4 exact-sequence subsequence suppression repair1

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

import の変更はありません。

変更関数:
- `merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows`

変更関数全体:

```python
def merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  exactness_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if classify_toda_proof_step_role(
      node.proof_step
    )
    is TodaProofDependencyRole.EHP_EXACTNESS
  )

  for left_step in exactness_steps:
    left_window = getattr(
      left_step.conclusion,
      "window",
      None,
    )

    if left_window is None:
      continue

    for right_step in exactness_steps:
      if right_step is left_step:
        continue

      right_window = getattr(
        right_step.conclusion,
        "window",
        None,
      )

      if right_window is None:
        continue

      if not (
        left_window.middle_term
        == right_window.source_term
        and left_window.target_term
        == right_window.middle_term
        and _toda_group_proof_narrative_map_name_latex(
          left_window.second_map
        )
        == _toda_group_proof_narrative_map_name_latex(
          right_window.first_map
        )
      ):
        continue

      left_line = (
        _render_generic_narrative_step(
          left_step
        )
      )
      right_line = (
        _render_generic_narrative_step(
          right_step
        )
      )

      left_index = next(
        (
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if paragraph.strip()
          == left_line.strip()
        ),
        None,
      )
      right_index = next(
        (
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if paragraph.strip()
          == right_line.strip()
        ),
        None,
      )

      if (
        left_index is None
        or right_index is None
      ):
        continue

      first_map = (
        _toda_group_proof_narrative_map_name_latex(
          left_window.first_map
        )
      )
      second_map = (
        _toda_group_proof_narrative_map_name_latex(
          left_window.second_map
        )
      )
      third_map = (
        _toda_group_proof_narrative_map_name_latex(
          right_window.second_map
        )
      )

      if None in (
        first_map,
        second_map,
        third_map,
      ):
        continue

      bare_sequence = (
        "$"
        + render_toda_primary_group_latex(
          left_window.source_term
        )
        + r" \xrightarrow{"
        + first_map
        + "} "
        + render_toda_primary_group_latex(
          left_window.middle_term
        )
        + r" \xrightarrow{"
        + second_map
        + "} "
        + render_toda_primary_group_latex(
          left_window.target_term
        )
        + r" \xrightarrow{"
        + third_map
        + "} "
        + render_toda_primary_group_latex(
          right_window.target_term
        )
        + "$"
      )
      merged = (
        bare_sequence
        + " は完全である."
      )

      bare_indices = tuple(
        index
        for index, paragraph in enumerate(
          paragraphs
        )
        if paragraph.strip().rstrip(
          "."
        )
        == bare_sequence
      )

      sequence_core = bare_sequence[
        1:
        -1
      ]
      sequence_arrow_count = (
        sequence_core.count(
          r"\xrightarrow{"
        )
      )
      containing_longer_indices = tuple(
        index
        for index, paragraph in enumerate(
          paragraphs
        )
        if (
          sequence_core
          in paragraph.strip()
          and paragraph.count(
            r"\xrightarrow{"
          )
          > sequence_arrow_count
        )
      )

      removal_indices = {
        left_index,
        right_index,
      }
      removal_indices.update(
        bare_indices
      )

      if containing_longer_indices:
        for index in sorted(
          removal_indices,
          reverse=True,
        ):
          paragraphs.pop(
            index
          )

        return "\n\n".join(
          paragraphs
        )

      introduction_index = (
        bare_indices[
          0
        ]
        if len(
          bare_indices
        ) == 1
        else None
      )

      if introduction_index is not None:
        insertion_index = (
          introduction_index
        )
      else:
        insertion_index = min(
          left_index,
          right_index,
        )

      for index in sorted(
        removal_indices,
        reverse=True,
      ):
        paragraphs.pop(
          index
        )

      removed_before_insertion = sum(
        1
        for index in removal_indices
        if index < insertion_index
      )
      insertion_index -= (
        removed_before_insertion
      )

      paragraphs.insert(
        insertion_index,
        merged,
      )

      return "\n\n".join(
        paragraphs
      )

  return markdown
```

### `tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py`

新規ファイルです。import を含む全文:

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


def _pi3_2_public_narrative() -> str:
  report = build_standard_toda_report(
    n=2,
    k=1,
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


def test_phase159_r1_7c_r4_pi3_2_keeps_only_longer_exact_sequence():
  rendered = _pi3_2_public_narrative()
  paragraphs = tuple(
    paragraph.strip()
    for paragraph in rendered.split(
      "\n\n"
    )
  )

  longer = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}$."
  )
  shorter = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1}$."
  )

  assert longer in paragraphs
  assert shorter not in paragraphs


def test_phase159_r1_7c_r4_pi3_2_keeps_injective_surjective_structure():
  rendered = _pi3_2_public_narrative()

  assert (
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    in rendered
  )
  assert "は単射" in rendered
  assert "は全射" in rendered
  assert "(1), (2) より" in rendered
  assert "は同型" in rendered


def test_phase159_r1_7c_r4_pi3_2_eta2_wording_is_unchanged():
  rendered = _pi3_2_public_narrative()

  assert (
    "この同型写像により"
    in rendered
  )
  assert (
    r"H(\eta_{2})=\iota_{3}"
    in rendered
    or r"H\left(\eta_{2}\right)=\iota_{3}"
    in rendered
    or r"H\left(\eta_{2}\right) = \iota_{3}"
    in rendered
  )
  assert (
    r"\eta_{2}"
    in rendered
  )
```

## 完了条件

- $\pi_3^2$ public Narrative で長い EHP 完全列を維持する。
- その中に含まれる短い部分完全列を再表示しない。
- 単射 $(1)$、全射 $(2)$、$(1),(2)$ から同型、という流れを維持する。
- $\eta_2$ の現在の文言を変更しない。
- 既存 $\pi_6^3$ exactness merge regression を壊さない。
- generator canonicalization regression を壊さない。
- 全体 pytest は実行しない。

## 次 Phase との境界

この repair は exact-sequence presentation（完全列表示）の重複抑制だけを扱う。
$\eta_2$ の文言、stable 判定、他の prose refinement は扱わない。
