# Phase 166 R3-AU-2 監査

## 変更対象

- 新規 `phase166_r3au2_generator_join_audit/audit.py`：`read_csv`, `locate`, `parse_ids`, `classify_gen_coe`, `inspect`, `write_csv`, `main`
- 新規 `phase166_r3au2_generator_join_audit/test_r3au2.py`：限定テスト3件
- 新規 `run.ps1`、README.md、AUDIT.md
- 既存 production code・既存テストは変更しない

## 方法

全行を `Element` の識別子をキーとして `HyoujiGen.csv` と照合する。未知 ID、重複 ID、空の `Element`、不正値は個別分類する。`gen_coe` は係数列の形のみ分類し、`Element` と係数位置との数学的対応は仮定しない。

照合結果は `all_rows.csv`、要確認行は `review_rows.csv`、特殊名称の抽出は `special_generators.csv` に保存する。名称の抽出は探索補助であり、全件確認を意味しない。

## 完了条件

DB の全行が結果に現れ、高次 stem が残り、各行について ID 対応状態・係数列の形・基礎生成元の表示候補を記録できる。数学的同一性および LaTeX 正確性の認定はゼロのままとする。

## 次段階との境界

この監査は意味づけや production renderer の改修をしない。DB と既存の型付き表現との数学的橋渡しは別工程で検証する。

全体 pytest は Phase 166 終了時のみ実施する。
