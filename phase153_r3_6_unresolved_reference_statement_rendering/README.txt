Phase153-R3-6
Unresolved Reference Statement Rendering

目的
====
Phase153-R3-2 で unresolved と確認された 37 reference steps / 12 statement types を、
内部 rule-name や type-name ではなく、既存 dataclass field から数学的に表示する。

対象 statement types
====================
- Toda52CompositionIsomorphismStatement
- TodaLemma54Statement
- TodaProp51FiniteDimensionalStatement
- TodaProp56FiniteDimensionalStatement
- TodaLemma513Statement
- TodaProp511FiniteDimensionalStatement
- TodaProp515Pi12_5HopfIsomorphismStatement
- Toda36Lemma514SigmaDoublePrimeBridgeStatement
- Toda55NuFamilyFiniteDimensionalStatement
- TodaLemma514SigmaPrimeStatement
- Toda53NuPrimeBracketSpecializationStatement
- TodaLemma514Sigma8Statement

変更対象
========
production:
- toda_group_proof_generic_narrative_renderer.py

tests:
- tests/test_phase153_r3_6_unresolved_reference_statement_rendering.py

実装方針
========
新しい数学的事実は作らない。
各 statement が既に持っている field のみを表示する。

今回しないこと
==============
- reference selection rule の変更
- Reference/body ownership rule の変更
- duplicate suppression rule の変更
- proof graph の変更
- theorem-specific group-number branch
- full pytest

テスト
======
n=2..15, k=0..7, depth=2 の 112 groups を走査し、
R3-2 で unresolved だった 12 statement types / 37 occurrences 全てについて、
generic renderer が rule-name / type-name / repr / str fallback を返さないことを確認する。

完了条件
========
- 対象 12 statement types を全種類検出する
- occurrences = 37
- 37件すべて semantic rendering される
- R3-3〜R3-5 と既存 Reference tests が通る
- full pytest は実行しない

次 Phase との境界
================
R3-6 は unresolved renderer の解消まで。
Phase153 の残作業では、R3 全体の 112-group 再監査と、
Phase 終了時だけ full pytest を行う。
