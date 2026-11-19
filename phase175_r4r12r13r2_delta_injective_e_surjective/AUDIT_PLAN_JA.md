# R13R2 監査計画

1. 現行 GitHub `develop` の `phase165_r14_r6_generic_iso.py`、`phase165_r12_r12_ehp_consequences.py`、`phase165_r12_r11_prop42_unified.py`、`phase175_r4r10_cited_58_prop25_public/{source,provider}.py` を確認した。
2. `π₉⁹=0` を必要とする既存の E 全射分岐を、今回の完成証明として採用しない。
3. 自由巡回群から自由成分が非零の直和群への写像の単射性を、3件の独立した証明済み前提から導く。
4. Δ 単射と H–Δ、E–H の完全列2件から E 全射を導く。
5. テストは本パッケージの5件に限定し、公開 Provider 接続や全体 pytest を行わない。

## 完了条件

- 全ての新規規則が未証明候補を GIVEN として扱わないこと。
- `Toda (5.8)` の Δ が EHP の該当 Δ と一致すること。
- 零の自由成分、別の生成元、不正な懸垂次数を拒否すること。
- 本番の Proof Search と群構造完成は次工程で検証すること。
