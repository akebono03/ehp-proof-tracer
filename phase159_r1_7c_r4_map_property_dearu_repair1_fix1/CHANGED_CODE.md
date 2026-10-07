# Phase 159 R1-7c R4 map-property `である` repair1 fix1

## 変更対象

production code の変更はありません。

### test

`tests/test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py`

import の変更はありません。

変更テスト関数全体:

```python
def test_phase159_r1_7c_r4_pi11_6_uses_concise_map_property_prose():
  rendered = _public_narrative(
    6,
    5,
  )

  assert (
    r"$\Delta: \pi_{10}^{9} \to \pi_{8}^{4}$ は単射."
    in rendered
  )
  assert (
    r"$E: \pi_{9}^{4} \to \pi_{10}^{5}$ は全射."
    in rendered
  )
  assert (
    r"[R1]より, $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射."
    in rendered
  )
```

## 修正理由

repair1 の production normalization は正常に動作している。

失敗したのは Reference prefix（参照接頭辞）の stale expectation（古い期待値）のみ。

旧期待:
`[R1] より,`

現行 public contract:
`[R1]より,`

GitHub の現行 Phase157/158 出力も後者で統一されているため、test expectation のみ修正する。

## 完了条件

- map-property focused regression PASS
- $\pi_3^2$ exact-sequence regression PASS
- $\pi_6^3$ exactness display regression PASS
- generator canonicalization regression PASS
- production code 追加変更なし
- full pytest は実行しない

## 次 Phase との境界

この fix は stale Reference-prefix expectation の修正のみ。
Reference の意味内容、map-property semantic data、exact-sequence、$\eta_2$、stable 判定には触れない。
