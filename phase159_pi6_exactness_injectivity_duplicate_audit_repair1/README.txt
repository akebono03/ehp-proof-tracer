Phase 159 - pi_6^3 exactness injectivity duplicate audit repair1

原因
====
前回 audit script は package subdirectory 内から直接実行されたため、
Python の sys.path[0] が audit directory になった。

その結果、repository root にある

  toda_group_proof_narrative_contribution_renderer.py

を import できなかった。

修正
====
audit script 冒頭で

  ROOT = Path(__file__).resolve().parents[1]

を求め、ROOT を sys.path の先頭へ追加してから project modules を import する。

production code の変更
=======================
なし。

test の変更
===========
なし。

目的
====
pi_6^3 の

  E:pi_5^2 -> pi_6^3 は単射.

が最終 public Narrative で2回になる処理段階を特定する。

監査対象
========
- insert_toda_group_proof_narrative_map_property_dependencies()
- suppress_toda_group_proof_narrative_repeated_unique_step_statements()
- order_toda_group_proof_narrative_injective_image_order_reason()

全体テスト
==========
実行しない。
