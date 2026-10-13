# Phase 165 R14-R27

## 変更対象
新規 `phase165_r14_r27_scope_delta.py` の `ScopeEvidence`、`inspect_scope_context`、`conditional_exactness_step`、`audit_r27`。関連テスト6件と `audit.py`、`run.ps1`。既存のファイル・推論規則を変更しない。

## 検証
採用 TeX の Proposition 4.2 を型付き化した R26 と R24 の懸垂同型の接続状態を再利用する。TeX がルートの `Toda_01.tex` に存在すれば Proposition 4.2 の周辺文を記録し、範囲除外の可能性を検出する。ただし前後の短い文字列は定理の全仮定ではなく、**n=1 を自動承認しない**。テストは明示的承認を模擬して ProofStep が生成可能なことだけを確認する。

## 完了条件
対象6テスト・原文がない場合の保護・仮定なしの ProofStep 不生成。実証されていない n=1 の EHP 適用を根拠に Δ=0 と宣言しない。

## 次 Phase 境界
実際の Toda 原文で Proposition 4.2 の前提範囲を確定し、条件を満たす場合のみ R24 の導出を実行する。全体 pytest は Phase 165 の最後にのみ実施。
