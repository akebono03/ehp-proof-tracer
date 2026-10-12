# Phase 164 R8-R1 — ProofStep 生成経路の棚卸し

- モード: 読み取り専用
- 全体 pytest: 未実施
- 解析した本番 Python ファイル数: 278
- 集計範囲: root-level *.py; exclude tooling prefixes, backups, tests, nested archives and old phase bundles
- 構文エラー: 0

## 呼び出し分類

- dataclass_replace_review: 68件
- direct_constructor: 155件
- inference_application: 26件

## 代表経路

- generator_replay: file=True, direct=0, inference=0
- operation_replay: file=True, direct=0, inference=0
- backward_reconstruction: file=True, direct=0, inference=2
- core_proof: file=True, direct=8, inference=2
- group_calculation: file=True, direct=0, inference=0

## 生成サイト例（各分類先頭15件）

### dataclass_replace_review
- `fix_phase94_2_line_endings.py:11` — `main` / `replace`
- `fix_phase94_2_line_endings.py:11` — `main` / `replace`
- `formatter.py:183` — `format_proof_step` / `replace`
- `generator_facts.py:141` — `GeneratorFactRepository.materialize_typed_element` / `replace`
- `phase162_pi5_3_backward_selection.py:48` — `_canonical_goals` / `replace`
- `phase162_r3g_existing_reason_bridge.py:78` — `build_phase162_r3g_existing_reason_trace` / `replace`
- `phase162_reference_boundary.py:97` — `cite_verified_fixed_statement` / `replace`
- `phase162_web_narrative_integration.py:53` — `_format_phase162_proof_sentences` / `replace`
- `phase162_web_narrative_integration.py:81` — `_compose_phase162_group_conclusion` / `replace`
- `phase163_r4_r11_literature_registration.py:133` — `_copy_snapshot` / `replace`
- `phase163_r4_r11_literature_registration.py:142` — `_copy_snapshot` / `replace`
- `phase163_r4_r12_literature_registration.py:192` — `register_prop51_prop53_literature_statements` / `replace`
- `phase163_r4_r12_literature_registration.py:195` — `register_prop51_prop53_literature_statements` / `replace`
- `phase163_r4_r6_structured_binding.py:96` — `bind_verified_fixed_statements` / `replace`
- `phase163_r4_r6_structured_binding.py:107` — `bind_verified_fixed_statements` / `replace`
### direct_constructor
- `hopf_rules.py:51` — `ehp_h_homomorphism_proof_step` / `ProofStep`
- `hopf_rules.py:161` — `hopf_invariant_proof_step` / `ProofStep`
- `map_facts.py:27` — `MapIsomorphismFact.to_proof_step` / `ProofStep`
- `phase162_pi5_3_backward_selection.py:62` — `_canonical_goals` / `ProofStep`
- `phase162_pi5_3_web_replay.py:38` — `build_phase162_pi5_3_web_replay` / `ProofStep`
- `phase162_reference_boundary.py:72` — `cite_verified_fixed_statement` / `ProofStep`
- `phase162_web_narrative_integration.py:119` — `_build_phase162_legacy_validated_isomorphism_markdown` / `ProofStep`
- `phase162_web_narrative_integration.py:182` — `_build_phase162_existing_group_connection` / `ProofStep`
- `phase162_web_narrative_integration.py:265` — `_phase162_ehp_leaves` / `ProofStep`
- `proof.py:1061` — `apply_inference_match` / `ProofStep`
- `proof.py:1127` — `relation_proof_step` / `ProofStep`
- `proof.py:1158` — `kernel_proof_step` / `ProofStep`
- `proof.py:1171` — `image_proof_step` / `ProofStep`
- `proof.py:1184` — `cokernel_proof_step` / `ProofStep`
- `proof.py:1243` — `exactness_proof_step` / `ProofStep`
### inference_application
- `phase161_r5_backward_proof_reconstruction.py:98` — `reconstruct_phase161_r5_goal.resolve` / `apply_inference_match`
- `phase161_r5_backward_proof_reconstruction.py:119` — `reconstruct_phase161_r5_goal.resolve` / `apply_inference_match`
- `phase161_r7_premise_provenance_validation.py:86` — `validate_phase161_r7_provenance.visit` / `apply_inference_match`
- `phase162_group_structure_backward.py:148` — `reconstruct_group_structure_goal` / `apply_inference_match`
- `phase162_pi5_3_backward_selection.py:73` — `_canonical_goals` / `apply_inference_match`
- `phase162_pi5_3_backward_selection.py:108` — `_apply_unique` / `apply_inference_match`
- `phase162_pi5_3_web_replay.py:36` — `build_phase162_pi5_3_web_replay` / `apply_inference_match`
- `phase162_r2_existing_proof_connection.py:99` — `reconstruct_phase162_r2_from_existing_proofs` / `apply_inference_match`
- `phase162_r3j_inference_rule_audit.py:71` — `classify_r3j_inference_rule` / `apply_inference_match`
- `phase162_reference_boundary.py:96` — `cite_verified_fixed_statement` / `apply_inference_match`
- `phase162_web_narrative_integration.py:173` — `_build_phase162_existing_group_connection` / `apply_inference_match`
- `phase162_web_narrative_integration.py:194` — `_build_phase162_existing_group_connection` / `apply_inference_match`
- `phase164_r5_web_registry_connection.py:69` — `build_phase164_r5_web_pi5_3_proof` / `apply_inference_match`
- `proof.py:1079` — `apply_inference_matches` / `apply_inference_match`
- `proof.py:1102` — `apply_inference_matches_with_results` / `apply_inference_match`

## 判断の境界

- `ProofStep(...)` は直接生成候補である。
- `apply_inference_match(...)` は規則に基づく推論生成であり、単純なコンストラクタと統合しない。
- Replay は既存 ProofStep の identity（同一性）保持が必要であり、新規生成対象ではない。
- `dataclasses.replace` は他のデータクラスも対象とするため個別に確認する。
- 本結果は静的棚卸しであり、R8 の実装完了判定ではない。
