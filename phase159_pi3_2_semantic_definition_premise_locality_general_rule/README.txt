Phase 159: semantic definition-premise locality general rule

目的
----
unique-preimage definition の public Narrative で、consumer が直接必要とする
semantic premises を consumer の直前へ配置する。

今回の pi_3^2 では、eta_2 definition の direct premises は
- H: pi_3^2 -> pi_3^3 の isomorphism
- pi_3^3 = Z{iota_3}
である。

一般規則
--------
1. semantic closure 上で unique-preimage definition consumer を選ぶ。
2. consumer.proof_step.premises を direct premises として使う。
3. consumer と同じ group_map を持つ isomorphism premise を semantic に特定する。
4. その他の direct premises の相対順序は保持する。
5. 「この同型写像により」の直前参照を自然にするため、
   matching isomorphism premise を direct-premise 群の最後に置く。
6. direct-premise 群全体を consumer の直前へ移す。
7. prose の文字列内容から依存関係を推測しない。
   文字列は semantic step と public paragraph の位置対応にのみ使う。

期待順序
--------
完全性より H は全射. (2)

[R1]より, pi_3^3 = Z{iota_3}.

(1), (2) より, H: pi_3^2 -> pi_3^3 は同型.

この同型写像により,
H(eta_2)=iota_3 となる eta_2 in pi_3^2 が一意に存在する.

変更対象
--------
- toda_group_proof_narrative_renderer.py
  - 新規:
    _phase159_reorder_unique_preimage_definition_premise_locality()
  - 変更:
    render_toda_group_proof_narrative_markdown()
- tests/test_phase159_pi3_2_map_property_order.py
  - 新規:
    test_phase159_pi3_2_definition_premises_are_local_to_semantic_consumer()

テスト方針
----------
focused tests のみ実行する。
Phase の最後ではないため full pytest は実行しない。
