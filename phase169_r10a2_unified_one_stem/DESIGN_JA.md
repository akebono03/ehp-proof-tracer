# Phase 169 R10A2 — 1-stem と 2-stem の Narrative 表示統一

## 現状と原因

R10A1 では、2-stem の R7 型 `GeneratorImage` 連鎖を、実際に証明された場合に限って一式に圧縮できた。しかし 1-stem では `phase166_r3ac_stable_notation` と `phase165_r12_r21_eta_generator_chain` の別々の型付き推論から表示が作られており、群構造の中間表示と最後の一回懸垂が重複した。

## 変更する対象

- 既存本番ファイル：`phase168_r3_5_model_renderer.py`
- 関数：`render_model_backed_narrative_markdown()` の全文（ZIP 実行後 `output/render_model_backed_narrative_markdown_FULL.py` に出力）
- 新規ファイル：`phase169_r10a2_unified_one_stem/one_stem_projection.py`
- 新規関数：`project_verified_one_stem_notation_chain()`（新規ファイル先頭の import と補助コメントの後に追加）
- 新規限定テスト：`tests/test_r10a2_one_stem_projection.py`（6件）
- 変更しないもの：DB、`shared_expansion_provider`、R7 規則、命題台帳、既存の Reference/ProofStep、R10A の投影規則

## 証明の信頼境界

1. 1-stem の型付き root が `stable_eta_notation` の証明済み等式であることを既存投影関数により確認する。
2. 根拠となる Toda (4.5) の具体的同型と先行群構造が実際に root の祖先に含まれることを確認する。
3. η 系列の一般定義が実際の `GIVEN` かつ引用付き前提であることを確認する。
4. 省略する中間 `Relation` と `GeneratorSuspension` を完全に識別し、型・次元・出典が不一致なら圧縮を拒否する。
5. 1-stem と 2-stem とも R10A の `VerifiedStableImageChainDisplay` で本文に一回だけ式を出す。
6. Proof Tree、Reference、証明ステップ、未完成証明の表示は変更しない。

## 期待する文章

`π₉⁸` の証明本文は、先行 `π₄³`、Toda (4.5) の `E⁵` 同型、η 系列の `E⁵(η₃)=η₈`、結論の四要素のみを示す。本文の `E(η₇)=η₈` と `π₉⁸=Z/2{E⁵η₃}` は圧縮後表示しない。

## 検証と次 Phase

限定 pytest と Web の完成証明、引用、Proof Tree、R10A 2-stem 出力を検証する。既存 R10A1 のファイルと異なれば変更せず停止する。失敗時は変更前の R10A1 へ戻す。全体 pytest は Phase 169 終了時のみ。次の R10B の `HyoujiGen.csv` 全系列一般化は本 Phase 変更に含めない。
