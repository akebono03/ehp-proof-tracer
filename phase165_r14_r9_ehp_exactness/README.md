# Phase 165 R14-R9 — EHP 完全性からの一般 Hopf 推論

変更対象: 新規 `phase165_r14_r9_ehp_exactness.py`（全クラス・関数を含む）、`test_phase165_r14_r9_ehp_exactness.py`、`audit.py`、`run.ps1`。既存コード変更なし。

## 実装内容
- `hopf_injective_from_exactness_rule()`: 直前の群が零、かつ E→H の完全性があれば H 単射。
- `hopf_surjective_from_exactness_rule()`: H→Δ の完全性と Δ=0 があれば H 全射。
- `expand_generic_ehp_hopf_goal()`: EHP の次数を満たす Hopf 写像で一般的な部分目標を返す。
- `audit_pi32_hopf_exactness()`: π₃² の2枝に残された部分目標を出力する。

出典認証、Registry 検証、旧証明の再利用は行わない。
テストの GIVEN は検証専用 fixture であり、実際の命題の証明ではない。

## 完了条件
関連テスト8件が通過すること、単射・全射の2枝を構築できること、異なる完全列や Delta を混同しないこと、未認証の証明が生成されないこと。

## 次工程との境界
Toda (5.1) の `π₂¹=0` を現行 `TodaPrimaryGroupZeroStatement` に対応付けること、π₃³→π₁¹ の Δ=0 に根拠を与えること、必要な完全性を認証・登録すること。R14-R9 の成果だけでは π₃² の証明は完成しない。
