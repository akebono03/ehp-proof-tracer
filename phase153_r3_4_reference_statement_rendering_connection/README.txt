Phase153-R3-4
Reference Statement Rendering Connection

目的
====
Phase153-R3-3 で production API 化した representative statement selection rule を
Reference section の表示へ接続する。

変更対象
========
production:
- toda_group_proof_narrative_references.py
- toda_group_proof_narrative_contribution_renderer.py

tests:
- tests/test_phase153_r3_4_reference_statement_rendering_connection.py

変更内容
========
1. Reference renderer に optional な
   statement_lines_by_reference_number を追加する。
2. contribution renderer で Reference entry の proof_steps を
   generic semantic renderer に通す。
3. rule-name / type-name / raw fallback は candidate にしない。
4. renderable candidate を R3-3 selection rule に渡す。
5. 選択された statement を [Rn] heading の直下に表示する。

今回しないこと
==============
- 本文側の重複 suppress
- unresolved 12 statement types の renderer 追加
- theorem-specific / group-specific branch
- full pytest

完了条件
========
- 従来 Reference renderer API が維持される
- [R2] (4.5) の下に semantic statement が表示される
- R3-3 selection rule が使われる
- internal rule-name fallback が Reference section に露出しない
- 関連 regression tests が通る

次 Phase との境界
================
R3-4 は表示接続だけ。
次段階で Reference section と本文の完全重複を最小限 suppress する。
unresolved renderer の補完は別 subphase で扱う。
