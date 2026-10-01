Phase153-R3-5 Fixed1
Align R3-4 Tests with Duplicate Suppression

原因
====
R3-5 production behavior は本文の
"[R2] により、<statement>を得る。"
を
"[R2]を用いる。"
へ縮約する。

しかし R3-4 の既存テストは、
Reference section の終端を "[R2] により、" で探していたため、
R3-5 の正しい新仕様で ValueError になった。

Fixed1 の変更
=============
tests/test_phase153_r3_4_reference_statement_rendering_connection.py のみ。

変更内容
========
1. R3-4 public Reference statement test の Reference section 終端を
   "[R2] により、" から "## 証明" へ変更する。

2. internal fallback name test も Reference section を
   "## 証明" で分割する。

production code は変更しない。

完了条件
========
Phase153-R3-5 targeted tests が全件 PASS。

全体 pytest
===========
Phase153 の最後だけ実行する。
