Phase 159 - pi_6^3 semantic-closure injectivity duplicate audit

目的
====
前回 audit では base presentation を contribution renderer に直接渡すと
E:pi_5^2->pi_6^3 は単射. は1回だった。

しかし実際の public route は contribution renderer の前に

  build_toda_group_proof_narrative_semantic_closure_presentation()

を実行する。

この差が pi_6^3 の単射重複を生んでいるか確認する。

監査内容
========
1. base presentation の SuspensionInjective node 一覧
2. semantic closure presentation の SuspensionInjective node 一覧
3. base contribution renderer の対象文数
4. semantic closure contribution renderer の対象文数
5. final public Narrative の対象文数

production code
===============
変更なし。

tests
=====
変更なし。

repository-wide tests
=====================
実行しない。
