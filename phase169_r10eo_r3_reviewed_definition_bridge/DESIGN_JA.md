# Phase 169 R10EO-R3 — 審査済み Definition の型付き登録

## 対象と変更一覧

本 Phase は R10EO-R2 の Definition Index（定義索引）を用い、文献を確認済みの Definition だけを既存の共通推論に接続する。

変更対象の既存ファイル・関数：

- `phase169_r10d2_general_family_definition/family_citation.py` の `canonical_member()` 全体、`cited_family_reference_sentence()` 全体。
- `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` 全体。

上記既存ファイルの import 部分は変更しない。変更後の関数全体は `full_functions/` に格納し、導入後にも `output/full_functions/` に出力する。

新規ファイル：

- `phase169_r10eo_r3_reviewed_definition_bridge/reviewed_definitions.py`（ファイル冒頭に import、`ReviewedDefinitionAttestation`、`REVIEWED_ATTESTATIONS`、`reviewed_definition_ids()`、`_chapter_vi_base()`、`verified_reviewed_definitions()`、`build_cited_reviewed_definitions()`）。
- `phase169_r10eo_r3_reviewed_definition_bridge/patch.py`（変更前の Git blob を照合する完全関数置換コード）。
- `phase169_r10eo_r3_reviewed_definition_bridge/tests/test_r10eo_r3_definition_bridge.py`（既存コード・引用・偽装拒否・引用接続テスト）。
- `phase169_r10eo_r3_reviewed_definition_bridge/audit.py`（実行時 Goal・Trust Boundary 監査）。
- `phase169_r10eo_r3_reviewed_definition_bridge/run.ps1`（バックアップ、パッチ、限定テスト、再監査、失敗時復元）。

`README.md` は英語、本資料は日本語で全文収録する。`docs/` の5文書は R3 中には変更しない。

## 採用の根拠と責務境界

`HyoujiGen.csv` の `kinds=0`、`k`、`n`、`latex` は、生成元の型・候補を示すメタデータであり、それだけでは Definition を証明しない。R2 Index も文字列発見だけなので、それだけでは証明しない。

R3 では、`sources/toda/Toda_06_2.tex` Chapter VI, v) の定義

$$
\zeta_n:=E^{n-5}\zeta_5\qquad(n\ge5)
$$

について、監査対象の転写の SHA-256、行番号、節開始、節終了、定義式の一意性、CSV の型との一致を照合する。審査済み情報は `ReviewedDefinitionAttestation` の定数レコードに保持し、未審査の候補を自動昇格しない。現時点では一件のみが審査済み。これは個別生成元に依存した推論規則ではなく、出典を採用するためのレコードである。原著の印刷版を独立照合したものとはしない。

引用が認可されれば、既存の `CitedStableFamilyDefinition` が `GIVEN` の結論となり、`canonical_member` と `expand_cited_stable_family` による `INFERENCE` を通じて、一段の `GeneratorImage` を得る。推論規則の定義および群構造輸送則は変更しない。

任意の $r\ge1$ について $E^r(\alpha_n)=\alpha_{n+r}$ の導出は、型付きの一段 `GeneratorImage` 連鎖と既存の輸送則を通じて行う。Toda (4.5) の同型適用条件 $n\ge k+2$ はこの定義とは独立に検証する。

## 監査基準

- 出典 SHA または定義の文面を変更すると拒否。
- 定義の行、型、開始次元、節の配置を変えると拒否。
- `GIVEN` から定義特殊化の `INFERENCE` を介することを確認する。未検証の `GeneratorImage` を `GIVEN` に置換しない。
- 既存の Chapter V 2件および Chapter VI 3件の引用経路は維持。
- 巡回群、直和群、合成元の既存輸送則は変更しない。
- `\pi_{41}^{30}` の残存 Goal を実行時に再収集し、`complete` の場合のみ Trust Boundary を検査する。`
- フル pytest は Phase 169 の終了時のみ実行する。

## 次 Phase との境界

R3 は審査済みの Definition の接続だけを行い、未審査33件の Definition を追加しない。もし11-stem に `CyclicStructureStatement` や `Relation` が残れば、R4 で既存の群構造輸送との関係を調査する。一般的な文献 Definition Index への全面置換、Chapter V の出典位置再設計、証明本文の改変はこの R3 の対象外とする。
