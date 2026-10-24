# R3-41P GitHub develop 事前レビュー（2026-10-24）

## 対象ファイル（閲覧確認済み）

- `phase168_r3_5_model_renderer.py`（397行）
- `phase168_r3_27_typed_statement_projection.py`（264行）
- `phase168_r3_3_proof_narrative_model.py`（167行）
- `phase168_r3_4_link_bridge.py`（31行）
- `phase168_r3_12_body_binding.py`（71行）
- `phase168_r3_29_order_projection.py`（180行）
- `phase165_r57_r20_general_specialization.py`（340行）
- `phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py`
- `phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py`
- `phase168_r3_29_order_projection/tests/test_phase168_r3_29_order_projection.py`
- `phase168_r3_39a_reference_accuracy/tests/test_phase168_r3_39a_reference_accuracy.py`
- `phase168_r3_8_citation_origin/tests/test_phase168_r3_8_citation_origin.py`

GitHub の `develop` を直接取得して行番号・関数実装・関連テストを確認した。ユーザーの作業ツリーと一致するとは限らないため、ZIP は実行環境のファイルを再監査する。

## 責務越境が実在する箇所

1. **Renderer 55–87行** `validated_specialization_citation_numbers()` は `specialize_typed_statement()` を実行。しかも一般の零群条件 `0 <= i < n` を独立に判定する。これは単なる Citation の参照ではない。
2. **Typed Projection 61–92行** `toda45_specialization_evidence()` は前提木をたどり、`specialize_typed_statement()` で `(n,m,k)` の適用条件を再判定。`typed_sentence()` 161–179行と Citation Projection 95–109行が依存。
3. **Typed Projection 112–158行** `project_stable_eta_notation_transition()` は `_stable_eta_renaming_shape()` を呼び、数学的条件が成立するか再チェックする。
4. **Typed Projection 230–237行** `typed_sentence()` は `prop42_exactness_indices()` によって完全列の窓を再判定する。
5. **Renderer 219–240行** 証明上の中間ステップ省略には `inference_rule.name` の固定文字列を使う。推論規則の命名変更に弱い。
6. **Renderer 193–217行** 核計算の統合表示は ProofStep の型や前提内容を比較する。数式同値の確認か表示の整合性確認かは分離して判断すべき。

## 保持すべき既存機能

- **Model 13–32行** `NarrativeCitation` は `assertion_ids` / `reference_ids` / `statement_bodies` を持つ。`ProofNarrativeModel` は `steps` / `citations` / `step_citation_numbers` を持つ。
- **Model 75–160行** は使用された ProofStep と登録出典を対応付け、番号を Model 上で確定する。
- **Link Bridge 22–30行** は使用済み GIVEN への登録リンクのみを渡す。
- **Body Binding 33–62行** はモデルの引用の双方向整合性を検査し、未登録 Citation を拒否する。これは妥当な表示境界の検査である。
- **Order Projection 41–180行** は表示順を決め、Proof Tree の依存関係や循環を検査する。新しい証明を推論していない。

## 監査結果の解釈

Model 側には、一般命題から具体命題への特殊化で確定した scalar binding を記録する専用フィールドはない。
また、Renderer が引用先祖をたどる処理に相当する確定済み投影を全ステップ分持つとも確認できない。
ただし「新しい層の追加が必要」という結論は出さない。現在の Model と証明木の情報で十分ならそれを利用する。

今回のパッケージは**監査専用**。実装変更対象はゼロ。
実行後の `output/audit.md` / `output/audit.json` / 3群の全文および diff を次の変更判定に使用する。
