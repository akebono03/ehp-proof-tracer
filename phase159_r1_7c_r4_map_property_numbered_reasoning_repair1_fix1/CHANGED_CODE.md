# Phase 159 R1-7c R4 numbered map-property reasoning repair1 fix1

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
    r"[R1]より, $H: \pi_{7}^{3} \to \pi_{7}^{5}\tag{1}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}\tag{2}$ は全射."
    in rendered
  )
```

## 修正理由

numbered-reasoning repair1 自体は 4 tests PASS。

失敗したのは、前段 map-property prose regression が
$\pi_{11}^6$ の旧 unnumbered（番号なし）表示を期待していたため。

旧:
`[R1]より, $H: ...$ は単射.`
`$H: ...$ は全射.`

現行:
`[R1]より, $H: ...\tag{1}$ は単射.`
`$H: ...\tag{2}$ は全射.`

よって test expectation のみ現行 public contract に更新する。

## 実行する pytest

- `tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`
- `tests/test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py`
- `tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py`
- `tests/test_phase157_r20_repair32_exactness_intro_anchor.py`
- `tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py`

## 完了条件

- numbered-reasoning focused regression PASS
- map-property prose regression PASS
- exact-sequence regression PASS
- exactness display regression PASS
- generator canonicalization regression PASS
- production code 追加変更なし
- full pytest は実行しない

## 次 Phase との境界

この fix は stale test expectation（古いテスト期待値）の修正のみ。
semantic inference、Reference、$\Delta$ 同型規則、$\eta_2$ 文言、stable 判定には触れない。
