# Phase 170 R3-R9 — Toda (7.12) による生成元等式の引用接続

## 監査結果

R3-R8R2 で $n=2, 1\leq k\leq33$ の33件中32件が完成。$k=12$ に限り、既知の先行 DB の群構造と対象の生成元の表現が一致しないため、共通 (5.2) 輸送の候補が生成されない。

$$
\varepsilon_3\circ\nu_{11}=\nu'\circ\bar\nu_6
\quad\text{(Toda (7.12))}
$$

## 最小修正

`phase170_r3_r9_toda712_cited_rewrite/source712.py` に、採用された Chapter VII の TeX を Git blob で検証し、`HyoujiGen.csv` の元 ID から両辺を型付きで構築する処理を追加する。文献の掲載順は採用 TeX の相対行順から構築し、原著の独立監査済みとは主張しない。これは FIXED_STATEMENT として登録するが、証明済み群や架空の ProofStep は登録しない。

`phase168_r2_toda52_transport.py` の既存関数に、直接一致しない場合のみ、検証済み等式を**第3の下位 Goal** として要求する推論を追加する。関係式なしで DB 群と対象生成元が同じという判断はしない。

`phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py` に当該引用登録を接続する。他の32件の経路と R10E4 の DB 前提検証・Web Trust Boundary は維持。

## テストと完了条件

限定 pytest の成功、$k=12$ の `COMPLETE`、公開 Web で `generic-complete-proof`、(7.12) の引用が実際の Proof Tree に含まれること。$k=5,6,8,10,11,14$ の回帰確認。全体 pytest は Phase 170 終了時のみ実行。
