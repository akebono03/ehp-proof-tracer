Phase 158-R5-5b repair1e — pi6 step-consumption diagnosis

背景
----
repair1d 後:

- R5-5b focused ordering: 5 passed
- Phase 144 equation-numbering contract: 3 passed
- Phase 149 local-body ordering: 7 passed, 1 failed

残る失敗:
test_phase149_rc3_3_pi6_3_calculation_chain_remains_numbered

目的
----
pi_6^3 の calculation chain が、
どの Narrative Argument で先に表示済みとして消費され、
後続 Argument で excluded されるかを確認する。

診断内容
--------
A. calculation block inventory
- block index
- ProofStep id
- transition participant か
- statement type
- rendered text

B. Argument-by-Argument consumption
- ordered position
- Argument role
- conclusion block
- seen_non_exact_step_ids before/after
- local block order
- calculation step が VISIBLE / EXCLUDED のどちらか
- body renderer の出力

変更対象
--------
新規 audit bundle のみ。

Production code changes:
なし。

Existing test changes:
なし。

repository-wide pytest:
実行しない。

完了条件
--------
1. numbered calculation chain の各 step が最初にどの Argument で消費されるか確認できる。
2. seen_non_exact_step_ids による suppression の有無を確認できる。
3. production code を変更しない。
