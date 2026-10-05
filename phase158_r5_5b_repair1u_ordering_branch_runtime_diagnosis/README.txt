Phase 158-R5-5b repair1u — ordering branch runtime diagnosis

背景
----
repair1t で確認:
- source eq1, eq2 は tag(1), tag(2)
- connector は復元済み
- target eq3 は plain
- runtime numbering は source-only 実装
- order statement / order conclusion が calculation chain より前

GitHub HEAD:
- numbering は source + target を番号付け
- local-body extractor は dependency-before-conclusion

一方、repair1d では production runtime に
TARGET conclusion のときだけ dependency-ordered local_body_blocks を維持し、
その他は global blocks order へ戻す branch を入れた。

目的
----
現在 runtime の branch を直接確認し、
次の production repair で:
1. target numbering を復元
2. ORDER argument も dependency order へ戻す

ことが同じ generic contract として安全か判断する。

変更対象
--------
新規 audit bundle のみ。

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。
