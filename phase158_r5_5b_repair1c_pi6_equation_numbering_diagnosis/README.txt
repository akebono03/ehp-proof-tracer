Phase 158-R5-5b repair1c — pi6 equation numbering diagnosis

背景
----
R5-5b focused ordering tests:
5 passed.

Phase 149 local-body ordering regression:
7 passed, 1 failed.

失敗した canonical contract:
test_phase149_rc3_3_pi6_3_calculation_chain_remains_numbered

症状:
pi_6^3 の rendered multi-Argument Narrative から
`\tag{1}` などの equation numbering が消えた。

目的
----
Production を追加変更する前に、番号消失位置を特定する。

診断内容
--------
A. number_toda_group_proof_narrative_equations() が番号対象とする
   source/target ProofStep を列挙。

各候補について:
- raw_plain:
  numbering 呼び出し直前 Markdown に plain equation が存在するか
- final_plain:
  numbering 後 Markdown に plain equation が存在するか
- final_tag:
  対応する `\tag{n}` が存在するか

B. Narrative Argument ごとに:
- ordered position
- role
- local body block indices
- method evidence block indices
- conclusion block
- local body 内 statement type / rendered text

C. numbering 前 Markdown 全文

D. numbering 後 Markdown 全文

変更対象
--------
新規 audit bundle のみ。

Production code changes:
なし。

Existing tests changes:
なし。

実行テスト
----------
診断 script が動作することだけを確認する lightweight test 1件。

repository-wide pytest:
実行しない。

完了条件
--------
1. 6本の番号候補について raw/final presence が確認できる。
2. numbering 前に式が消えているのか、numbering 内でタグ付けに失敗するのか判定できる。
3. 各式の Argument/local-body ownership が確認できる。
4. Production code を変更しない。
