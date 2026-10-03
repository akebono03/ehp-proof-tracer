Phase157 R11-R1 repair1

前回の audit script は current API に対して
`build_toda_group_proof_narrative_ordered_contributions()` の
`proof_chains` 引数が不足していた。

repair1 は current production flow と同じ順序で:

1. base_markdown を生成
2. proof_chains を生成
3. ordered contributions を
   current_markdown=base_markdown 付きで生成

する。

Production code changes: none
Test code changes: none
pytest: not run

この監査結果を R11-R2 の最小実装根拠にする。
