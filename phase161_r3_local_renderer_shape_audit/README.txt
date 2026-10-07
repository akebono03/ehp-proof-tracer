Phase 161-R3 local renderer shape audit

目的
====
repair2 で GitHub 現行の関数名

  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown

がローカル production file に存在しないことが確認された。

そのため、これ以上 GitHub 側の関数形を仮定して patch せず、
ローカルの現在の renderer 構造を audit-only で確認する。

確認内容
========
- restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage()
  を含む実際のローカル関数名
- final body-usage filter を含む関数名
- unmarked-reference relink helper を含む関数名
- restore call 前後のソース行
- candidate public/render functions

変更
====
production code changes: none
tests changes: none

全体 pytest は実行しない。
