# Phase 159 R1-7c R4 exact-sequence suppression repair2 fix2

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

import の変更はありません。

変更関数:
- `merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows`

repair1/fix2 で入った early suppression（前段抑制）を除去し、
GitHub 現行版へ戻します。

変更後の関数全体:

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

      introduction_index = (
        bare_indices[
          0
        ]
        if len(
          bare_indices
        ) == 1
        else None
      )

      removal_indices = {
        left_index,
        right_index,
      }

      if introduction_index is not None:
        removal_indices.add(
          introduction_index
        )
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

### 維持するもの

新規 helper:
- `suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements`

public contribution renderer の後段 call はそのまま維持します。

テスト変更はありません。

## 完了条件

- helper contract: PASS
- $\pi_3^2$ focused regression: PASS
- $\pi_6^3$ existing exactness regression: PASS
- generator canonicalization regression: PASS
- $\eta_2$ 文言変更なし
- full pytest は実行しない

## 次 Phase との境界

exact-sequence duplication の修正だけを扱います。
Reference、prose、stable 判定、generator 表記には触れません。
