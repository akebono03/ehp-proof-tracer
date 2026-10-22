# Phase 167 R4-⑩ — Shared Reference consumers

R4-⑨ 適用後を前提とする限定修正です。同じ文献 Reference から直接導出された複数の可視 ProofStep に同一の引用番号を付けます。零群専用の分岐や規則名検索は追加しません。出典側 GIVEN と結論側 INFERENCE の実際の一前提依存関係を使用します。

対象ファイル: `toda_group_proof_narrative_contribution_renderer.py`。
対象関数: `link_toda_group_proof_narrative_reference_body_consumers`。`patch.py` は AST で関数境界を特定し、R4-⑨ の該当区間だけ置換します。既存バージョンが一致しなければ中止します。`modified_function_full.py` に変更後の関数全文を出力し、バックアップを保存します。

実行: リポジトリ直下で `powershell -ExecutionPolicy Bypass -File .\phase167_r4_10_multi_reference_consumers\run.ps1`。

限定検証: (5.1) 由来の $\pi_5^5=\mathbb Z\{\iota_5\}$ と $\pi_4^5=0$ の両方に同一 Reference が付くこと、既存表示が保持されること。全体 pytest は Phase 167 終了時にのみ実施します。

範囲: 直接の単一前提による導出に限ります。多段・複数前提の Reference 伝播や証明探索は変更しません。
