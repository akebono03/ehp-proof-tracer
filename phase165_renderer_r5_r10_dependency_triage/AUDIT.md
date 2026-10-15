# Phase 165 R5-R10 監査範囲

- 対象：`phase162_web_narrative_integration.py`、`phase162_r3_narrative_connection.py`、`toda_group_proof_narrative_proof_chain_renderer.py`、`toda_group_proof_narrative_concrete_transport.py`。
- 関連テスト：`tests/test_phase162_r3_narrative_connection.py`、`tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py`、`tests/test_phase162_r4_b3_common_renderer_fix.py`。
- GitHub の現行コードを確認した。Windows 側の R4・R5 修正は GitHub と一致しない場合があるため、実環境を読み取り専用で解析する。
- R5-R9 は「本番側」に監査スクリプトを含め得るため、R5-R10 ではアプリケーション・監査・テストへ分類する。
- `_phase162_ehp_leaves` は `phase162_pi5_3_web_replay.py` で使用されており、この依存を解消するまでは旧モジュールを削除しない。
- 静的参照が0件でも外部 API や動的 import の不存在は証明できない。
- 既存コード・テストを変更せず、限定テストのみ実施。旧 Phase 162 fixture の6件の失敗は未解決として保持する。
- 次の作業では依存関数の移設や旧 API の取り扱いを設計し、変更が必要なファイルだけを対象にする。
