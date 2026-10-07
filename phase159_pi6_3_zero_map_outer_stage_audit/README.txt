Phase 159 pi6_3 zero-map outer-stage audit

目的
====

Phase 157 residual regression で public pi6_3 body から

  Delta: pi7^5 -> pi5^2 は零写像である.

が消えていることが判明した。

一方、直前の contribution-renderer stage audit では
この零写像 statement は残っていた。

したがって outer public pipeline のどこで消えるかを追跡する。

対象 stage
==========

00 with contributions
01 public wrapper
02 finalizer
03 Phase 158 public contract normalization
04 actual public renderer

各 stage で確認
===============

- zero-map statement の有無
- concise injectivity reason の有無
- 関連 paragraph の index / repr

production code
===============

変更なし。

test code
=========

変更なし。

pytest
======

実行しない。

全体テスト
==========

実行しない。
