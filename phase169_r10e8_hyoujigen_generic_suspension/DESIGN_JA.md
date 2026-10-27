# Phase 169 R10E8 — HyoujiGen 共通懸垂規則の文献接続

## 目的と責務

`HyoujiGen.csv` を生成元の型と名称に関する唯一の参照元とする。`kinds=0`、`id`、`k`、`n`、`latex` は「系列の候補」と「型付きの元」を表すが、CSV の値だけを根拠として懸垂像を証明済みにしない。

Todo Chapter VI の原典採用転写 `sources/toda/Toda_06_2.tex` の3箇所について、本文、節境界、HyoujiGen の最小次元・系列名との整合を検査し、引用付きの定義を `FIXED_STATEMENT` の `GIVEN` として登録する。原著版の紙面順序までは検証しておらず、`publication_position` は既存の Chapter V 採用転写の文献順序の直後に、検証した Chapter VI の行順を加えた値である。

この `GIVEN` から生成される具体的系列元定義と `GeneratorImage` は、既存の `canonical_member` と `expand_cited_stable_family` により **INFERENCE** として導く。規則の新設、元ごとの条件分岐、群構造のデータベース値からの懸垂像推定はしない。

## 対象系列

| ID | 系列 | HyoujiGen の stem | 最小次元 | 原典の位置 |
|---|---|---:|---:|---|
| 10 | $\varepsilon_n$ | 8 | 3 | Chapter VI, i) |
| 11 | $\bar\nu_n$ | 8 | 6 | Chapter VI, ii) |
| 12 | $\mu_n$ | 9 | 3 | Chapter VI, iii) |

表の値は確認結果の記録であり、実装で系列別に固定した推論パラメータではない。

## 変更対象

1. `phase169_r10d2_general_family_definition/family_citation.py` の import と `canonical_member`、`cited_family_reference_sentence`。過去の Chapter V 用 API と `SOURCE_RECORDS` は維持する。
2. `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge`。新しい引用 Bridge を既存 Bridge に接続する。
3. `phase169_r10e8_hyoujigen_generic_suspension/source_records.py`、`chapter_vi_reference.py` を新規作成する。既存の原典ファイル・DB・検索規則・Renderer は変更しない。
4. `phase169_r10e8_hyoujigen_generic_suspension/tests/test_r10e8_hyoujigen_generic_suspension.py` を新規作成する。

## 限定テストと完了条件

- R10E8 の出典照合、CSV-only 拒否、誤型拒否、ProofRule.GIVEN と INFERENCE の分離。
- R10D2、R10E5、R10E4 の限定回帰テスト。
- $\pi_{23}^{15}$、$\pi_{24}^{15}$ の探索状態と導出像数を監査する。未解決条件があれば `partial` のまま報告する。
- 全体 pytest は Phase 169 の最後にのみ実行する。

## 次 Phase との境界

R10E8 は文献付き系列定義の共有推論接続に限る。証明を完成と判定する最終条件は各 `GeneratorImage` の検証済み INFERENCE、群構造への依存関係、および Trust Boundary における検証であり、Narrative Model や共通 Renderer の変更はこの段階では行わない。
