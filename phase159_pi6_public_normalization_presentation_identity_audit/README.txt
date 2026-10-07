Phase 159 - pi_6^3 public normalization presentation identity audit

目的
====
実際の render_toda_group_proof_narrative_markdown() は

1. baseline renderer 内で semantic closure presentation を構築
2. contribution / wrapper / finalizer を closure presentation で処理
3. 最後の _phase158_normalize_public_narrative_contract() には
   元の base presentation を渡す

という非対称な経路になっている。

前回 audit は step 3 に closure presentation を渡していたため、
実際の public route と完全には一致していなかった。

監査内容
========
同じ finalized markdown に対して、

- base presentation で public normalization
- closure presentation で public normalization

をそれぞれ実行し、

  E:pi_5^2->pi_6^3 は単射.

の出現数を比較する。

さらに direct
render_toda_group_proof_narrative_markdown(base)
とも比較する。

production code
===============
変更なし。

tests
=====
変更なし。

repository-wide tests
=====================
実行しない。
