Phase 159 - pi_4^3 exactness reason unification repair1

目的
====
初回修正では実装本体は成功している。
focused test でも、
- EXACTNESS_TO_KERNEL reason が構築される
- 「完全性より」の reason sentence が public Narrative に1回存在する
ところまで成功している。

失敗したのは、test が kernel conclusion を
\ker\left(E: ...\right)
という特定の表示文字列で探していたため。

今回の repair1 は test-only。
実装ファイルは変更しない。

変更対象
========
tests/test_phase159_pi4_3_exactness_reason_unification.py

変更内容
========
kernel conclusion の期待文字列を hard-code せず、
_render_generic_narrative_step(reason.conclusion_step)
から現行 renderer の canonical public representation を取得して、
「完全性より」の reason sentence がその直前にあることを検証する。

Phase 境界
==========
- EXACTNESS_TO_KERNEL の実装は変更しない。
- pi_4^3 固有 special case は追加しない。
- equation numbering は変更しない。
- Reference は変更しない。
- 他の prose rule は変更しない。
- repository-wide tests は実行しない。
