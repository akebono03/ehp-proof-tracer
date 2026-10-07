Phase 159 pi6_3 exactness reason stage audit

目的
====

repair5 後、Phase 159 pi4_3 focused tests は 7/7 PASS した。

一方、Phase 157 dangling-connector regression で

  この完全性と $Δ=0$ より,
  $\ker E=\operatorname{Im}Δ=0$.

が public pi6_3 body から消えている。

この文は EXACTNESS_TO_MAP_PROPERTY typed reason から生成される。

確認内容
========

pi6_3 のみについて次を追跡する。

1. reason sidecar に EXACTNESS_TO_MAP_PROPERTY が存在するか。
2. render_toda_group_proof_narrative_reason_sentence() が文を生成するか。
3. reference boundary filtering 後も reason が残るか。
4. reason insertion 後に文が存在するか。
5. その後のどの stage で最初に消えるか。

production code
===============

変更なし。

pytest
======

実行しない。
これは audit-only。

全体テスト
==========

実行しない。
