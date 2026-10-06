# Phase 159-R1-6c repair2

## 変更対象

- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py`
  - `test_phase159_r1_4_pi3_2_public_uses_exactly_one_exact_sequence()`

Production code:
- 変更なし

import:
- 変更なし

## 変更後テスト関数全体

```python
def test_phase159_r1_4_pi3_2_public_uses_exactly_one_exact_sequence():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  long_exact = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}$."
  )

  proof_body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  exactness_lines = tuple(
    line
    for line in proof_body.splitlines()
    if r"\xrightarrow{" in line
  )

  assert exactness_lines == (
    long_exact,
  )
  assert "は完全である." not in proof_body
```

## 修正理由

R1-6c で、完全列導入文

```text
... 次の完全列を考える.
```

の直後にある列から、重複する

```text
は完全である.
```

を削除した。

R1-4 のテスト目的は「完全列が public proof body にちょうど1本だけあること」であり、
`は完全である.` の有無そのものではない。

したがって期待値を

```text
... pi_2^2$.
```

へ更新し、あわせて

```python
assert "は完全である." not in proof_body
```

を追加する。

## 完了条件

- R1-6c focused PASS
- R1-6a/R1-6b PASS
- Phase159 focused PASS
- related regressions PASS
- git diff --check PASS
- full pytest 未実行
