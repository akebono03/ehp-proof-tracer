Phase 159 - pi_4^3 repair3a
Contribution selection internal audit

目的
----
repair3 body exposure audit で確認された

  raw -> semantic closure -> blocks -> Argument local body

までは必要な pi_4^3 の事実が到達している一方、

  ordered contributions = 0

となる原因を contribution selection 内部だけで特定する。

監査対象
--------
- proof chain providers
- Argument 0 local body
- hidden_ids
- chain_ids
- provider anchors
- reachable anchors
- necessity
- base markdown visibility
- rendering fallback
- _build_visibility_occurrences
- owner selection
- ordered contributions

変更
----
Production code changes: NONE
Existing test changes: NONE
Document changes: NONE

pytest
------
実行しない。
Phase 最後の全体テストまで repository-wide pytest は行わない。

完了条件
--------
contribution_count=0 の直接原因が次のいずれかまで分類されること。

- NO_PROVIDER_ANCHORS
- ANCHORS_CANNOT_REACH_CONCLUSION
- NO_CHAIN_HIDDEN_INTERSECTION
- NECESSITY_FILTER_REMOVES_ALL
- ALREADY_VISIBLE_FILTER_REMOVES_ALL
- FALLBACK_FILTER_REMOVES_ALL
- OWNER_SELECTION_REMOVES_ALL
- その他の後段原因

Phase 境界
----------
repair3a は監査のみ。
production code の修正は repair3b 以降で、repair3a の診断結果に基づき
1か所に限定して行う。
