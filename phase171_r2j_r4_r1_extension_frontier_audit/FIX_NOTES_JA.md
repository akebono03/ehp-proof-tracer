# Phase 171 R2J-R4-R1 R1 — 監査テスト修正

## 修正原因

監査コード `_generator_image_goal()` が `Composition.is_type_compatible()` によって三重合成を判定していた。現行の `Composition.is_type_compatible()` は左右の因子を `HomotopyElement` / `Suspension` / `IteratedSuspension` に限定するため、`Composition(eta3, Composition(eta4, eta5))` を拒否する。

旧テストでは `FiniteCyclicGroup(2, eta2)` を $\pi_5^2$ の群構造と見なしていたが、$\eta_2$ の型は $S^3 \to S^2$ であり、$\pi_5^2$ の生成元 $\eta_2^3=\eta_2\circ\eta_3\circ\eta_4$（$S^5\to S^2$）ではない。

## 変更対象と変更単位

- `audit.py`：import 全体、`_generator_image_goal()` 関数全体を変更した。その他の関数は変更しない。
- `tests/test_audit.py`：`test_generator_image_requires_well_typed_double_and_source()` 関数全体を変更した。既存のほかの3テストは変更しない。
- `CODE_FULL_JA.md`：上記2ファイルの全文を掲載した。
- `README.md`（英語）・`監査仕様.md`（日本語）：検証対象を正確に説明した全文を収録した。
- 本番コード、既存の本番テスト、`expression.py`、プロジェクト直下の文書は変更しない。

`_endpoints()`（既存の `phase169_r10e5_composite_generator_image.rule`）で、各複合写像の始域・終域を再帰的に検証する。対象は `E: π_5^2 → π_6^3` の GeneratorImage 候補のみであり、証明済みという宣言はしない。

## 検証状況

- `audit.py` と `tests/test_audit.py` の Python 構文検査：PASS。
- 修正対象関数と既存 `_endpoints()` と同等の型モデルを用いた単独テスト：PASS。
- Windows 実リポジトリでの pytest 4件・証明木監査：未実行。

## 次の段階との境界

R2J-R4-R1 は読み取り専用監査であり、$\pi_6^3\cong\mathbb Z/4\{\nu'\}$ の完成証明や新規 GIVEN は導入しない。限定 pytest 4件と `audit.json` 作成が成功すれば本監査を完了とする。全体 pytest は Phase 171 終了時に限る。
