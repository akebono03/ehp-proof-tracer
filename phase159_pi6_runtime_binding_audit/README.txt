Phase 159 - pi_6^3 runtime binding audit

目的
====
fresh presentation でも、

- actual baseline + normalization: 対象単射文 1回
- direct render_toda_group_proof_narrative_markdown(): 2回

となる。

通常のソース読みだけでは説明できないため、
runtime で実際に呼ばれている関数 binding を inspect する。

監査内容
========
1. render_toda_group_proof_narrative_markdown
2. _phase158_baseline_render_toda_group_proof_narrative_markdown
3. _phase158_normalize_public_narrative_contract

について、
- function id
- module
- qualname
- source file
- co_firstlineno
- inspect.getsource()
を表示する。

さらに renderer module 上の baseline / normalizer を監査用 wrapper に
一時的に差し替え、direct public call 内部で実際に通る入出力を記録する。

production code
===============
変更なし。

tests
=====
変更なし。

repository-wide tests
=====================
実行しない。
