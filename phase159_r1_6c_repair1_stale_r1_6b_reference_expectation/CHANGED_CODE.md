# Phase 159-R1-6c repair1

## 変更対象

- `tests/test_phase159_r1_6b_toda51_attribution.py`
  - `test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry()`

Production code:
- 変更なし

import:
- 変更なし

## 変更後テスト関数全体

```python
def test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry():
  presentation = (
    _phase159_r1_6b_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  reference_section = (
    rendered.split(
      "## 使用する結果\n\n",
      1,
    )[1].split(
      "\n---\n",
      1,
    )[0]
  )

  assert (
    reference_section.count(
      "**[R1] (5.1).**"
    )
    == 1
  )
  assert "[F1]" not in reference_section
  assert "[F2]" not in reference_section
  assert "[F3]" not in reference_section

  assert (
    r"\pi_{3}^{2} = "
    r"\mathbb{Z}\{\eta_{2}\}"
    not in reference_section
  )
  assert (
    "Proposition 5.1"
    not in reference_section
  )
```

## 修正理由

R1-6b の責務は `(5.1)` attribution の統合であり、
Reference 本文の具体的表示は R1-6c で source-faithful general form に変更した。

旧 R1-6b test は以下の specialization を直接要求していた。

```text
pi_2^1 = 0
pi_3^3 = Z{iota_3}
E:pi_1^1->pi_2^2 isomorphism
```

R1-6c では Reference を Toda (5.1) 原文に対応する一般式へ変更したため、
これらの具体形は R1-6b test の責務ではなくなった。

R1-6b test は以下だけを検証する。

- `[R1] (5.1)` が単一 entry
- `[F1]`〜`[F3]` がない
- target が Reference にない
- Proposition 5.1 に誤帰属しない

一般式の正確な内容は R1-6c focused test が検証する。

## 完了条件

- R1-6c focused PASS
- R1-6a/R1-6b PASS
- Phase159 focused PASS
- related regressions PASS
- git diff --check PASS
- full pytest 未実行
