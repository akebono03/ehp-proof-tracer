# Phase 169 R10EO-R1 — Definition 一般化の設計監査

## 変更対象・追加位置

本 Phase は AUDIT_ONLY。本番ファイル・既存テストは変更しない。既存 API、Proof Tree、Reference も変更しない。

新規ディレクトリ `phase169_r10eo_r1_definition_audit/` に以下を追加する。

- `__init__.py`：監査用 package。
- `audit.py`：新規の純粋関数 `read_metadata`、`normalize_tex`、`literal_definition_candidates`、`classify_source`、`inspect_metadata_and_sources`、`inspect_live_goal`、`render_markdown`、`main` の全文。import は同ファイル先頭に全文掲載。
- `tests/test_r10eo_audit.py`：新規テスト関数7件の全文。import は同ファイル先頭に全文掲載。
- `run.ps1`：develop と固定 HEAD を照合し、限定 pytest、監査、Git 差分検査を実行。
- `README.md`：英語の使用方法。
- `DESIGN_JA.md`：本設計資料。

## 監査対象の現行コード

- `data/HyoujiGen.csv`
- `phase169_r10b_registered_stable_family_binding/family_registry.py` とテスト
- `phase169_r10d2_general_family_definition/family_citation.py` とテスト
- `phase169_r10e8_hyoujigen_generic_suspension/source_records.py`、`chapter_vi_reference.py` とテスト
- `phase169_r10e1_general_group_transport/transport.py` とテスト
- `phase165_r52_r9_shared_math.py`
- `sources/toda/Toda_05_2.tex`、`sources/toda/Toda_06_2.tex`

## 判断

`kinds=0` は現在の実装で添字付き系列の型付き候補を作る分類に使用される。`n` は候補の開始次元、`k` は次数差。`stable` と `stable_orders` は現行 CSV で空欄であり、定義の真偽を判断する根拠にならない。

数学的な論理構造は次のように区別する。

1. CSV の型情報から、登録済み生成元候補を作る。これは証明ではない。
2. 採用した文献中の定義を正確に同定し、出典・出版順序・原著照合状態を管理する。この承認があって初めて固定 `DEFINITION`／`GIVEN` の候補になる。
3. 承認された $\alpha_n:=E^{n-n_0}\alpha_{n_0}$ から、`StableFamilyMemberDefinition` を一般規則で導出する。
4. 隣接する定義インスタンスから $E(\alpha_n)=\alpha_{n+1}$ の `GeneratorImage` を推論する。
5. すべての `GeneratorImage` と Toda (4.5) の独立した同型を前提に群構造を輸送する。

## R10EO-R2 の設計候補（今回は未実装）

生成元 ID ごとの推論規則を増やさず、**文献単位で採用を検証する Definition インデックス**を設計する。一般的な TeX 定義形を探索・構造化するが、テキスト一致だけを `GIVEN` に昇格させない。採用済み出典と監査済み位置を明示した source attestation（出典認証）を要求する。

`SOURCE_RECORDS` と `CHAPTER_VI_SOURCE_RECORDS` は、必要な出典認証に置き換えた範囲で縮小できる。ただし単に削除して CSV から `GIVEN` を作る実装は禁止する。既存の η の経路は R10EO-R1 で変更せず、統合可能性を次段階で別途検討する。

合成生成元は各成分の型付き `GeneratorImage` を維持し、直和群は各成分の順序・位数・画像の独立した前提を維持する。今回の監査で群構造の `Relation` を自動成立と扱わない。

## 監査の限界

- 出典は `sources/toda/` の採用済み転写。原著印刷版の独立照合をしたとは主張しない。
- `literal_definition_candidates` は保守的な字面一致であり、TeX のすべての表現形式に対応する一般パーサではない。検出漏れや候補重複を個別に確認する。
- 本環境ではユーザーの Windows checkout を実行できない。`run.ps1` により `pi_41^30` の Open Goal 全件を実行時に再取得する。
- 実装は未変更。全体 pytest は Phase 終了時のみ実施する。

## 完了条件

GitHub 最新 HEAD との整合確認、39件の候補同定、CSV と出典の責務境界の明示、ζ の文献中定義候補の検出、既存テストおよび新規限定テストの実行、`pi_41^30` の残り Goal の再報告、既存 tracked file の無変更を確認すること。R10EO-R1 自体は「設計監査」であり、`pi_41^30` の完成証明を目標としない。
