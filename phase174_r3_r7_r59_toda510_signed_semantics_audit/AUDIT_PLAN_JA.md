# Phase 174 R59 — Toda (5.10) 型と符号の整合性監査

## 実装前に確認した GitHub の現行コード

- `akebono03/ehp-proof-tracer`、`develop` HEAD `82d725d8649cd6307c2abd67024e3ef4f3cddfe2`。
- `sources/toda/Toda_05_2.tex` の (5.10) は `\Delta(\iota_{11})=\nu_5\circ\eta_8`（符号なし）。
- `phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py` と関連 test：原文の固定 SHA、独立した Proposition 5.8 の位数2表示、`TodaDeltaImageUpToSignStatement`。
- `phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py` と関連 test：自由巡回群から有限巡回群への一般的な写像の核を3前提から求める規則。
- `phase174_r3_r7_r57_narrative_source_cleanup/audit.py`：2群の完成証明の公開 Narrative 監査。
- R58 はローカル未実施の可能性があり、監査は R58 の対象コードを変更しない。

## 数学的監査

(5.10) の値域は `\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}`。したがって `-\nu_5\eta_8=\nu_5\eta_8`。
この**具体的**な位数2の値域に限り、内部の符号付き命題は原文と同じ帰結を与える。
一般の `\mathbb Z/m` では `+h` と `-h` は同じ元とは限らない。
ただし `\Delta(g)=\pm h` の両方で、`\ker(\mathbb Z\{g\}\to\mathbb Z/m\{h\})=m\mathbb Z\{g\}` は正しい。

## 変更対象

既存コード・既存テスト・主要5文書は一切変更しない。
新規ディレクトリ `phase174_r3_r7_r59_toda510_signed_semantics_audit/` のみ。

- `audit.py`：新規関数 `git_blob_sha`, `signed_generator_is_identical`, `checked_git_files`, `local_git_snapshot`, `inspect_semantics`, `main`。全関数・import の全文はファイルに収録。
- `tests/test_audit.py`：新規の5テスト関数（パラメータ化）。全関数・import の全文はファイルに収録。
- `run.ps1`：監査・限定 pytest の実行。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`。

## 完了条件

1. Source Guard の Git Blob SHA 照合 PASS。
2. (5.10) の式が符号なしであり、対応する群が位数2、出典は2件の既存 GIVEN と確認。
3. R35 の3前提が元のまま一致し、汎用規則を変更しない。
4. R57 公開証明の2群の完成・Reference・Prop 2.7 の境界を維持。
5. R59/R34/R35 の限定 pytest PASS。全体 pytest は実行しない。

## 次の境界

もし原文をそのまま「符号なしの型」で登録し直すなら、既存の signed 型を読む全 consumer と回帰テストを先に監査し、互換性を持つ別 Phase とする。R59 はそこまで先取りしない。
