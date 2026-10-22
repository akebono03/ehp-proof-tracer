# Phase 168 R2-8③ 修正記録

## 既存コードと限定テストの確認

GitHub `develop` の `phase166_r3t_goal_source_binding/goal_source.py`、`phase166_r3aj_structured_generator.py`、`expression.py`、`homotopy_groups.py`、`phase168_r2_8_1_citation_mismatch_audit/audit.py` および R2-8①関連テストを確認した。R2-8②の提出済み `structured_comparison.json` では、9件の goal と DB goal が完全一致し、具体的な命題の照合では名前や source/target の相違などが残った。

## 変更範囲

1. 変更対象は `phase166_r3t_goal_source_binding/goal_source.py` の `_same_group_structure()` 全体のみ。import 部分は変更しない。
2. 新規ファイル `phase168_r2_8_3_generator_identity/identity.py` に既存 `HyoujiGen.csv` の ID 2,3,4 の実メタデータに基づく限定的な照合関数を追加。
3. 新規限定テストは `tests/test_r2_8_3_generator_identity.py` の7関数。既存テストは変更しない。
4. `apply.py` による変更前バックアップと `run.ps1` による限定テストおよび引用再監査。

## 判断境界

型付き生成元の `GeneratorSymbol`、具体次数、既知 source/target、合成因子の隣接次数、有限巡回群の位数、直和成分の順序を比較する。型付き表現として不十分な場合は照合を拒否する。固定文献命題の選択・掲載順・重複排除は既存 resolver のまま。一般命題の特殊化はこの Phase に含めない。全体テストは Phase 最後のみ。

## 実行後に確認すること

限定 pytest が PASS すること、7件の具体的出典が一意に解決されること、未特殊化の2件が UNRESOLVED のままであること。実行前にこれらの実行結果を認定しない。
