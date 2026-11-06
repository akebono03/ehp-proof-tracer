# Phase 174 R3-R7-R13 — 一般消滅関係の独立文献登録と型付き証明監査

## 目的と前提

R12 において Toda (5.9) の一般命題の転写と独立特殊化規則を検証した。しかし、公開 Registry の一般命題 GIVEN は0件、公開の左因子零関係候補1件は等式の対称性のみだった。

今回、採用 TeX `sources/toda/Toda_05_2.tex` の一般関係 `$\nu_n\circ\eta_{n+3}=0\ (n\ge6)$` を、文献マニフェストの `(5.9)` source-order position と照合し、独立した `RegistryBridgeResult` に一般命題だけを出典付き GIVEN として登録する。`$\nu_6\circ\eta_9=0$` は R12 の型付き推論で導き、GIVEN にはしない。

## 変更ファイルと全関数

既存ファイルは一切変更しない。新規ディレクトリ `phase174_r3_r7_r13_cited_annihilator_bridge/` のみ。

- `registry.py`：`reviewed_toda59_source_position()`、`build_isolated_toda59_annihilator_bridge()`、`join_isolated_source_bridge()`。
- `audit.py`：`git()`、`git_blob_sha()`、`matches_source_blob()`、`verify_git_and_sources()`、`previous_report_path()`、`validate_r12_report()`、`inspect_isolated_registration_and_proof()`、`output_path()`、`make_report()`、`main()`。
- `tests/test_registry.py`：`manifest_fixture()` と文献・型付き推論・独立 Registry に関する全テスト。
- `tests/test_audit.py`：`sample_r12()` と前工程・Source Guard・非公開接続に関する全テスト。
- `run.ps1`：限定 pytest の分割実行、DryRun、本監査。
- `README.md`：英語の実行説明。
- `AUDIT_PLAN_JA.md`：本計画。
- `CODE_FULL_JA.md`：import・クラス・関数・テスト・スクリプトの全文。

新規クラスは定義しない。新規関数は上記の各新規ファイルの冒頭 import 群の直後から定義する。

## 証拠の独立性・禁止事項

- Source-first：文献原文、掲載位置、型付き生成元 ID をそれぞれ検査。
- source-order position 9300 は採用テキストの順序であり、原著印刷版の位置は未検証。
- 一般命題のみ Source GIVEN とし、具体的零関係、ImageZero(E)、目標群零の直接 GIVEN を禁止。
- R12 の全監査 JSON を必須とし、DryRun のみの JSON を拒否。
- 出典・HEAD の固定 SHA と改行正規化による Source Guard を維持。
- 独立した Registry のみを構築し、公開 Provider・GIVEN・Narrative・Web を変更しない。
- First Successful Proof Search 方針を維持し、唯一性検査や群専用 Narrative を追加しない。

## テスト・完了条件と次段階の境界

DryRun → 本実行で R13 と R12〜R3・数学/系列の限定回帰テスト、Source Guard を実行する。一般命題の source-screened GIVEN が隔離環境で1件、具体例の検証済み INFERENCE が1件、公開一般命題は0件のまま、という実測を JSON に記録する。**これらは根の完成証明を意味しない。**

次の R14 以降で公開経路への最小接続と、合成零→巡回群の零像→EHP 完全列の公開証明再評価を行う。全体 pytest は Phase 174 終了時にのみ行う。
