# Phase 166 R3 — 順序情報の読取専用監査

## 目的

復旧済みの $\pi_3^2$ 証明を維持し、共通探索の実運用登録情報で (5.1)、Proposition 5.1、関連する主張の順序情報が埋まっているか調べる。

## 現行 GitHub コードで確認したこと

- `phase163_r4_registry_bridge.py`: 文献構成要素には `component_position` が入るが、文献全体の `publication_position` と主張の `available_after_position` は設定されない。
- `phase165_goal_only_search.py`: 標準の `reconstruct_registered_goal` 呼び出しは `lookup_mode` を指定しない。
- `phase165_r3_recursive_search.py`: `legacy`、`typed_reference`、`typed_reference_ordered` の3モードが存在する。
- Web で成功した $\pi_3^2$ と標準の探索入口が同一経路とは、まだ確認できない。

## 変更対象

既存ファイル・クラス・メソッド・テストは変更しない。新規 `phase166_r3_order_audit/audit.py` に `collect()` と `main()`、`test_audit.py` に限定テスト3件を追加。`run.ps1` と本書、`README.md` を追加。

## 完了条件と次工程

限定 pytest 3件が PASS し、実際の登録順序の欠損状況を JSON に記録できること。次に Web 実経路を特定して、必要な順序登録・共通探索接続だけを修正する。独立確認による資格制度や群別アダプターは追加しない。全体 pytest は Phase 166 の末尾のみ。
