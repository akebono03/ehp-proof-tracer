Phase 159 pi4_3 generator-bridge duplicate suppression repair2

原因
----
target block 自体は1回しか描画されていない。

重複は relocated direct premise に含まれる

  Toda pi_4^3 finite cyclic quotient calculation

が

  pi_4^3 = Z/2{E eta_2}

という内部 statement を持ちながら、public renderer では eta-family notation により

  pi_4^3 = Z/2{eta_3}

と描画されるために生じる。

同じ root のもう1つの direct premise

  eta_3 = E eta_2

が generator bridge を与えるので、quotient premise と root conclusion は
public semantic claim として同一である。

修正
----
既存の
extract_toda_group_structure_narrative_redundant_direct_premise_step_ids()
を拡張する。

従来:
- target group が同じ
- group structure semantic key が完全一致

今回追加:
- FreeCyclicGroup または FiniteCyclicGroup
- 型が同じ
- FiniteCyclicGroup では order が同じ
- generator が sibling direct-premise equality bridge を介して同値

なら premise を redundant と判定する。

文字列比較は使用しない。

前回 repair1 の撤回
-------------------
前回追加した contribution insertion 側の root semantic suppression は
原因層ではなかったため撤回する。

削除:
- toda_group_proof_narrative_statement_identity.py
- tests/test_phase159_pi4_3_semantic_final_conclusion_dedup.py

contribution renderer に追加した import / guard も除去する。

変更対象
--------
変更:
- toda_group_proof_narrative_group_structure_semantics.py

新規:
- tests/test_phase159_pi4_3_generator_bridge_duplicate_suppression.py

撤回:
- toda_group_proof_narrative_contribution_renderer.py の repair1 追加分
- toda_group_proof_narrative_statement_identity.py
- tests/test_phase159_pi4_3_semantic_final_conclusion_dedup.py

全体テストは Phase 159 終了時まで実行しない。
