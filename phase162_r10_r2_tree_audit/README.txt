Phase 162 R10-R2 -- read-only tree audit

対象: π_5^3 の Web replay と R10 補助再構築経路。
Production や既存テストを変更しない。元の ProofStep の引用ラベルも変更しない。

Output (repository root):
  phase162_r10_r2_tree_audit.json
  phase162_r10_r2_tree_audit.md

監査すること:
- 両経路の最終結論、ノード、edge、文献境界、H(ν')=η5 と Lemma 5.2
- 引用の direct premise、consumers、root からの identity-based paths
- 重複した結論、map-property statement、Reference 帰属

実施しないこと:
- Web Renderer の修正
- 引用ルールの真偽の自動判定
- 全体 pytest
