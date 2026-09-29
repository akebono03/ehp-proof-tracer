Phase 143-75AP R17 completion audit R3

目的
====
古い R14 API を使用せず、現在の Phase143 テストと同じ入口で
Narrative を再生成して completion 条件を確認する。

現行入口
========
tests.test_phase143_19_method_evidence._method_evidence_data(n, k)
  -> presentation, blocks, sidecar, arguments

render_toda_group_proof_narrative_multi_argument_markdown(
  presentation,
  blocks,
  sidecar,
  arguments,
)

監査内容
========
- n=2..17, k=0..7 のうち _method_evidence_data が構築可能な群を走査
- presentation node 数を集計
- presentation 内の internal rule.name が最終 Narrative に残る回数を集計
- render exception を集計

完了条件
========
- rule-name fallback occurrences = 0
- distinct fallback rule names = 0
- render errors = 0

変更
====
なし。read-only audit。
