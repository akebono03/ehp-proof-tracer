# Phase 159-R1-7b repair8

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7b_exactness_step_latex`
  - `_phase159_r1_7b_inline_exactness_latex`

### Tests
新規変更なし。repair4 までに更新した focused tests を再利用する。

## import

production import の変更はありません。

`render_toda_primary_group_latex` と
`TodaProp42ExactnessStatement` は既に import 済みです。

## 変更後 `_phase159_r1_7b_exactness_step_latex`

```python
def _phase159_r1_7b_exactness_step_latex(
  proof_step: ProofStep,
) -> str | None:
  statement = proof_step.conclusion

  if not isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    return None

  window = statement.window

  return (
    render_toda_primary_group_latex(
      window.source_term
    )
    + r" \xrightarrow{"
    + window.first_map.name
    + r"} "
    + render_toda_primary_group_latex(
      window.middle_term
    )
    + r" \xrightarrow{"
    + window.second_map.name
    + r"} "
    + render_toda_primary_group_latex(
      window.target_term
    )
  )
```

## 変更後 `_phase159_r1_7b_inline_exactness_latex`

```python
def _phase159_r1_7b_inline_exactness_latex(
  line: str,
) -> str | None:
  stripped = line.strip()
  verbose_suffix = "$ は完全である."

  if (
    stripped.startswith(
      "$"
    )
    and stripped.endswith(
      verbose_suffix
    )
  ):
    latex = stripped[
      1:-len(
        verbose_suffix
      )
    ]
  elif (
    stripped.startswith(
      "$"
    )
    and stripped.endswith(
      "$."
    )
  ):
    latex = stripped[
      1:-2
    ]
  elif (
    stripped.startswith(
      "$"
    )
    and stripped.endswith(
      "$"
    )
  ):
    latex = stripped[
      1:-1
    ]
  else:
    return None

  if latex.count(
    r"\xrightarrow{"
  ) < 2:
    return None

  if not latex.startswith(
    r"\pi_{"
  ):
    return None

  return latex
```

## 修正理由

repair7 runtime diagnosis で以下を確認した。

1. `TodaProp42ExactnessStatement` は多数存在するが、
   `_phase159_r1_7b_exactness_step_latex()` がすべて `None`。
2. baseline pi11_4 の visible E-H exactness は
   `$...$.`
   形式であり、現行 inline parser は `None`。

原因1:
旧 helper は `_render_generic_narrative_step()` が純粋な `$...$`
を返す前提だったが、実際には
`$...$ は完全である.`
という prose を返すため、開始/終了 `$` 判定に失敗した。

修正:
`TodaProp42ExactnessStatement.window` の typed data から
exactness LaTeX を直接生成する。

原因2:
public rendering pipeline の後段で `は完全である` が除去された
exactness line が `$...$.` として残る経路がある。

修正:
二本以上の `\xrightarrow{...}` を持ち `\pi_{...}` から始まる
pure inline chain について `$...$.` も exactness として認識する。

## 実行する pytest

- `tests/test_phase159_r1_7b_exact_sequence_display_order.py`
- `tests/test_phase157_r20_repair37_short_exact_after_map_support.py`
- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests/test_phase148_rc2_3_exactness_exposure.py`
- `tests/test_phase148_rc2_3_repair_r1.py`

full pytest は Phase 159 最後まで実行しない。

## 完了条件

- typed H-Delta exactness smoke check PASS。
- runtime `$...$.` parser smoke check PASS。
- focused tests PASS。
- pi6_3 short exact sequence display math 維持。
- pi11_4 H-Delta exactness を Delta 全射の前に display math。
- pi11_4 E-H exactness を display math。

## 次 Phase との境界

R1-7b repair8 では exact-sequence display/order のみ。

未着手:
- pi6_3 の `2ν'` 連続等式統合
- equation numbering policy
- Reference aggregate suppression
- map-property prose 全体統一
