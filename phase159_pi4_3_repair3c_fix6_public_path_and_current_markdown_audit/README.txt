Phase 159 - pi_4^3 repair3c fix6
Public path and current_markdown contract audit

背景
----
fix5 では build_toda_group_proof_narrative_ordered_contributions() を
current_markdown=None で呼び、pi_4^3 の

- Delta(iota_5)
- Im Delta

だけが selected、
- ker E
- E surjective

は occurrence/owner まで通るが selected=False と確認した。

しかし実際の public renderer:
render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

は base_markdown を構築し、

  current_markdown=base_markdown

を明示して ordered contributions を生成している。

また既存 test:
test_phase144_6_r5_43_r3_current_markdown_plumbing_repair.py

は default 呼び出しと explicit base_markdown 呼び出しが同一 step population であることを
契約としている。

目的
----
1. TARGETS 6群で default / explicit current_markdown の selected step identity を比較。
2. pi_4^3 で4事実の default / explicit selection を比較。
3. 実際の public renderer 出力に4事実が存在するか確認。
4. 既存 current_markdown contract test を実行。

変更
----
Production code changes: NONE
Existing test changes: NONE
Document changes: NONE

pytest
------
tests/test_phase144_6_r5_43_r3_current_markdown_plumbing_repair.py

Repository-wide pytest は実行しない。

完了条件
--------
- public path で pi_4^3 4事実の実際の表示状態が確定する。
- repair3c が default/explicit parity contract を壊したか確定する。
- この結果を見るまで production selection は追加変更しない。
