# Phase 168 R3-8 — 追加コードと境界

- 追加ファイル: `phase168_r3_8_citation_origin.py`（リポジトリ直下）
  - 新規クラス `CitationOrigin`、`CitationOriginReport`
  - 新規関数 `inspect_citation_origins`
- 追加位置: 既存の `phase168_r3_4_link_bridge.py` と同じリポジトリ直下
- 追加テスト: `phase168_r3_8_citation_origin/tests/test_phase168_r3_8_citation_origin.py`（ZIP 展開先）
- 追加診断: `probe.py`（ZIP 展開先）
- 既存ファイルの変更: なし
- 実装全文・import 全文: `phase168_r3_8_citation_origin.py` とテストファイルに省略なしで収録
- 限定テスト: `python -m pytest -q phase168_r3_8_citation_origin/tests/test_phase168_r3_8_citation_origin.py`
- 完了条件: 4 テスト PASS、二群について出典重複と追加出典の由来が表示される
- 次工程: 出典の区別が明らかになってから、明示された文献識別子に基づく共通モデルの一本化を行う。今回は文献の恣意的削除や Renderer 切替は行わない
