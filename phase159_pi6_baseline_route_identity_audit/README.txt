Phase 159 - pi_6^3 baseline route identity audit

目的
====
前回 audit では同じ finalized markdown を public normalization すると
base / closure presentation のどちらでも対象単射文は1回だった。

一方 direct
render_toda_group_proof_narrative_markdown()
では2回になる。

したがって差は baseline renderer の実行経路側にある。

監査内容
========
毎回 fresh presentation を作り、以下を比較する。

1. baseline 処理を手動再現
2. _phase158_baseline_render_toda_group_proof_narrative_markdown()
3. actual baseline を public normalize
4. render_toda_group_proof_narrative_markdown()

さらに semantic closure を

  base -> closure1 -> closure2

と2回適用し、node count と出力を比較する。

production code
===============
変更なし。

tests
=====
変更なし。

repository-wide tests
=====================
実行しない。
