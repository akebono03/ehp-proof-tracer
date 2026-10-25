# Phase 168 R3-41P18 — Origin Observation 信頼境界監査

## 目的と対象

GitHub `akebono03/ehp-proof-tracer` の `develop` を確認したうえで作成した **AUDIT_ONLY（監査のみ）** パッケージ。現行コード確認時のコミットは `784e9c0c04970c123bc1c01c2ce1d9a87e7613ef`。

Phase 168 R3-41P17 が実装した `capture_search_origins()` と `build_origin_bound_narrative_model()` を、標準 Web へ採用する前に監査する。**意図的に脆弱な Python API 呼び出しを模擬する監査であり、インターネット越しの攻撃が成立するとの主張ではない。**

## 追加するファイルと関数

アプリ本体の変更対象ファイル・クラス・メソッド：**なし**。既存 API・既存テストも変更しない。

新規追加位置：リポジトリ直下 `phase168_r3_41p18_origin_boundary_audit/`。

- `__init__.py`：パッケージ初期化のみ。
- `audit.py`：`source_hashes()`、`search_with_context()`、`project()`、`expected_rejection()`、`audit_real_case()`、`audit_scope_limits()`、`render_report()`、`collect_report()`、`main()`。いずれもこの新規モジュール内に追加。
- `tests/test_phase168_r3_41p18_origin_boundary_audit.py`：限定監査テスト。ファイル内の必要な import とテスト関数はすべて省略なしで収録。
- `run.ps1`：Windows PowerShell 用、一度の監査・限定テスト・レポート収集。
- `INSTRUCTIONS_JA.md`：この説明全文。

## 実行

PowerShell から、作業リポジトリで実行する。

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p18_origin_boundary_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p18_origin_boundary_audit\run.ps1"
```

前提として R3-41P17 が正常に適用済みで、`proof_origin_capture.py` とその関連 API が存在する必要がある。

`run.ps1` は以下を順番に実行する。

1. 監査開始前の関連ソース SHA-256 を保存。
2. 正規の $\pi_3^2,\pi_4^3,\pi_5^4$ の探索と、実験的 origin handoff の一致確認。
3. 明示的 note 関数で生成した記録の不適切な受理、target の不一致、Bridge ラッパー差し替え、同一 scope で複数探索が混在する問題を**再現・計測**。
4. 既存 P17・P16・P15・P13・P12、Factory と Bridge の限定 pytest。
5. P12 の publication order（文献順）監査。
6. SHA-256 を比較し、アプリ本体が変更されていないことを確認。
7. `output/audit.json`、`output/audit.md`、ログ、`output/review_bundle_日時.zip` を出力。

レポートの `ORIGIN_BOUNDARY_GAPS_CONFIRMED` は、未修正の弱点が検出され、監査の期待結果と合致したことを意味する。**安全性が完成したという意味ではない**。

監査用テストは `audit.json` の直前の実行結果を検査する。単独の pytest を直接実行する場合、最初に `python -B -m phase168_r3_41p18_origin_boundary_audit.audit` を実行する。

## 境界と完了条件

今回の完了条件：正常な3群の全文・Citation 一致、限界の再現、限定 pytest PASS、監視対象のハッシュ不変。

P17 の origin handoff を標準 Web へ接続しない。`PartialProofResult` や `ProofNarrativeModel` に認証フラグを追加しない。既存 matcher の再検証・Renderer の数学的チェック2箇所を削除しない。

次の R3-41P19 の範囲は、信頼できる canonical search invocation（正規探索呼出）と結果・文献位置・screened bridge を同じ単位で結び付ける最小設計とする。新しい数学的エンジンや新たな規則台帳を先取りしない。

**Phase 全体 pytest は Phase 168 の最後だけ実行するため、この ZIP には含めない。**
