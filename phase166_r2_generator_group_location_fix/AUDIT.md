# Phase 166 R2 入力 CSV 所在修正

## 原因
前版では `sphere(3).csv` がリポジトリ直下または `data/` にあることを前提としていたが、実環境には存在せず監査が失敗した。

## 変更対象
- `phase166_r2_generator_group_location_fix/audit.py` の `main()`：入力ファイル検索先に同梱 `data/` を追加。全関数を維持したまま検索処理を修正。
- `test_audit.py`：同梱データ行数テストを追加。
- `run.ps1`：限定テストのみ実行。
- `data/sphere(3).csv` と `data/HyoujiGen.csv`：ユーザー提供の元データを変更せず同梱。

## 完了条件
2つの入力 CSV を読めること、生成元 ID の対応が得られること、証明資格0件の維持、限定 pytest PASS。

## 次段階との境界
本修正は入力所在の問題のみ対象とし、R2 の数学的同一性認定および R3 の証明資格付与は行わない。全体 pytest は Phase 166 R10 まで行わない。
