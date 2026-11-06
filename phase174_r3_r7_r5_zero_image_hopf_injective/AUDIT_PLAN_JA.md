# Phase 174 R3-R7-R5 監査計画

## 監査前に確認した現行コード・関連テスト

GitHub `akebono03/ehp-proof-tracer`、`develop`、`1f3a61d7d6cfc7854e56c4f5c372bf5c71e203df` を確認。

- `sources/toda/Toda_05_2.tex` の Proposition 5.9 証明。
- `map_property_rules.py` の `ImageZeroStatement`。
- `phase165_r12_r11_prop42_unified.py` の `prop42_exactness_indices`。
- `phase165_r14_r9_ehp_exactness.py` の Hopf 単射性一般規則。
- `phase165_r12_r12_ehp_consequences.py` の EHP 完全列の帰結。
- `phase165_r14_r6_generic_iso.py` の `MapInjective`。
- `phase165_r52_r9_shared_math.py` の共通証明探索 provider。
- `phase174_r3_r7_r3_ehp_zero_rule/rule.py` および関連テスト。
- 関連テスト `tests/test_map_property_rules.py`、`phase165_r14_r9_ehp_exactness/test_phase165_r14_r9_ehp_exactness.py`、`phase165_r12_r12_ehp_consequences/tests/test_phase165_r12_r12_ehp_consequences.py`。

## 数学的契約

EHP の完全性により $\operatorname{im}(E)=\ker(H)$。したがって $\operatorname{im}(E)=0$ なら $H$ は単射になる。この推論は $E$ の定義域が零であることを必要としない。

Toda の転写には $\pi_{10}^{5}\cong \mathbb Z/2$ および $E\pi_{10}^{5}=0$ の双方が記載されている。これは別々の主張であり、転写の確認だけではどちらも VERIFIED ProofStep ではない。

## 変更対象と Phase の境界

変更対象は新規 `phase174_r3_r7_r5_zero_image_hopf_injective/` のみ。`rule.py` に一般規則を追加するが、共通 provider・Web・既存データベースには接続しない。

`ImageZero(E)` と $E\to H$ の型付き完全性はそれぞれ独立 Goal とする。`ImageZero(E)` の出典からの証明接続、$\pi_{11}^{6}$ の生成元と $\Delta$ 全射性の証明は次段階以降に残す。

## 完了条件

- 新規および関連限定 pytest が PASS。
- DryRun と本監査の Source Guard が PASS。
- 一般的な Root 候補が1件、2つの前提 Goal が分離。
- 未証明の `ImageZero(E)` が GIVEN として混入しない。
- 新規の group GIVEN / production rules が各0、Web 経路変更なし。
- 全体 pytest 未実施。
