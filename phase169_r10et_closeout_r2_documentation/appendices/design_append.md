<!-- PHASE169_R10ET_DOCUMENT_CLOSEOUT_20261028 -->

## Phase 169 R10ET — 共通 Definition と証明に必要な引用の境界（2026-10-28）

### 本番探索での Definition（定義）の責務

R10ET-R5D は `phase165_r52_r9_shared_math.py::shared_expansion_provider()` の探索候補順を修正した。型付き `GeneratorImage`（生成元の写像像）が安定範囲の共通 Definition に厳密に適合するときだけ、独立に replay（推論再生）できるゼロ前提の `GoalExpansion` を優先する。不適合な対象では既存の探索候補を引き続き使用する。新たな個別 family 名や群ごとの例外規則は導入しない。

共通 Definition は生成元像の既存の型付き関係に適用するものであり、群構造、Toda (4.5) の同型性、あるいは異なる生成元の同一性を独力で確定するものではない。DB prior（既知の群構造）と Toda (4.5) は、完成証明で実際に使用される場合、独立した引用付き `GIVEN` の祖先として保持する。`HyoujiGen.csv` を含む既存の生成元データとの接続を維持し、表示文字列・family 名を証明根拠の代替にしない。個別 Definition の旧台帳エントリは、この作業で削除していない。

### Proof Tree と Narrative / Reference の責務分離

R10ET-R6C は `phase168_r3_3_proof_narrative_model.py` の `root_ancestor_step_indices()` と `build_proof_narrative_model()`、`phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` を更新した。**完成証明**の本文と Reference の対象は、選択された root（結論）から前提をたどって到達できる検証済み ProofStep のみとする。これにより、探索結果中に保持された別経路の未使用 `GIVEN` を Reference に混入させない。採用引用には連続した番号を割り当てる。

Proof Tree 自体・探索結果の全 `ProofStep`・既存の Trust Boundary（信頼境界）・部分証明の観測情報は変更しない。表示層は命題・推論・DB 情報を新たに生成しない。モデルの祖先関係が不正であれば fail-closed（安全側で拒否）とし、文献名の一致だけで祖先とみなさない。

### 監査結果と適用範囲

R6B の $\pi_{10}^{8}$ は `COMPLETE`・Trust PASS、共通 Definition 適用可能4件・正規実使用4件、残存依存0件だった。元の Reference [R1] は `sphere.csv` の `(n=7,k=2)` の未使用 DB prior で、結論の祖先に含まれなかった。R6C は9個の検索済み ProofStep を保持しながら、root から到達できる8個だけを完成証明に表示し、実際の証明に必要な `(n=4,k=2)` の DB prior と Toda `(4.5)` を [R1]・[R2] として表示した。

R6D は R6 の `certify_reviewed_production()` のソース同一性確認を R6C 後の正しい Model / Renderer に対応させ、元の19ケース監査を改めて実行した。必須16件・追加3件の `CHECK=PASS`、Trust PASS、共通 Definition が適用可能な個別引用依存の残件0を確認した。限定 pytest は R6C 43 PASS、R6D の R6 再実行24 PASS。Git index と既存変更は保持された。全体 pytest は Phase 169 の末尾まで実行していない。

### Phase 169 との境界

以上は R10ET の対象範囲に限る検証であり、任意の $(n,k)$ の完成証明・全登録命題の数学的真理・過去の個別 Definition 登録削除を保証しない。Phase 169 全体の Closeout、対象範囲の回帰テスト選定、Git に登録する監査生成物の整理は後続の工程とする。長い自動生成ファイルを一括 `git add -A` で登録しない運用上の注意を維持する。
