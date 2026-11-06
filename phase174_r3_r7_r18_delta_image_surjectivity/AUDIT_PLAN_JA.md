# Phase 174 R3-R7-R18：一般 Delta 像の全射性推論監査

## 目的

R17 で未解決の `MapSurjective(Delta: pi_13^13 → pi_11^6)` に対し、同型と全射を循環させることなく、次の一般推論の型付き義務を作る。

$$
\operatorname{im}\Delta=\mathbb Z\{g\},\quad
\pi_{11}^{6}=\mathbb Z\{g\}
\quad\Longrightarrow\quad
\Delta:\pi_{13}^{13}\twoheadrightarrow\pi_{11}^{6}.
$$

1. `phase174_r3_r7_r18_delta_image_surjectivity/rule.py` の新規 `delta_surjectivity_image_inputs`、`delta_surjectivity_from_full_free_cyclic_image_rule`、`expand_delta_surjectivity_from_full_free_cyclic_image` を追加する。
2. すべての条件を型で検査し、結論を生成できるのは **2件とも INFERENCE で検証された ProofStep** が存在するときだけとする。
3. `exact_prior_database_result` の表現は探索用 Goal の候補であって、R18 の独立推論の前提を証明したことにはしない。
4. Phase 165 の一般 Delta image 規則、Toda Proposition 4.2、R3/R17 の公開根の状態を監査する。
5. 本番 Provider・GIVEN・Narrative・既存テスト・5主要ドキュメントは変更しない。全体 pytest は Phase の終わりに限る。

## 完了条件

- GitHub develop HEAD とローカル引き継ぎ状態を比較して、Source Guard PASS。
- 目標の一般 Delta 全射性について独立の候補1件、下位の2つの未証明 Goal が正確に生成される。
- 既存公開 Provider は Delta 全射性候補0件のまま、未完成の証明を誤って完成扱いしない。
- 既存の関連 pytest と新規限定 pytest が PASS。
- 将来 R19 における公開接続を先取りしない。
