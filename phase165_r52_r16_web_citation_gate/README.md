# Phase 165 R52-R16 — Web 共通探索の引用前提審査

## 変更対象（最初に確認）

- `phase165_r52_r9_shared_math.py`: `build_shared_typed_bridge()` のレコード ID 名寄せ1箇所、および `search_shared_group_goal()` 全体
- 新規 `phase165_r52_r16_web_citation_gate.py`: `screen_shared_proof_context()`（共通条件で ProofStepLink を審査）
- 新規 `test_phase165_r52_r16_web_citation_gate.py`: テスト関数4件
- `install.py`, `run.ps1`: 既存ファイルのバックアップを作り、対象 pytest だけ実行

## 信頼境界

採用済み Toda TeX に由来する既存の型付き GIVEN は、これまでの採用済み文献ポリシーを維持します。原著独立照合済みとは認定しません。これ以外の命題は Phase 164 R2 の **順序・検証済み ID・依存関係** 判定が ALLOWED の場合のみ、共通探索に証人として渡します。証明対象そのものの引用も除外します。

`R15` の厳格照合は文献掲載位置が未確定の命題を自動承認しません。既存採用済みソースについては従来契約を残す過渡設計であり、全 Source Registry の厳密引用統一が完了したとは主張しません。

## 実行

リポジトリルートで:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r52_r16_web_citation_gate.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r52_r16_web_citation_gate\run.ps1"
```

## 完了条件

- 確認済み先行 Reference は採用、未確認・後続・異文献は除外
- $\pi_3^2$ の最終目標を直接 GIVEN にしない
- R9/R14/R15 関連テストが PASS
- 全体 pytest は Phase 165 終了時のみ

## 次 Phase 境界

R16 は検索前提の選別のみ。一般形の条件付き特殊化、全命題の掲載位置確定、Web の部分表示／完成表示の一元化は対象外。
