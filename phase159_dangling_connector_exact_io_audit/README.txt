Phase 159 dangling connector exact I/O audit

目的:
repair4 後の suppress_toda_group_proof_narrative_dangling_connectors()
について、synthetic input ではなく実際の stage 21 input を確認する。

対象:
- pi_4^3
- pi_6^3

出力:
- stage 21 BEFORE の paragraph 番号 + repr
- dangling cleanup AFTER の paragraph 番号 + repr
- connector count
- raw Markdown

これにより:
- pi_4^3 の「以上より,」がどの paragraph に存在するか
- repair4 がなぜ actual pipeline で保持できないか
- pi_6^3 の reason prose にどの paragraph で副作用が出るか

を特定する。

production code は変更しない。
pytest / 全体テストは実行しない。
