Phase156-R5 repair2 — public header without body marker diagnostic

Production changes
==================
なし。

背景
====
Phase156-R5 Fixed1 では、
body_marker_without_header = 0
となった一方、

public_header_without_body_use:
  occurrences=4
  affected_groups=4

が残った。

既存 Phase153 audit-only contract は
body marker -> Reference header
のみを保証し、
Reference header -> body marker
を必須にはしていない。

目的
====
4件について次を調べる。

- group
- rendering route
- Reference headers
- body markers
- marker の無い Reference 番号
- canonical selected statements
- selected statement が本文に直接現れているか

判断
====
A. real minimal-display defect
   Reference が本文でも statement としても使われていない。

B. allowed implicit use
   Reference statement が本文に直接展開される、
   または特殊 renderer の prose が Reference を利用している。

C. audit contract mismatch
   marker を必須にする条件そのものが既存 public contract より強すぎる。

この診断前に production code は変更しない。

テスト
======
focused diagnostic tests のみ。

repository-wide pytest は実行しない。
