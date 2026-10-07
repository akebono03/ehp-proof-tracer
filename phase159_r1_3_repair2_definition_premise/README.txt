Phase 159-R1-3 repair2

原因:
repair1 は eta_2 definition の prerequisite を PRECONDITION_FOR_DEFINITION から探したが、
この semantic role は現行では nu-prime / Lemma 5.2 系に限定される。

既存構造:
toda_pi3_2_define_eta2_inference_rule() は Hopf isomorphism と pi_3^3 free cyclic fact を
premises として eta_2 definition を導く。
inference engine は使用した ProofStep を derived ProofStep.premises に保存する。

修正:
_phase159_unique_preimage_definition_line() は proof_step.premises から
同じ map を持つ isomorphism premise を直接確認する。

変更対象:
- toda_group_proof_narrative_renderer.py
  - _phase159_unique_preimage_definition_line() 全体
  - _phase159_project_generic_semantics_to_public_proof() 内の呼び出し1か所

テスト変更:
なし。

Full pytest:
実行しない。
