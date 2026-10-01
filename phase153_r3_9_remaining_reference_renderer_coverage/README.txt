Phase153-R3-9
Remaining Reference Renderer Coverage

目的
====
Phase153-R3-8 で remaining renderer coverage defect と分類された
9 statement types / 31 occurrences を semantic-renderable にする。

対象
====
- TodaProp44IsomorphismStatement
- TodaProp53FiniteDimensionalStatement
- TodaProp44SecondSummandRestrictionStatement
- TodaProp59FiniteDimensionalStatement
- TodaDeltaSurjectiveStatement
- TodaProp58FiniteDimensionalStatement
- TodaProp511NuSquaredFiniteDimensionalStatement
- TodaDeltaKernelFreeCyclicStatement
- TodaProp27HopfInvariantUpToSignStatement

変更対象
========
production:
- toda_group_proof_generic_narrative_renderer.py

tests:
- tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py

実装方針
========
新しい数学的事実は追加しない。
既存 statement field のみを表示する。

今回しないこと
==============
- representative selection rule
- public route connection
- Reference/body ownership
- duplicate suppression
- proof graph
- full pytest

完了条件
========
- R3-8 の9 statement types を全種類検出
- occurrences = 31
- 31件すべて fallback なし
- 112 groups の structured Reference entries 222件すべて selected statement を持つ
- R3-3〜R3-6 関連テストを壊さない

次 Phase との境界
================
R3-9 は renderer coverage だけ。
次は R3-10 で public Reference connection defect を扱う。
