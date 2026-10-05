Phase 158-R5-5b repair1q — contract runtime-source diagnosis

背景
----
repair1p で tag loss の境界を特定:

wrapped:
- eq1 tag(1) present
- eq2 tag(2) present

finalized:
- eq1 tag(1) present
- eq2 tag(2) present

normalized:
- eq1 tag lost
- eq2 tag lost

したがって tag loss は
_phase158_normalize_public_narrative_contract()
の中で発生している。

ただし GitHub HEAD の同関数を読む限り、
tag を直接削除する処理は見当たらない。

目的
----
ローカル runtime の関数本文を直接確認する。

確認内容
--------
1. 実際に import された module path
2. inspect.getsource() による runtime function 全文
3. tag literal / replace / re.sub の有無
4. baseline の tag 関連行
5. normalized の対応行
6. tagged line が exact / untagged のどちらで normalized に存在するか

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。
