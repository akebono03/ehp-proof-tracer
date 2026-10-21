# Phase 166 R3-AU-8 監査記録

## 変更対象

新規 `audit.py`：`read_rows`、`parse_ids`、`inspect`、`main`。
新規 `test_r3au8.py`：3件の限定テスト。
新規 `run.ps1`、`README.md`、`AUDIT.md`。既存本番コードは変更しない。

## 対象

`data/sphere.csv` の Element ID 列と `data/HyoujiGen.csv` の定義を全行で照合し、元のメタデータを監査出力に保持する。
`generator` は参考情報のみ。`gen_coe` は直和成分の係数で、Element の合成因子数とは一致させない。

## 既存コードの接続境界

`repository.SphereRepository.get_group()` は `element` と `gen_coe` を整数配列として保持する。
`expression.Composition.is_type_compatible()` は左の source と右の target の一致を要求する。
`render_toda_expression_latex` は Composition、Sum、Multiple を表示できる。
ただし表示元 ID の始域・終域を検証可能な型に変換する橋渡しは、この Phase では追加しない。

## 完了条件

全行の ID と元定義のメタデータを対応付け、ID 解決可否と型検査未認定を明確に出力する。全体 pytest は Phase 166 終了時のみ実施。
