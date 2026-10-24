# Phase 168 R3-41P10 — Generic ProofStep replay (audit only)

この監査は、既存 matcher による Model 入口での一括検証を試作する。
証明済みの証拠を新規発行するものではなく、探索後に数学的検証を再実行する方式である。

| 群 | 推論 Step | 汎用再検証 PASS | 時間(ms) | 前回全文一致 | Citation |
|---|---:|---:|---:|---|---|
| pi3_2 | 13 | 13 | 1.847 | True | True |
| pi4_3 | 19 | 19 | 2.86 | True | True |
| pi5_4 | 7 | 7 | 1.084 | True | True |

## 人工的な偽の推論
- stable_eta: Model受け入れ=True, 汎用再検証で拒否=True, 失敗内容=[{'step_index': 2, 'conclusion_type': 'Relation', 'premise_count': 2, 'rule_name': 'cited stable eta-family notation for iterated transport', 'matching_premise_bindings': 0, 'accepted': False, 'failure': 'RULE_MATCH_REJECTED'}]
- ehp_exactness: Model受け入れ=True, 汎用再検証で拒否=True, 失敗内容=[{'step_index': 25, 'conclusion_type': 'EHPImageEqualsKernelStatement', 'premise_count': 1, 'rule_name': 'EHP exactness implies image equals kernel', 'matching_premise_bindings': 1, 'accepted': False, 'failure': 'CONCLUSION_MISMATCH'}]

## 信頼境界に関する解釈
- `ProofStep` と `ProofNarrativeModel` 自身は証明済み証明書ではない。
- `find_inference_matches_for_rule()` による再検証は表示から数学を分離できるが、探索時の検証と重複する。
- GIVEN の出典・文献順をこの試作は再認証しない。
- ここで PASS しても全群・全 API について検証済みと宣言するものではない。
- 監査結果を評価するまで、本体の Renderer / Model / Search に変更しない。

**AUDIT_STATUS**: PASS
**FULL_PYTEST_NOT_RUN**
