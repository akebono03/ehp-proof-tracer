# Phase 175 R4R14R4 実装・監査計画

## 対象

- 新規 `phase175_r4r14r4_general_zero_transport/rule.py`: `composite_value_zero_inputs`、`proved_composite_zero_image_rule`、`expand_proved_composite_zero_image`
- 新規 `tests/test_rule.py`: 一般性、推論依存関係、無効入力、偽 GIVEN 排除を限定テスト
- 新規 `run.ps1`: Git blob 固定値と限定 pytest

## 数学的意味

別途証明された $E(g)=c$ と $c=0$ から $E(g)=0$ を推論する。$c$ は2因子以上の任意の適切に型付けされた合成を許す。結論や出典を直接登録しない。

## 境界

この段階は独立した一般規則のみ。共有 Provider、Web、既存規則を変更せず、$\pi_{10}^6=0$ の完成を主張しない。R4R14R5 以降で、型付き Toda (5.9) と探索の接続、EHP 完全性を確認する。全体 pytest は実施しない。
