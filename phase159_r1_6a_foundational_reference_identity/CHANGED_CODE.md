# Phase 159-R1-6a

変更対象:
- proof.py
  - FoundationalReferenceIdentity を追加
  - ProofStep 全体を変更
- toda_upstream_bootstrap.py
  - proof import に FoundationalReferenceIdentity を追加
  - _build_phase49_result() 全体を変更
- toda_group_proof_narrative_renderer.py
  - proof import に FoundationalReferenceIdentity を追加
  - foundational reference helper を追加
  - render_toda_group_proof_narrative_markdown() 全体を変更
- tests/test_phase159_r1_6a_foundational_reference_identity.py を新規追加

実装方針:
- literature reference と foundational reference を別型で保持
- foundational は [F1], [F2], ... として表示
- literature fixed-statement pipeline は変更しない
- pi_3^2 target を Reference に再導入しない
- Proposition 5.1 に誤帰属しない

完了条件:
- 3 premise に foundational identity が保持される
- public Reference に 3 foundational facts が表示される
- root target は foundational reference を持たない
- Reference に pi_3^2 target / Proposition 5.1 が出ない
- focused tests / related tests / git diff --check PASS

次 Phase との境界:
- 本文への [F1] より等の linkage は未実装
- full pytest は Phase 159 最後のみ
