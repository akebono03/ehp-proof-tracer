# Phase 174 R56R1：監査出力先の型エラー修正

## 事象と原因

R56 の DryRun、Source Guard、数学的規則の共通接続と限定 pytest 64 件は PASS。その後、`audit.py:110` の `"EHPProofTracerAudit" / "phase174_r3_r7_r56"` が文字列同士の `/` 演算となり TypeError。`inspect_public()` はその直前に終了しているため、数学的検査を実行してから出力保存だけで停止した。

## 今回の最小変更

既存ファイルで変更するのは `phase174_r3_r7_r56_cyclic_generator_bridge/audit.py` の `main()` だけ。式を

```python
destination /= Path("EHPProofTracerAudit") / "phase174_r3_r7_r56"
```

に変更する。既存 import、`inspect_public()`、数学的規則、共通 Provider、Renderer、Source は変更しない。

## ガード

現行 GitHub develop の既存共有 Provider を R56 Installer の Source Guard で検証し、さらに R56 配布 ZIP に含まれる `audit.py` 全文の SHA-256 を検証する。LF/均一 CRLF は受け付けるが、未知のファイル編集と混在改行は拒否する。再実行可能。

## 限定テスト・完成条件

- R56R1 のパッチ単体 pytest 5 件が PASS（ローカル環境で確認済み）。
- Windows 側で `python -B -m phase174_r3_r7_r56_cyclic_generator_bridge.audit` が終了コード 0 を返す。
- `public_proofs.json` を出力し、`PASS_R56_TWO_GENERAL_RULES_SOURCE_FIRST_PUBLIC` を返す。
- `pi11_6_complete` / `pi12_7_complete` / 先行 DB 結果の再証明なし等を改めて確認する。
- 新規 GIVEN=0、数学的規則=0、全体 pytest は実施しない。

## 次 Phase との境界

本修正は監査結果保存の型エラーの修正のみ。数学的証明規則や一般 Narrative の機能拡張はしない。
