# Phase 169 R10EF — 1-stem 重複導出の由来監査

## 位置づけ

R10EE では $\pi_5^4$ と $\pi_6^5$ が `partial` であり、登録された型付き Goal は各1件だが、同じ目標の導出が2件残ることを確認した。R10EE 末尾の Git 状態不一致については、変更されたパスがログに記録されなかったため、監査が本番コードを変更したと断定しない。

## 監査の構成

既存の `phase165_r3_recursive_search.append_unique_verified_derivation()` を直接置換するのではなく、実際の探索中に `unittest.mock.patch.object()` で観測ラッパーを一時的に呼び、**必ず元の関数へ委譲**する。元の関数が候補を残したかを、元の関数の呼び出し前後の候補数から記録する。選択・除外・追加推論は行わない。

新規 `trace.py` の `AppendObservation`、`is_exact_goal_conclusion()`、`forward_and_observe()`、`pairwise_kept_indices()` は観測用のみに使用する。新規 `audit.py` は既存の Backward Search（逆向き証明探索）を `n=4,5; k=1` について実行し、根に向かう候補と GIVEN の参照情報を報告する。既存の `same_completed_proof_tree()` と `same_cited_scalar_specialization()` の結果も比較するが、その判定を使って新たな同一視を行うことはない。

追跡ファイルの Git 状態は実行前後にパス付きで保存する。変化を検出した場合は安全側で終了し、何が変化したかを印字する。`git reset`、`git checkout`、差分の自動削除は行わない。

## 変更対象

既存本番ファイル、既存テスト、プロジェクト文書は変更なし。新規ファイルは `__init__.py`、`trace.py`、`audit.py`、`run.ps1`、`tests/test_r10ef_trace.py`、`README.md`、`DESIGN_JA.md`。import およびすべての新規関数・クラスのコード全文をそれぞれのファイルに記録する。

## 完了条件と次 Phase 境界

2つの群それぞれで、採用候補の由来、ルートとなる証明木の比較、文献祖先が観測できること。限定 pytest が PASS し、Git の追跡ファイル状態が実行前後で変化しないこと。`partial` は `partial` として記録する。**根拠に基づく次の最小修正が決まるまでは Phase 169 を完了としない。** 全体 pytest は Phase 169 の最後のみ実施する。
