<!-- PHASE168_FINAL_CLOSURE_20261025 -->

## Phase 168 — 現行共通 Narrative と信頼境界の確定（2026-10-25）

### 実装済みの公開経路

現在の標準的な群の完全証明は、以下の単一の責務分担で生成する。

```text
型付き Goal（登録済み証明対象）と文献掲載順
    ↓
Backward Search（逆向き証明探索）
    ↓
Proof Tree（採用された ProofStep と依存関係）
    ↓
Proof Tree verification（完全証明の検証境界）
    ↓
Proof Narrative Model（実際に使用した証明・引用の射影）
    ↓
共通 Renderer（本文・Reference・Citation の出力）
    ↓
標準 Web 表示
```

- 標準 Web 入口：`web_group_proof.py::build_standard_web_group_proof_view()`。
- 完全証明の検証境界：`phase168_r3_41p13_trust_boundary/verification.py::verify_proof_tree_for_narrative()`。R3-41P19 では、完全証明の対象群と結論の一致を検査する条件を追加した。
- Model 接続：`phase168_r3_4_link_bridge.py::build_linked_proof_narrative_model()` と `phase168_r3_3_proof_narrative_model.py`。
- 共通文章・文献表示：`phase168_r3_5_model_renderer.py::render_model_backed_narrative_markdown()` と Reference projection（参照本文射影）。

完全証明の検証では、GIVEN（既出の固定命題）の選別済み出典・掲載順と、INFERENCE（推論）の既存規則・祖先を点検する。引用対象の命題識別子は登録 Goal から解決し、後続命題・自己参照を引用可能な証拠として扱わない。旧「使用順」制限を再導入せず、`publication_position` と必要な `component_position` に基づく文献順を用いる。未解決の結果は partial として表示し、完成へ昇格させない。

### Origin Observation の制約と保持する防御

R3-41P17 で `proof_origin_capture.py` に Factory 出力と探索で採用された ProofStep のオブジェクト同一性を観測する機能を追加した。しかし R3-41P18 は、外部から記録を自己申告して偽の INFERENCE を受け入れさせ得ること、複数探索が同一 Observation に集約され得ること、実験的 handoff では別の Bridge wrapper や不整合な target を受け入れ得ることを確認した。**Observation は数学的な証明書ではない。**

R3-41P19 で対象群の検証を加えたのは標準の検証関数である。実験的な origin handoff に残る境界問題まで解決したとは主張しない。標準 Web の matcher を使った検証は維持する。任意の利用者定義 `InferenceRule`、外部供給 `RegistryBridgeResult`、出典文献そのものの数学的真実性について一般認証したという意味でもない。

Renderer / Typed Projection に残る `_stable_eta_renaming_shape()` と `prop42_exactness_indices()` による数学的な形状検査2箇所は、直接渡された未検証 Model の不正な表示を拒否する互換性防御として維持する。証明を新規生成する責務を Renderer へ移すこととは区別する。これらを撤去する場合は、全ての呼び出し元に対する真正性保証を先に成立させる必要がある。

### Reference と代表群の不変条件

- $\pi_3^2=\mathbb Z\{\eta_2\}$：INFERENCE 13、GIVEN 5、計18 ProofStep。
- $\pi_4^3=\mathbb Z/2\{\eta_3\}$：INFERENCE 19、GIVEN 6、計25 ProofStep。
- $\pi_5^4=\mathbb Z/2\{\eta_4\}$：INFERENCE 7、GIVEN 3、計10 ProofStep。

$\pi_5^4$ は、Proposition 5.1 に登録された $\pi_4^3$ の**群構造**と Toda (4.5) の $(n,m,k)=(3,4,1)$ への適用を使用する。$\pi_4^3$ の完成証明木そのものを再帰的に再利用・再表示する必要はない。生成元は $E(\eta_3)=\eta_4$ として扱う。

上記3群について証明本文・Reference・Citation は固定基準と全文一致し、GIVEN 14件の文献順が PASS した。Phase 168 最終限定 pytest は **86 PASS**、現行 `tests/` および Phase 168 関連回帰を対象とする終了テストは **3546 PASS、FAIL 0、ERROR 0**。歴史的な退避テストを含む無制限の repository-wide pytest や、未監査の全群についての証明成立を主張しない。

### Phase 境界

Phase 168 の正式な完了対象は、標準公開経路の Proof Tree / Reference / Narrative の整合性、数学的な防御の維持、上記最終回帰である。2-stem の全群の証明完成は本 Phase の完了条件として認定しない。次工程は残存する partial 群の型付き導出・出典資格の確認から始め、旧方式の個別 Renderer や固定文章を復活させない。
