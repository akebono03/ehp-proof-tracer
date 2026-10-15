# Phase 165 R5-R8：公開入口の境界監査

## 現状と目的

R5-R7 で現在の Web Group Proof から旧 Phase 162 Narrative への静的 import 経路は見つからなかった。R5-R8 ではその調査を CLI・Generator の既知の入口へ広げるとともに、旧 Phase 162 関数を直接呼ぶ箇所を特定する。

## 追加・変更するファイル

- `phase165_renderer_r5_r8_boundary_audit/audit.py`（新規、読み取り専用監査）
  - `active_sources`、`shortest_path`、`investigate`、`render_report`、`main`
- `phase165_renderer_r5_r8_boundary_audit/test_audit.py`（新規）
  - 6つの限定テスト
- `phase165_renderer_r5_r8_boundary_audit/run.ps1`（新規）

既存のクラス・関数・import は変更しない。追加位置はプロジェクトルート直下の独立フォルダー。

## 限定テスト

```powershell
python -m pytest -q .\phase165_renderer_r5_r8_boundary_audit\test_audit.py
```

監査ロジックの単体テスト：6件成功。ユーザーの Windows リポジトリにおける監査は未実施。

## 完了条件

- 既知の公開入口から旧 Phase 162 への静的 import 経路を表示する。
- 旧 Phase 162 の直接 import 呼び出し箇所を表示する。
- Group Proof と Generator・CLI の関数内部の呼び出し名を表示する。
- `audit.json` と `review.md` を保存する。
- 解析エラーがないことを確認する。

監査成功は実行時に独立経路が存在しないことの証明ではない。R5 の最終認定は後続の判断を要する。

## 次の作業との境界

監査結果で現行公開経路から旧 Phase 162 への到達が疑われた場合のみ接続元を変更対象として検討する。旧 Phase 162 fixture 6件の不整合は未解決のまま維持。全体 pytest は Phase 165 の終了時だけ行う。
