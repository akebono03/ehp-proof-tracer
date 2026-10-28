<!-- PHASE169_R10ET_DOCUMENT_CLOSEOUT_20261028 -->

## 2026-10-28 — Phase 169 R10ET 共通 Definition・Reference の証明監査記録

**記録区分：** 既存 Toda 命題・群構造 DB・型付き Proof Tree に対する本番探索と表示の回帰監査。新たな数学的定理の発見・原典命題の独立した形式証明・任意次元の完全自動証明を主張しない。

### Definition と独立した証明祖先

R5D の本番探索では、安定範囲の厳密な型付き `GeneratorImage`（生成元像）に該当する場合だけ、共通 Definition の正規 `INFERENCE` を優先する。これは対象の生成元像を与える既存の規則であり、前段の群構造や同型の根拠を省略できることを意味しない。DB prior（既出の群構造）と Toda `(4.5)`（安定懸垂同型）は、使用される場合にそれぞれ独立した引用付き `GIVEN` の根拠として必要である。旧個別 Definition が登録済みであることは、実際の完成証明がそれを引用したことを意味しない。

### $\pi_{10}^{8}$ の使用引用と未使用引用

R6B で確認した当初の証明木は `COMPLETE`、Trust PASS、共通 Definition に該当する生成元像4件をすべて正規 `INFERENCE` で実装（`ELIGIBLE=4`、`CANONICAL=4`、残存依存0）。ただし検索結果の9 `ProofStep` のうち、`sphere.csv` の `(n=7,k=2)` に由来する DB prior は結論の祖先ではなかったため、完成証明 Reference [R1] と本文への掲示は不適切だった。

R6C では Proof Tree 全9ステップを保持したまま、root から到達できる8ステップだけを完成証明の本文・Reference の対象にした。実際の結論を支持する引用は `sphere.csv` の `(n=4,k=2)` の DB prior と Toda `(4.5)` の2件であり、順に [R1]・[R2] として表示する。**表示対象を絞ったことは、証明の前提や推論を削除したことではない。** Partial（未完成）証明の観測経路は従来のまま保持する。

### 対象群と検証結果

R6 の必須16ケースは $\pi_{69}^{43}$、$\pi_{56}^{30}$、$\pi_{41}^{30}$、$\pi_{44}^{30}$、$\pi_{46}^{30}$、$\pi_{39}^{30}$、$\pi_{3}^{2}$、$\pi_{4}^{3}$、$\pi_{5}^{4}$、$\pi_{4}^{2}$、$\pi_{5}^{3}$、$\pi_{6}^{4}$、$\pi_{28}^{22}$、$\pi_{32}^{22}$、$\pi_{23}^{15}$、$\pi_{33}^{24}$。追加3ケースは $\pi_{10}^{8}$、$\pi_{22}^{13}$、$\pi_{24}^{15}$。R6D で19件すべて `CHECK=PASS`、Trust PASS、共通 Definition 適用可能な個別 Definition への残存依存0件と判定した。

R6D の実行結果は `R10ET_R6_REQUIRED_PASS=True`、`R10ET_R6_PROBES_PASS=True`、`R10ET_R6_AUDIT_ONLY_COMPLETE=PASS`、限定 pytest **24 PASS**、`R10ET_R6D_COMPLETE=PASS`。R6C の実装時には限定 pytest **43 PASS** と19件の追加監査 PASS を確認した。監査出力：`phase169_r10et_r6_residual_definition_dependency_audit/output/20261028_174644_215/audit.md`。Git index は変更されなかった。

**検証境界：** この有限集合の成功から全登録群・全 stem の完成証明や `HyoujiGen.csv` の全データの数学的正しさを演繹しない。新たな数学的命題は登録せず、Phase 169 全体の全体 pytest および正式終了認定は未実施とする。
