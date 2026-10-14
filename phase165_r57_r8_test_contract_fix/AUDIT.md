# R57-R8 テスト失敗の原因

- `test_shared_provider_has_specialization_with_screened_reference`: 未展開の `build_adopted_prop51_reference()` は複合命題の `GIVEN` を1つだけ持つ。`shared_expansion_provider()` はその `GIVEN` の結論を収集するため、構成要素の `Relation` は見つからない。本番の `build_shared_typed_bridge()` と同じく、`expand_cited_given_components()` を通してから検査する。
- `test_inference_rule_derives_only_from_typed_source_step`: `find_inference_matches_for_rule()` の返値は `InferenceMatch` であり `.conclusion` はない。既存の `derive_inference_proof_step()` によって `ProofStep` を生成し、その結論を確認する。
- R57-R8 の実装変更は不要。両件はテストの前提と API の使い方の不一致。
- 共通探索による π₅⁴ の成功と Web 表示は今回の対象テストだけでは証明されない。
