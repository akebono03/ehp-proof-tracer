# Phase 175 R3R10R1 — CRLF テストの Windows 互換性修正

## R3R10R1 変更対象（既存コード・テスト確認後）

- **修正ファイル：** `phase175_r3r10_generator_zero_narrative/tests/test_install.py`。
- **修正テスト関数：** `test_crlf_file_preserves_line_endings()` の全体。
- **先頭 import：** 変更なし。`pathlib.Path`、`pytest`、`install` の import 全文は `CODE_FULL_JA.md` に掲載。
- **追加関数・クラス：** なし。
- **今回の本体コード変更：** なし（R3R10 に含まれている `typed_sentence()` の関数全体の置換処理は引き続き実行対象）。
- **原因：** Windows の `Path.write_text()` がもともと CRLF を出力した後、旧テストが LF を CRLF に一律置換して `CRCRLF` を発生させていた。
- **修正：** 入力の CRLF をまず LF に揃え、CRLF に一度だけ変換。CRCRLF がないことを検査。
- **再現・回帰確認：** `tests/test_install.py` の3テスト、および Python による初期 CRLF 模擬を確認。Windows 上では新 ZIP 解凍後の限定 pytest と公開監査で判定する。

## R3R10 本来の作業内容（変更なし）


## 対象と変更箇所（最初に確認）

現行 GitHub `akebono03/ehp-proof-tracer` の `develop` のコードを確認した。R3R9 の `route.py`・`rule.py`・`test_public_search.py` および実際の Web 使用経路 `web_group_proof.py` → `phase168_r3_5_model_renderer.py` → `phase168_r3_27_typed_statement_projection.py` を確認した。

- **変更する既存ファイル：** `phase168_r3_27_typed_statement_projection.py`。
- **変更する既存関数：** `typed_sentence(statement, step)` の全体。差し替え全文は `full_functions/typed_sentence_FULL.py`。
- **変更しない既存 import：** ファイル先頭の import 節は無変更。追加 import は `typed_sentence()` 内の `GeneratorImage` 条件分岐に限定。
- **既存クラス・他の関数：** 無変更。
- **R3R10 から継続して含めるファイル：** `phase175_r3r10_generator_zero_narrative/` 配下の `install.py`、`audit.py`、`run.ps1`、`__init__.py`、`full_functions/typed_sentence_BASE.py`、`full_functions/typed_sentence_FULL.py`、`tests/test_projection.py`、`tests/test_install.py`、`tests/test_public.py`、本書および README・CODE_FULL・TEST_RESULTS。
- **新規関数の配置：** `install.py` のモジュール定数・`PatchPlan` の後に `_function_span`・`_normalized_function`・`plan_patch`・`apply_patch` を定義。`audit.py` の定数の後に `_command`・`_check_git`・`_audit_public_result`・`run`・`main` を定義。各テスト関数は新規テストファイルに配置。

## 数学的な表示仕様

既存の `GeneratorImage` 推論を数式として描画する。文献に明記された `E(η₂∘ν′)=0` は R3R9 で検証済みの出典型 `TodaLemma57ExplicitNuPrimeZero` を前提とする `INFERENCE` であり、今回のコードはその証明を新規に作らない。`Zero` の表示を `0` にし、通常の簡易表示が扱えない合成生成元のみ、既存の `render_toda_expression_latex()` を用いて表示する。合成は入力された `Composition` の左右から `\circ` を明示し、表示上の省略を避ける。

既存の Model Renderer は、当該推論ステップの先祖にある `GIVEN` の引用番号から `[R2]より,` を自動付与する。証明木の順序に従って、群構造・生成元の像・零写像の順で説明する。引用番号・群の次元による文字列置換は実施しない。

## ガード・検証

1. `develop` ブランチ、既存コード Git Blob SHA、R3R9 依存ファイルの存在を検証。
2. `typed_sentence()` の現行全文が GitHub で確認した旧全文に一致することを確認。変更があれば失敗。
3. `-DryRun` はコード変更・pytest 実行なし。
4. 本実行で完全な関数単位の置換と限定 pytest を行う。
5. `inspect_one_group(3,4)` で実際の公開検索・Trust・Reference・Web 完成と `[R2]より, E(η₂∘ν′)=0.` の表示順序を確認する。Lemma 5.4 が再導入されないことを確認。
6. 失敗時、今回変更した対象ファイルを安全な場合に限り元のバイト列へ戻す。

## 完了条件・Phase の境界

完了 Gate は `PASS_R3R10_LEMMA57_ZERO_GENERATOR_NARRATIVE_VISIBLE`。検証を実施していない段階では成功宣言しない。Source-first、First Successful Proof Search、唯一性検査なしの方針を維持し、数学的 GIVEN・新規推論・個別 Narrative を追加しない。全体 pytest は Phase 175 の終了時のみ実施。次の数学的課題 `π₉⁵` と `π₁₀⁶` は本変更に含めない。
