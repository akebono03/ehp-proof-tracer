# Phase 175 R4R12R5R2 — ZIP ルートの修正

- 原因：R4R12R5R1 の ZIP 内に余分な `r4r12r5r1_build/` が含まれ、既存の `installer.py` が上書きされなかった。
- 修正対象：ZIP の格納階層、および説明文書のみ。実装の論理は変更しない。
- 配置：`phase175_r4r12r5_iterated_suspension_endpoints/installer.py` をリポジトリ直下へ展開する。
- `EXPECTED_HEAD` は `9203e1a8c077320a58214bda40d9bfeb17704f58` に固定する。
- 検証：展開先、ソース値、限定 pytest、DryRun と本実行、既存 R4R3 規則の6つの義務を確認する。
- 新規 GIVEN・新規数学規則なし。全体 pytest は実施しない。
