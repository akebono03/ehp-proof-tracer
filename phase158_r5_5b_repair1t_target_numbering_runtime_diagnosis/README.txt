Phase 158-R5-5b repair1t — target numbering runtime diagnosis

背景
----
repair1s 後:
- Phase 157 dangling connector tests: 5 passed
- Phase 157 final reflexive suppression: 2 passed
- Phase 156 relation-side normalization: 3 passed / 1 failed

失敗行は equation_three:

2 nu' = eta_3^3 tag(3)

したがって:
- eq1 tag(1): 復元
- eq2 tag(2): 復元
- connector (1) と (2) より,: 復元
- eq3 tag(3): 未復元

目的
----
runtime の equation-numbering 実装について、
target step の line matching と numbering 条件を確認する。

確認内容
--------
1. runtime source 全文
2. target step object id
3. source step object ids
4. plain/tagged line indices
5. connector line indices
6. numbering function を再度直接適用した結果

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。
