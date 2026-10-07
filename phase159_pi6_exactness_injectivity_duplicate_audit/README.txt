Phase 159 - pi_6^3 exactness injectivity duplicate audit

目的
====
pi_4^3 の全射重複は解消したが、pi_6^3 の

  完全性より, E:pi_5^2->pi_6^3 は単射.

だけが最終 public Narrative で2回カウントされる。

これ以上 suppression を追加する前に、
どの pipeline stage で2件目が生じるかを特定する。

監査対象
========
- insert_toda_group_proof_narrative_map_property_dependencies()
- suppress_toda_group_proof_narrative_repeated_unique_step_statements()
- order_toda_group_proof_narrative_injective_image_order_reason()

各呼び出しの BEFORE / AFTER について、
E:pi_5^2->pi_6^3 は単射.
を含む paragraph をすべて表示する。

production code の変更
=======================
なし。

テスト変更
==========
なし。

全体テスト
==========
実行しない。
