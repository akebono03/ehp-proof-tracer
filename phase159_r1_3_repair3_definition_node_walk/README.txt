Phase 159-R1-3 repair3

原因
----
repair2 で `_phase159_unique_preimage_definition_line()` は
`proof_step.premises` から isomorphism premise を読むようになったが、
呼び出し側が依然として `semantic_sidecar.dependency_semantics` の
`PRECONDITION_FOR_DEFINITION` だけを走査していた。

eta_2 definition はその semantic dependency の対象ではないため、
helper が一度も呼ばれていなかった。

修正
----
`_phase159_project_generic_semantics_to_public_proof()` の definition projection 部分を、
`semantic_presentation.nodes` 全体の走査に変更する。

各 ProofStep に対して `_phase159_unique_preimage_definition_line()` を呼び、
helper 自身が以下を満たす場合だけ prose を生成する。

- statement に map / element / image がある。
- `proof_step.premises` に同じ map の isomorphism statement がある。

したがって pi_3^2 専用の dimension / statement-name 条件は追加しない。

変更対象
--------
- toda_group_proof_narrative_renderer.py
  - `_phase159_project_generic_semantics_to_public_proof()` の definition traversal

import 変更
-----------
なし。

テスト変更
----------
なし。

Full pytest
-----------
実行しない。
