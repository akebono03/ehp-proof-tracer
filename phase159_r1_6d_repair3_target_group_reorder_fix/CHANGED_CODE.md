# Phase 159-R1-6d repair3

## 変更対象

### production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_6d_reorder_target_group_fact_after_surjectivity()`

import:
- 変更なし

class:
- 変更なし

tests:
- 変更なし

## 変更後 helper 全体

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
    target_group_latex = (
      render_toda_primary_group_latex(
        target_group
      )
    )

    rendered_surjective = (
      _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          surjective_step
        )
      )
    )

    surjective_match = re.match(
      r"^\$(?P<math>.+)\$ は全射\.$",
      rendered_surjective,
    )

    if surjective_match is None:
      continue

    display_prefix = (
      "\\[\n"
      + surjective_match.group(
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

    target_group_pattern = re.compile(
      r"^\[R[0-9]+\] より, \$"
      + re.escape(
        target_group_latex
      )
      + r" = .+\$\.$",
      flags=re.MULTILINE,
    )

    target_group_match = (
      target_group_pattern.search(
        rendered
      )
    )

    if target_group_match is None:
      continue

    target_group_line = (
      target_group_match.group(
        0
      )
    )

    if (
      target_group_match.start()
      > display_end
    ):
      continue

    source_start = (
      target_group_match.start()
    )
    source_end = (
      target_group_match.end()
    )

    while (
      source_end < len(
        rendered
      )
      and rendered[
        source_end
      ]
      == "\n"
    ):
      source_end += 1

    without_source = (
      rendered[
        :source_start
      ]
      + rendered[
        source_end:
      ]
    )

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

    return (
      without_source[
        :display_end
      ]
      + "\n\n"
      + target_group_line
      + without_source[
        display_end:
      ]
    )

  return rendered
```

## 修正理由

repair2 では target group の group fact 自体に `(5.1)` locator が直接付いていることを要求していた。

実際の public Narrative では

```text
[R1] より, pi_3^3 = Z{iota_3}.
```

と正しく linkage されていても、その個別 Relation step に locator が直接付いているとは限らない。

repair3 では:

1. `TodaHopfInvariantSurjectiveStatement` から target group を取得。
2. その target group の LaTeX を生成。
3. public body の
   `[Rk] より, $<target group> = ...$.`
   を検索。
4. それが全射式より前にある場合だけ削除。
5. 全射 display math の直後へ再挿入。

これにより `pi_3^3` をハードコードしない。

## 完了条件

- ordering focused 2 tests PASS。
- R1-6d focused PASS。
- R1-6a/b/c + Phase159 focused PASS。
- related regressions PASS。
- `git diff --check` PASS。
- full pytest は未実行。

## 次 Phase との境界

public proof order のみ修正。
Reference 内容・proof DAG・inference rule は変更しない。
