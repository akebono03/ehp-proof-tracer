Phase156-R5 repair1 — body marker without header diagnostic

Production changes
==================
なし。

目的
====
Phase156-R5 で残った4件の
body_marker_without_header
だけを具体的に切り分ける。

確認するもの
============
- group
- n / k
- rendering route
- public Reference header numbers
- body Reference marker numbers
- missing header numbers
- offending body lines
- full rendered narrative

この段階では production を修正しない。

判断
====
診断後に4件を次のどちらかに分類する。

A. real rendering defect
   public Reference header が欠落しているのに body marker が残っている。

B. audit contract mismatch
   special route / hand-written marker が canonical Reference header と
   別の numbering contract を持っており、R5 audit が同一 contract と
   誤認している。

既存 Phase153 audit-only test が PASS しているため、
この区別を行う前に production を変更しない。

テスト
======
focused diagnostic tests のみ。

repository-wide pytest は実行しない。
