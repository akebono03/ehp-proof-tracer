# R45R1 限定 pytest ImportError 修正

## 現象

R45 の Source Guard / DryRun / 監査本体は PASS したが、`PROP42_SPECIALIZATION_REGRESSION` の pytest 収集中に `GENERAL_ASSERTION_ID` の ImportError が発生。`phase165_r12_r11_prop42_unified.py` と同名の `phase165_r12_r11_prop42_unified/`（テスト用ディレクトリ）が存在するため、`--import-mode=importlib` で名前空間が衝突する。同構造を持つ `phase165_r12_r12_ehp_consequences/` にも同じ衝突リスクがある。

## 変更対象（最小）

1. `phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1` 全文を置換。2つの歴史的 Proposition 4.2 回帰テストだけ `--import-mode=prepend` とする。他の限定 pytest は `importlib` のまま。
2. `phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py` 全文を置換。runner の Import Mode 選択を守るテスト関数を追加。

本番ファイル、数学的推論規則、出典、R45 の `audit.py` / `source_guard.py` は変更しない。

## パッチ・実行順

- 新規 `phase174_r3_r7_r45r1_pytest_importmode_fix/` に、比較可能な旧版・全文置換版、ガード付き `patch.py`、`run.ps1`、限定テストを追加。
- DryRun で GitHub `develop` HEAD / source pins / 既存 R45 対象ファイルの内容を検査し、書き換えない。
- 本実行で対象2ファイルのみ置換し、元の R45 監査と限定 pytest を再実行する。
- 最後に R45R1 の限定テストを実施する。
- 全体 pytest は Phase 174 の最終工程まで行わない。

## 完了条件と次工程との境界

R45R1 完了条件は修正後 R45 の限定 pytest と R45R1 の限定テストがすべて PASS すること。R45 監査 Gate の `CANONICAL_INFERENCE_PENDING` は変更しない。Prop.4.2 の Provider 候補の存在と、実際の `INFERENCE` の成立は別物であり、後者の調査は以後の工程で行う。
