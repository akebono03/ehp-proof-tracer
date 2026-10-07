Phase 159 pi3_2 semantic definition-premise locality repair1

原因
====
1. 前回 apply script は render_toda_group_proof_narrative_markdown() 全体の
   literal body を置換していたため、ローカルの後続変更があると一致しなかった。
2. tests/test_phase159_pi3_2_map_property_order.py の既存 focused test は、
   H の単射・全射を古い inline prose で完全一致しており、
   現在の numbered display-math 契約に対して stale だった。

修正
====
- renderer の変更は全文置換ではなく、
  _phase158_normalize_public_narrative_contract() 呼び出し直後の
  安定した関数アンカーへ locality pass を挿入する。
- locality 関数がすでに前回の途中適用で存在する場合は再追加しない。
- focused test は H の map と property の semantic content を paragraph 内で確認し、
  inline/display の表現差には依存しない。
- locality については
    H 全射
    pi_3^3 = Z{iota_3}
    H 同型
    eta_2 definition
  の意味的順序と、最後の3項の隣接性を確認する。

変更対象
========
- toda_group_proof_narrative_renderer.py
  - _phase159_reorder_unique_preimage_definition_premise_locality()
    （未追加の場合のみ追加）
  - render_toda_group_proof_narrative_markdown()
    （locality pass 呼び出しのみ追加）
- tests/test_phase159_pi3_2_map_property_order.py
  - stale focused expectations を現在の numbered display 契約から独立させる
  - locality test を追加

Phase 境界
==========
今回も unique-preimage definition の direct-premise locality のみ。
一般 proof scheduler の再設計は行わない。
full pytest は Phase 終了時のみ。
