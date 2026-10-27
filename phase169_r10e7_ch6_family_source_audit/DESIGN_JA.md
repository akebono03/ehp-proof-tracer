# Phase 169 R10E7 — Chapter VI 系列定義監査

## 対象・変更一覧

新規監査専用フォルダ `phase169_r10e7_ch6_family_source_audit/` を追加する。既存の本番モジュール・テスト・主要ドキュメントは変更しない。

- `audit.py`：`FAMILIES` と `inspect_source_clause()`, `inspect_generator_metadata()`, `inspect_manifest()`, `build_report()`, `main()` を新規追加。これらの関数は同ファイル内の定義位置に全体を収録。
- `tests/test_r10e7_ch6_source_audit.py`：監査関数への限定テストを新規追加。`import` を含むファイル全体を収録。
- `run.ps1`：develop ブランチ・確認済 HEAD・Git blob のガード、限定 pytest、監査、出力復旧を実行。
- `README.md`：英語の実行手順。

## 原典確認対象

採用転写 `sources/toda/Toda_06_2.tex` の定義式を、節内に限定して一意に照合する。

- ε 系列（HyoujiGen ID=10, stem=8）：$\varepsilon_n=E^{n-3}\varepsilon_3$ （$n\ge3$）。
- $\bar\nu$ 系列（ID=11, stem=8）：$\bar\nu_n=E^{n-6}\bar\nu_6$ （$n\ge6$）。
- μ 系列（ID=12, stem=9）：$\mu_n=E^{n-3}\mu_3$ （$n\ge3$）。

現在の `phase163_r4_r94_output/manifest.json` は Chapter V までの source-order position を持つ。Chapter VI の位置を推測して補わない。データベースの生成元名・型一致は `GeneratorImage` の証明としない。原典採用転写の確認は原著の印刷版の照合ではない。

## 完了条件

- 3つの Chapter VI 定義式が該当節に一意に存在し、CSV の型情報と整合する。
- Chapter VI の引用マニフェストの有無を事実として報告する。
- 新しい `GIVEN`／`INFERENCE` を作らず、既存の `partial` を `complete` に変更しない。
- 限定 pytest と Integrity が通り、本番 tracked file を変更しない。

## 次作業との境界

次段階は Chapter VI の reference/position を別途審査し、共通 `CitedStableFamilyDefinition` 経路に接続する最小変更。Proof Tree と Trust Boundary で正当化されるまで完成証明は表示しない。全体 pytest は Phase 169 の最後のみ。
