# Phase 159-R1-6b repair2

## 変更対象

- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py`
  - `test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically()`

Production code:
- 変更なし

import:
- 変更なし

## 変更後テスト関数全体

```python
def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  injective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3} "
    r"\text{ は単射}. \tag{1}$"
  )
  surjective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3} "
    r"\text{ は全射}. \tag{2}$"
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

  assert (
    r"\tag{1}$ は単射."
    not in rendered
  )
  assert (
    r"\tag{2}$ は全射."
    not in rendered
  )

  assert (
    "(1), (2) より, "
    + isomorphism
    in rendered
  )
```

## 修正理由

R1-6b で numbering contract を意図的に変更した。

旧:
```text
$H: ...\tag{1}$ は単射.
```

新:
```text
$H: ... \text{ は単射}. \tag{1}$
```

旧 R1-4 テストだけが旧表示を要求していたため、
production を戻さず test expectation を現行 contract に合わせる。

## 完了条件

- R1-6 focused tests PASS。
- Phase 159 focused tests PASS。
- related literature/reference regressions PASS。
- `git diff --check` PASS。
- 実表示で `(1)` と `(2)` が property 全体に付く。
- `[R1] (5.1)` attribution を維持。
- full pytest は未実行。

## 次 Phase との境界

- production logic の変更なし。
- 次段では必要なら `[R1] より` / `完全性より` の本文 linkage を扱う。
