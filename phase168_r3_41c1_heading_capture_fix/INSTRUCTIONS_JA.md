# Phase 168 R3-41C1 — 見出し取得検査の修正

## 原因

R3-41C の Web 表示テストと監査が `line.segments` だけを結合していたため、`kind="heading"` に保持された `line.prefix`（「探索診断」など）を見落とした。

## 変更対象

- 新規 ZIP 内 `tests/test_phase168_r3_41c1_heading_capture_fix.py`: `_text()` 全文を修正し、未解決 Goal・探索診断の見出しが `WebGroupProofRenderedLineView` に存在することも検証。回帰テスト1件を追加。
- 新規 ZIP 内 `audit.py`: `read_text()` 全文を修正し、見出しの存在を検証。
- 新規 ZIP 内 `run.ps1`: R3-41C1 の新パッケージをモジュールとして起動。
- 実装対象 `web_group_proof.py`: `build_web_partial_group_proof_view()` は R3-41C と完全一致。
- 実装対象 `phase165_r52_r4_flask_bridge.py`: `build_group_proof_progress_view()` は R3-41C と完全一致。
- import 部は変更しない。

## 実行

リポジトリ直下で以下を実行する。

```powershell
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41c1_heading_capture_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41c1_heading_capture_fix\run.ps1"
```

## 完了条件

- 今回の限定 pytest 全件 PASS。
- `NOT_SEARCHED`, `PARTIAL`, `SEARCH_FAILED` の状態、未解決 Goal と探索診断の見出しが残る。
- 完成4群と明示 legacy と直接 Adapter fallback が変更前後でバイト単位一致。
- 確認されていない Reference は追加しない。
- 失敗時は2つの実装ファイルを元に戻す。

次工程 R3-41D の実部分証明監査までは旧互換経路の削除・全体 pytest は行わない。
