Phase 159 pi4_3 final-connector repair4

変更対象
========

変更:
- toda_group_proof_narrative_contribution_renderer.py
  - suppress_toda_group_proof_narrative_dangling_connectors()

新規:
- tests/test_phase159_pi4_3_final_connector_repair.py

import の変更
=============
なし。

監査結果
========

repair3 後:
- pi4_3 final group conclusion の重複は解消した。
- root conclusion count は全 pipeline stage で 1。
- connector count は stage 21 まで 1。
- stage 22 suppress_toda_group_proof_narrative_dangling_connectors()
  で 1 -> 0 になった。

原因
====

「以上より,」が独立 paragraph ではなく、
直前 paragraph の末尾 line として存在していた。

旧 dangling-connector cleanup は paragraph の末尾 line が

  以上より,
  したがって,
  これより,
  これらより,

のいずれかなら無条件に削除していた。

しかし直後に数式 derivation paragraph がある場合、
これは dangling connector ではない。

修正
====

paragraph 末尾の standalone connector の直後に
non-reference mathematical derivation paragraph がある場合:

旧:
- connector を削除。

新:
- 現 paragraph 末尾から connector を除く。
- connector を次の derivation paragraph の先頭へ移す。

例:

  [R2]より, pi3^2 = ...
  以上より,

  pi4^3 = ...

を

  [R2]より, pi3^2 = ...

  以上より, pi4^3 = ...

へ正規化する。

Reference marker paragraph が続く場合は connector を移さず、
従来どおり redundant connector として削除する。

既存 numbered connector の規則は変更しない。

テスト
======

新規:
- trailing 「以上より,」が次の数式 derivation に移動する。
- pi4_3 public proof の final conclusion が1回。
- 「以上より, final conclusion」が保持される。
- proof が □ で終わる。

既存:
- Phase 157 dangling connector cleanup
- Phase 159 provenance priority
- Phase 159 generator-bridge duplicate suppression
- Phase 143 group-structure duplicate suppression
- Phase 50 pi4_3 inference / exactness

完了条件
========

pi4_3 proof body の末尾が

  以上より, pi4_3 = Z/2{eta_3}.
  □

となり、同じ group conclusion は1回だけであること。

次 Phase との境界
=================

今回は dangling connector の分類だけを修正する。
connector 文体全般、equation numbering、他 group の prose は変更しない。

全体テストは Phase 159 終了時まで実行しない。
