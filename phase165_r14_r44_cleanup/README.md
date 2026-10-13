# Phase 165 R44 — 不要な後付け Renderer の撤去

変更対象は `toda_group_proof_narrative_renderer.py` の末尾の公開関数 `render_toda_group_proof_narrative_markdown` と、R43 で追加した `phase165_r14_r43_reference_reason.py` です。

- R43 の後処理呼び出しを撤去し、共通 Renderer が生成した文章をそのまま返す。
- 使われなくなった R43 専用モジュールを `.phase165_r44_removed.py` に退避する（内容は削除せず復旧可能にする）。
- R38 の Registry、R41 の Replay、R42 の型付き表示と出典 metadata、従来の参照処理は変更しない。
- `cleanup.py` は同じ状態に繰り返し実行可能。未知の構造を検出した場合は中止する。

対象 `pytest` は5件。全体 pytest は実行しない。

完了条件：R43 追加フックがなくなり、R42 の変更が保持される。**一般形 Reference の自動表示が復旧したことは、この作業だけでは保証しない。** その接続は、Registry Statement ID と従来の固定文献命題 component classifier の対応を現行コードで監査してから修正する。
