Phase 159 - repair3c fix1
Cross-group performance audit

目的
----
repair3c 後、既存 focused regression が

  test_phase144_6_r5_42_reproduces_phase40_selected_population

の fixture 構築中で長時間停止する現象を分解する。

TARGETS
-------
(3, 3)
(5, 3)
(4, 6)
(5, 7)
(8, 7)
(9, 7)

各 target について以下を測定する。

- _context() 構築時間
- argument ごとの local body / provider / anchor / chain 数
- argument ごとの _necessity_for_chain() 時間
- necessity pair 数
- _build_visibility_occurrences() 時間
- build_toda_group_proof_narrative_ordered_contributions() 時間

変更
----
Production code changes: NONE
Existing test changes: NONE
Document changes: NONE

pytest
------
実行しない。
repository-wide pytest も実行しない。

完了条件
--------
どの target / argument / stage で repair3c による探索量増大が発生しているかを
数字で特定する。

この audit の結果を確認するまで production optimization は行わない。
