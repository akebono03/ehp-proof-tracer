# Phase 172 R3R1R1：コミット済み Renderer 対応の修正計画

## 前提・原因

R2R1 は成功済みである。R3R1 は `preflight()` でコミット済み Renderer の blob が R2 適用前 `94996b403f1c01f81319824565db422463714f02` に等しいことを要求して失敗した。GitHub `develop` の現行 `phase168_r3_5_model_renderer.py` の blob は、R2 適用後 `bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95`。実装上の誤った前提であり、数学的証明失敗ではない。

## 変更範囲

既存の本番ソース・Proof Tree・Reference・Renderer 変更なし。今回置換するのは ZIP 由来の未追跡ファイル `phase172_r3r1_hopf_chain_audit/audit.py` の `preflight()` 全体である。定数 `EXPECTED_COMMITTED_R2_RENDERER_BLOB` と補助関数 `reviewed_renderer_installation()` を追加する。新規修正パッケージ内の `install.py`・`run.ps1`・6件の限定テストを追加する。既存 import は変更しない。

## 内容ガード

コミット側の状態として、(1) R2 以前の固定 blob と、そのバイト列に既知の `transformed()` を適用した作業ツリー、(2) R2 適用済みの固定 blob と完全一致する作業ツリー、のみ許可する。CRLF/LF は正規化して比較する。未知の blob や作業ツリー差分は拒否する。R2R1 の `projection.py` とテストの hash 検査、ブランチ `develop`、リモート HEAD 検査は維持する。

## テスト・完了条件

新規6件の限定 guard テスト、既存 R3R1 の3グループの限定 pytest、実際の Backward Search `complete`、未解決 Goal 0、Web `generic-complete-proof`、Reference 8件、作業ツリー非変更。失敗時は監査ファイルを復元し、ログを外部出力する。全体 pytest は Phase 172 終了時のみ実行。R3 本実装、R4、R5 は先取りしない。
