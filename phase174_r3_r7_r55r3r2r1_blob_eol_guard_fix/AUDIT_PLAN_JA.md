# Phase 174 R55R3R2R1 — Git blob 改行照合修正

## 失敗原因

旧 R55R3R2 は `_run_git('show', ..., binary=True)` の結果を `_source()` で LF に正規化した後で `_git_blob(committed)` を実行した。GitHub `develop` の `phase168_r3_27_typed_statement_projection.py` は CRLF のため、正しい Git blob であっても SHA が一致しなかった。

## 修正範囲

- 新規 ZIP 内の `install.py`：`_git_blob` をバイト列に限定し、`construct_sources` で HEAD blob の生バイト列を照合してから `_source()` で正規化する。
- 新規 ZIP 内の `tests/test_payload.py`：CRLF/LF/BOM に対する回帰テストを追加。
- `run.ps1`：新規パッケージ名に対応。
- `README.md`・`CODE_FULL_JA.md`：新しい実装を全文掲載。

数学的証明木、文献 GIVEN、推論規則、Source-first、First Successful Proof Search は変更しない。旧 R55R3・R55R3R1 専用 Narrative の撤去方針も維持する。

## Source Guard

ローカル `develop` と GitHub HEAD の系譜を確認し、元の Git blob SHA を生バイト列で検証する。ローカルファイルは元の BOM と改行形式を維持する。未確認の編集や旧パッケージの不明なファイルは削除せず停止する。

## 確認する限定 pytest

- `tests/test_payload.py`：CRLF / LF / BOM の SHA 差異と型検査を追加。
- `tests/test_static.py`：旧専用 Narrative の実行経路が残っていないこと。
- `tests/test_typed.py`：型付き命題の共通表示（一般の偶数 $n$ も対象）。
- `tests/test_public.py`：実 Group query と HTTP。
- `phase174_r3_r7_r55_common_exactness_intro/tests/test_http.py` および R37 規則の限定回帰。

全体 pytest は Phase 終了まで実行しない。

## 完了条件

1. DryRun の Source Guard PASS。
2. 旧 R55R3・R55R3R1 の専用モジュール撤去。
3. 既存三ファイルの想定済み・最小限の変更のみ。
4. 限定 pytest と実公開証明監査 PASS、既存28段階の証明木維持。
5. 数学的 GIVEN と推論規則の増分ゼロ。
