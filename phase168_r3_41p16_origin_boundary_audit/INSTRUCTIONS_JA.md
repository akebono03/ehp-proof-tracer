# Phase 168 R3-41P16 — 推論規則・Bridge 由来の読み取り専用監査

## 監査の位置づけ

R3-41P15 の fail-closed（検証不能なら拒否）を維持したまま、標準 Web 経路の実際の3群について `InferenceRule`（推論規則）と `RegistryBridgeResult`（命題台帳の接続情報）の由来を測定します。

本 ZIP は **AUDIT_ONLY** です。アプリ本体、既存テスト、Renderer、Proof Narrative Model、固定基準ファイルを変更しません。今回の追加対象は `phase168_r3_41p16_origin_boundary_audit/` の新規監査ファイルだけです。既存関数・クラス・import の変更はありません。

## 観測する経路

- `phase165_r3_recursive_search.reconstruct_registered_goal()` における採用済み推論のファクトリ生成
- `phase165_r52_r2_search_adapter.search_registered_partial_proof()` からの探索イベント
- 探索に渡された Bridge と `context_sink` に渡された Bridge の同一性
- GIVEN が登録済みの選別済み出典と一致するか、文献順で先行するか
- Model が ProofStep オブジェクトをそのまま保持するか
- $\pi_3^2$、$\pi_4^3$、$\pi_5^4$ の固定全文・Reference・Citation の一致
- 自作規則・自作 Bridge に対する既存 verifier（検証関数）の保証の限界

診断には `unittest.mock.patch` を使いますが、既存関数を正常に呼び出す薄い wrapper（包み込み）だけです。**実際の探索の判定や証明データを変更しません。**

## Windows PowerShell

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p16_origin_boundary_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p16_origin_boundary_audit\run.ps1"
```

監査だけを先に試す場合は `-SkipTests` を付けられます。

## 出力

- `output/audit.json`：3群のファクトリ由来、検索観測、Bridge 同一性、Reference/Citation 比較
- `output/audit.md`：監査結果と次工程の設計判断
- `output/pi3_2_current.md` など：3群の全文および Reference・証明の抽出結果
- `output/audit_stdout.log`、`output/audit_stderr.log`：監査ログ
- `output/pytest_focused_stdout.log`、`output/pytest_focused_stderr.log`：限定 pytest の結果
- `output/review_bundle_日時.zip`：上記の監査結果まとめ

## 完了条件

- INFERENCE 13/19/7件のすべてが探索時の `derive_inference_proof_step()` とオブジェクト同一である。
- GIVEN 5/6/3件のすべてが、正規探索へ渡された screened Bridge と対応し、文献順で先行する。
- 探索の `proved` イベントと ProofStep、Proof Narrative Model の対応が確認できる。
- 3群の公開証明本文・Reference・Citation が既存固定基準と全文一致する。
- 自作規則や自作 Bridge を既存 matcher に渡すだけでは独立の数学的正しさを保証できない、と明確に確認できる。
- アプリ本体と固定基準の SHA-256 が実行前後で不変である。

## 次工程との境界

R3-41P16 では、探索時に検証された事実を受け渡す仕組みを **実装しません**。次工程で、検証証跡の発行位置・改変防止・既存 API と partial の扱いを決めます。新しい検証エンジンや独立規則台帳は導入しません。Renderer に残る `_stable_eta_renaming_shape()` と `prop42_exactness_indices()` は維持します。

**全体 pytest は Phase 168 終了時まで実行しません。**
