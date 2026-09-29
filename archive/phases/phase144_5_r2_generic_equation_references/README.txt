Phase 144-5-R2
================

目的
----
Phase 144-5-R1 で確認した「全 standalone 数式への機械的連番」を修正し、
generic calculation-chain に必要な式だけを番号化して本文から参照する。

変更対象
--------
変更:
- toda_group_proof_narrative_equation_numbering.py
  - `これらより、` で表現される generic calculation chain の source/target のみ番号化。
  - source の番号を使って `(1) と (2) より、` のような参照文を生成。
- tests/test_phase144_5_generic_definition_order_equations.py
  - selective numbering と actual reference を検証。

変更しない:
- toda_group_proof_narrative_argument_multi_renderer.py
- toda_group_proof_narrative_argument_renderer.py
- Semantic / Block / Argument model
- legacy renderer
- CLI / Web route
- docs

一般化境界
----------
n, k, π₆³, ν′, Toda Proposition 5.6 による分岐は追加しない。
Narrative がすでに持つ generic calculation-chain connector
`これらより、` を presentation-level の参照境界として利用する。

実行
----
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase144_5_r2_generic_equation_references.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_5_r2_generic_equation_references\run_phase144_5_r2.ps1"

全体 pytest は Phase 途中なので実行しない。

完了条件
--------
- Definition purpose が維持される。
- Order purpose が維持される。
- calculation chain の source/target のみ番号化される。
- 本文に `(n) と (m) より、` が実際に生成される。
- 全 standalone 数式への連番は行わない。
- target-specific hardcoding がない。
- focused regression が通る。

次 Phase との境界
-----------------
Phase 144-5-R2 では legacy production route を変更しない。
完了後の Phase 144-6 で π₆³ production route を generic-only に切り替える。
