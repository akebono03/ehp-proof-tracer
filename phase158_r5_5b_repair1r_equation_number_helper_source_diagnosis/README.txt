Phase 158-R5-5b repair1r — equation-number helper source diagnosis

背景
----
repair1q で runtime の
_phase158_normalize_public_narrative_contract()
に次の処理が存在することを確認:

proof_body = (
  _phase158_normalize_public_equation_numbers(
    proof_body
  )
)

この helper の直後に:
- tag(1) が消える
- tag(2) が消える
- tag(4) も消える

GitHub HEAD には helper 自体が存在しない。
したがってローカル Phase 158 作業中の未 push 実装と判断する。

目的
----
helper の runtime source と実際の before/after を取得し、
意図と副作用を確定する。

確認内容
--------
1. module path
2. helper runtime source 全文
3. tag / regex / replace / connector logic の有無
4. proof body の line-by-line before/after
5. full input / full output

変更対象
--------
新規 audit bundle のみ。

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。
