# Phase 159 R1-7c R4 generator canonicalization repair1 fix2

## 変更対象

production code の変更はありません。

### `tests/test_phase157_r20_generic_dependency_rendering.py`

import の変更はありません。

変更テスト関数全体:

```python
def test_phase157_r20_reference_dependencies_are_recovered_from_graph():
  rendered = _render_pi6_3_r20()

  for reference in (
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "(5.7)",
  ):
    assert reference in rendered
```

## 変更理由

現行 design では structural Reference attribution（構造的参照帰属）は
explicit `[Rk]` marker（明示的参照マーカー）がなくても成立する。

したがって、

```python
rendered.index("[R5]より") < rendered.index("[R3]より")
```

は現在の contract を表していない stale expectation（古い期待値）である。

## 完了条件

- 5件の current Reference が存在する
- `pi_7^5 = Z/2{eta_5^2}` の canonicalization が維持される
- Phase 143 / Phase 59 / Phase 159 focused regression がすべて PASS
- full pytest は実行しない
