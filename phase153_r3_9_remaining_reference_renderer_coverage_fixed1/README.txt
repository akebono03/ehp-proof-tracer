Phase153-R3-9 Fixed1
Remaining Reference Renderer Coverage

修正理由
========
初版 apply script の marker が、実改行ではなく文字としての "\n" を含む形で生成され、
R3-6 helper の関数定義を検出できなかった。

初版は marker 検出前に import 置換を行ったため、ローカルでは import のみ
先行適用されている可能性がある。

Fixed1
======
- marker を実改行の正しい文字列へ修正
- import が既に適用済みでも安全に継続できる idempotent apply に変更
- helper / dispatch / surjective tuple も既適用なら再変更しない
- production の数学的仕様は初版と同じ

変更対象
========
production:
- toda_group_proof_generic_narrative_renderer.py

tests:
- tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py

完了条件
========
- 9 statement types / 31 occurrences が semantic-renderable
- structured Reference entries 222件すべて selected statement あり
- targeted regression tests PASS
- full pytest は実行しない
