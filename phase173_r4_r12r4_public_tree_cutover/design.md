# Phase 173 R4-R12R4：公開 Narrative の証明木経路への切替

## 現行コードと既存テスト

GitHub `develop` の HEAD `188f707e1fcd8fde7b22af02a6b4005986fb3c1e` で、公開 Web adapter が `render_model_backed_narrative_markdown` の出力を `project_verified_toda56_narrative` により再構築していた。`phase173_r4_r13_narrative_audit/audit.py` は旧 Web の `$\Phi$` 表記の存在を検査していた。既存の専用 Projector への単体テストは公開経路とは独立している。

## 今回変更する対象

1. `phase165_r52_r3_web_adapter.py` の `build_partial_web_group_proof_view` 全体。変更後は既存の model-backed Renderer の出力をそのまま Web 行に変換する。クラス、import、推論部分は変更しない。
2. `phase173_r4_r13_narrative_audit/audit.py` の `inspect_dimension` 全体。各群の既存の推論規則、認証された DB prior、証明根、4件の引用を引き続き監査し、Web 文字列を特定の `$\Phi$` 表記ではなく共通 Renderer の実際の出力と比較する。
3. `phase173_r4_r13_narrative_audit/tests/test_audit.py` 全体。旧文章の存在ではなく出典・完成状態・Web 経路の契約を検査する。
4. 新規 `phase173_r4_r12r4_public_tree_cutover/install.py` と `tests/test_install.py`、`tests/test_public_contract.py`。追加位置は新規 Phase パッケージ内。

## 原則

証明探索 → Verified Proof Tree（検証済み証明木） → `ProofNarrativeModel` → 既存の model-backed Renderer → Web の順にする。公開 Web Adapter に文章の後段上書き、特定の群や生成元への分岐、証明されていない関係の追加を認めない。

モデルの Reference と ProofStep の内容は変更しない。先行 DB の引用は既存 `display_prior_reference_locator` を使い、記録された認証情報を維持する。

## 追加するテスト

- AST と全文検査：公開 Adapter に旧 Projector の import・呼び出しがないこと。
- 5群の live test：`complete`、Open Goals=0、証明根、引用4件と根への祖先関係、Web 表示が共通 Renderer の出力と一致すること。
- 既存 R4-R12 と R4-R13 の限定 pytest を実行。未証明の $\pi_{12}^4$ は R4-R12 既存テストにより引き続き拒否する。

## 意図的な未実施事項

中央 `phase168_r3_5_model_renderer.py` 内に残る球面次元固定の説明、過去の専用 Narrative 関数の物理削除、証明探索規則の一般化は本ステップで行わない。したがって本ステップだけで全体統一を宣言しない。次の R4-R12R5 は中央 Renderer の構造上の例外を型付き証明木から導出できる形に改め、構造ゲートを再実行する。

## 確認結果の取り扱い

本 ZIP 自体の静的検査は作成環境で行う。利用者のリポジトリ上での完成証明・Web の回帰 PASS は `run.ps1` の実行ログを受領するまで宣言しない。`DryRun` は本体を変更せず、通常実行だけが3ファイルを書き換える。限定 pytest が失敗した場合はロールバックを試みる。

## R4-R12R4R1：HEAD lineage 修正（2026-11-03）

最初の R4-R12R4 ZIP の `preflight()` は `HEAD == 188f707e` だけを許していた。その後、監査専用 R4-R12R3 が `382cef8b` にコミットされ、GitHub とローカルが一致しているにもかかわらず停止した。比較検証により、新コミットの変更が `phase173_r4_r12r3_architecture_audit/` と `.pytest_cache/v/cache/nodeids` だけであり、公開 Web adapter・R4-R13 audit・監査テストの対象 Git blob がすべて不変であることを確認した。

今回のインストーラー修正は `install.py` に `reviewed_head_lineage_allowed()` を追加し、`preflight()` の HEAD 完全一致判定を「GitHub とローカル HEAD の一致」「監査済み基点からの祖先関係」「その間のコミットが監査成果物と pytest キャッシュだけを変更」「対象3ファイルの既存 blob 完全一致」に改める。コード・文献・ProofStep・レンダラーの変更が間に入った場合は停止する。既存のインストーラーの適用・失敗時復元処理、3つの変更ファイル、公開経路の移行内容には触れない。

追加した限定テストは `test_reviewed_head_lineage_allows_only_audit_commit()` と `test_reviewed_head_lineage_rejects_production_changes()` の2件。修正版 ZIP は従前のパッケージと同じディレクトリ名に展開して上書きできる。R4-R12R4 の実リポジトリ上での限定 pytest / Web 完成確認はユーザー実行ログまで未確認として扱う。
