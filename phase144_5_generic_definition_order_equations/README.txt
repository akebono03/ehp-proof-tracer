Phase 144-5
===========

目的
----
Phase 144-4 で B と判定された Definition / Order / equation numbering-reference
を generic Narrative 側で確認・補完する。

現行コード確認結果
------------------
Definition と Order は Phase 143 の Argument 層ですでに一般化されていた。

- TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
- TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER
- extract_toda_group_proof_narrative_argument_purpose_subject()
- "$subject$ を定める."
- "$subject$ の位数を決定する."

したがって Phase 144-5 ではこれらを再実装しない。
144-4 の B 判定は lower-level generic proof text と完成済み Argument Narrative の
層の違いによるものだった。

変更対象
--------
変更:
- toda_group_proof_narrative_argument_multi_renderer.py
  - generic equation numbering を最終 Narrative に適用。

新規:
- toda_group_proof_narrative_equation_numbering.py
  - standalone 数式への連番付与。
  - 式番号参照 `(N)` を生成する一般 helper。
- tests/test_phase144_5_generic_definition_order_equations.py

変更しない:
- legacy π₆³ renderer
- CLI / Web route
- Semantic / Block / Argument の既存意味論
- docs
- 他群専用 renderer

実行
----
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase144_5_generic_definition_order_equations.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_5_generic_definition_order_equations\run_phase144_5.ps1"

pytest
------
Phase 途中なので全体 pytest は実行しない。

完了条件
--------
1. generic π₆³ Narrative に Definition purpose が表示される。
2. generic π₆³ Narrative に Order purpose が表示される。
3. standalone 数式に generic な連番が付く。
4. generic equation reference helper が利用可能になる。
5. π₆³ / ν′ / Proposition 5.6 の hardcoding が numbering にない。
6. focused regression が通る。

Phase 144-6 との境界
--------------------
Phase 144-5 では legacy route を削除しない。
Phase 144-6 で初めて π₆³ の production route を generic-only に切り替え、
legacy と同等の数学的情報・可読性を確認する。
