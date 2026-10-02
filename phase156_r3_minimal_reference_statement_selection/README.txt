Phase156-R3 — minimal Reference statement selection rule

変更対象
========
Production:
- toda_group_proof_narrative_references.py
  - select_toda_group_proof_narrative_reference_statement_steps()

New focused test:
- phase156_r3_minimal_reference_statement_selection/
  test_phase156_r3_minimal_reference_selection.py

New audit:
- phase156_r3_minimal_reference_statement_selection/audit_phase156_r3.py

変更内容
========
現行 selector は boundary-used candidate が無い場合、
proof edge で使われている candidate をすべて公開 Reference statement
として選択していた。

Phase156-R2 では reference_side_overfull 103件のうち、
85件が same-Reference internal consumer only であることが確認された。

R3 では次の一般規則に変更する。

1. Reference 境界を越えて直接使われる candidate がある場合:
   その boundary-used candidates を従来どおり全て選択する。

2. boundary-used candidate が無い場合:
   same-Reference internal consumer だけでは公開 statement を増やさない。

3. 既存 API 互換性のため、candidate 自身または consumer が
   entry.reference と一致しない既存 proof-used case は従来どおり優先する。

4. それ以外は最初の eligible candidate 1件へ fallback する。

import 変更
===========
なし。

Phase156-R3 で行わないもの
===========================
- Reference theorem / lemma 自体の選択変更
- proof body duplicate suppression
- Reference rendering format の変更
- proof data の変更
- stable range の拡張
- repository-wide pytest

focused pytest
==============
python -m pytest `
  ".\tests\test_phase153_r3_3_reference_statement_selection.py" `
  ".\tests\test_phase153_r5_reference_selection.py" `
  ".\tests\test_phase153_r6_reference_granularity.py" `
  ".\phase156_r3_minimal_reference_statement_selection\test_phase156_r3_minimal_reference_selection.py" `
  -q -p no:cacheprovider

public Reference regression
===========================
python -m pytest `
  ".\tests\test_phase153_r3_10_public_reference_connection_repair.py" `
  -q -p no:cacheprovider

完了条件
========
- focused selector tests PASS
- public Reference connection regression PASS
- 112 groups
- exceptions = 0
- selection violations = 0
- boundary-used statements は維持
- boundary が無い same-Reference internal usage では公開 selection を1件より増やさない

次 Phase との境界
=================
Phase156-R4 で proof body duplicate suppression を扱う。
R3 では Reference statement selection だけを変更する。
