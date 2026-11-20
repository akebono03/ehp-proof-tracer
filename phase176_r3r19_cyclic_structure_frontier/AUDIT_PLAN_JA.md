# Phase 176 R3R19 監査計画

## 対象

R3R18 で子 Goal に候補0件と報告された `CyclicStructureStatement`（位数2）を対象とする。根の3候補は有限巡回構造規則2件、等式の対称性1件である。

## 数学上の境界

R3R16 では `E(η₂∘ν′∘η₆)=0` が出典付き推論により示された。しかし、写像の核に属することだけから `π₈³` が位数2の巡回群であるとは結論できない。群の位数と当該生成元の位数、または単射な Hopf 写像と像の生成性など、独立した証明義務を要する。

## 変更対象

- `phase176_r3r19_cyclic_structure_frontier/audit.py`：新規監査関数 `git`, `check_sources`, `preflight`, `summarize`, `observe`, `worker`, `report_path`, `execute`, `main`。
- `phase176_r3r19_cyclic_structure_frontier/tests/test_audit.py`：新規限定テスト4件。
- `phase176_r3r19_cyclic_structure_frontier/run.ps1`：DryRun、本実行、限定 pytest。
- 本 README、監査計画、コード全文文書。

既存プロダクションコードの変更なし。追加 import は全て新規ファイル内。既存のクラス・メソッドの変更なし。

## 検証・完了条件

- `develop`、追跡ファイルのクリーン状態、現行コードの主要アンカーをチェック。
- 型付き根 Goal と巡回構造の子 Goal を取得し、共有候補と2経路の候補および子 Goal を記録。
- `search_failed` が改善されなければ未完成として記録し、証明済みと誤判定しない。
- 限定 pytest 4件。全体 pytest は Phase 終了時まで行わない。

## 次工程との境界

R3R19 は監査のみ。R3R20 以降で、証明可能な前提が存在する経路に限り一般規則の接続を検討する。根の直接 GIVEN、専用証明、専用 Narrative は追加しない。
