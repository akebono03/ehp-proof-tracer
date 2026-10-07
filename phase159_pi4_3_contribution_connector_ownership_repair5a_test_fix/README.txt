Phase 159 pi4_3 contribution-connector ownership repair5a

目的
====

repair5 の production code は変更しない。

repair5 で追加したテスト helper が
tests/test_phase143_19_method_evidence.py の
_method_evidence_data() の返り値順を誤って解釈していたため、
テストだけを修正する。

現行 helper の返り値
===================

  (
    presentation,
    blocks,
    sidecar,
    arguments,
  )

repair5 の誤り
==============

誤:

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  )

このため semantic_sidecar に block tuple が入り、
build_toda_group_proof_narrative_proof_chains() の型検証で

  TypeError:
  semantic_sidecar must be a TodaGroupProofNarrativeSemanticSidecar

となっていた。

変更対象
========

変更:
- tests/test_phase159_pi4_3_contribution_connector_ownership.py
  - _phase159_pi4_3_context()

production code:
- 変更なし

import:
- 変更なし

修正後
======

  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    1,
  )

とする。

その後の返り値は repair5 テスト内で従来どおり

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    base,
    ordered_contributions,
  )

に整形する。

テスト
======

Phase 159:
- contribution connector ownership
- provenance priority
- generator bridge duplicate suppression

既存 regression:
- Phase 144 contribution placement
- Phase 157 dangling connector cleanup
- Phase 50 pi4_3 inference / exactness

完了条件
========

1. 新規 Phase 159 テストが型エラーではなく実際の repair5 behavior を検証する。
2. pi4_3 の final conclusion が1回。
3. 「以上より, pi4_3 = ...」が保持される。
4. Phase 157 dangling connector regression が PASS する。
5. 全体テストは実行しない。

次 Phase との境界
=================

repair5a は test-only。
production behavior の追加変更は行わない。
