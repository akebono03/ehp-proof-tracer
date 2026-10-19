# Phase 165 R6-8 Phase 58 切替

## 変更対象
- `probes/probe_phase58_capabilities.py` の import 全体と `build_phase58_representative_result` 全体（実行時に既存コードから生成し、ファイル全体を書き換える）
- 新規 `test_phase165_r6_8_phase58_cutover.py` の2テスト関数と import 全体
- 新規 `install_and_test.py`、`run.ps1`、`README.md`

## 内容
Phase 58 の旧 Phase 50 probe に依存した `pi4_3_step` を、共通 `search_group_from_registered_goal(n=3,k=1)` が返す検証済み INFERENCE の結論から取得する。旧規則を復活させない。既存の `phase50` 戻り値キーは、使用していた `final_group_steps` のみに限定して維持する。旧 Phase 50 の数学的結果すべてを再現するものではない。

実行時は変更前の既存コードが想定したものと一致するか4箇所を照合。不一致の場合は変更せず停止。元ファイルを `.r6_8_original.bak` にバックアップ後、ファイル全体を置換。新規限定テスト2件を実行し、失敗または90秒タイムアウトならコードを元に戻す。既存の任意のバックアップは上書きしない。

## 実行
`powershell -ExecutionPolicy Bypass -File .\phase165_r6_8_phase58_cutover\run.ps1`

## 完了条件
限定テスト2件 PASS。105件すべての収集エラーはこの変更だけでは解消されないので R6-8 の最終完了扱いにはしない。Phase 53/55 等は未変更。全体 pytest は Phase の最後のみ。
