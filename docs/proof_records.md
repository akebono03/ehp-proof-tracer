# EHP Proof Tracer — 証明記録

この文書は、代表的な数学的証明および証明基盤の記録索引である。

詳細な過去記録は内容を削除せず `docs/proof_records/` 以下へ保存する。

現在の設計は `docs/design.md`、開発履歴は `docs/development_log.md`、今後の計画は `docs/roadmap.md` を参照する。

---

# 数学的証明記録

## 初期記録 / Toda 式 (5.8)

`docs/proof_records/early_records_and_toda_5_8.md`

## Toda Lemma 5.7 から Lemma 5.10

`docs/proof_records/toda_5_7_to_5_10.md`

## Toda Proposition 5.11 から Lemma 5.16

`docs/proof_records/toda_5_11_to_5_16.md`

## 安定 stem \(G_0\) から \(G_7\)

`docs/proof_records/stable_stems_g0_g7.md`

---

# 証明基盤の記録

## Phase 79–89

`docs/proof_records/proof_infrastructure_079_089.md`

証明 Repository、repository 支援推論、自動規則選択、有界 producer 探索、診断、depth パラメータ化、有限 retry、具体的定理 instance filtering の記録。

## Phase 90–101

Toda 群問い合わせ、群正規化、EHP / 証明 provenance、表示 / レポート、標準運用 repository、CLI、生成元探索の記録。

## Phase 102

`docs/proof_records/production_proof_scope_exploration_102.md`

代表結果:

\[
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
\]

## Phase 103

`docs/proof_records/applicable_theorem_relevance_103.md`

```text
適用候補 != 証明成功
関連度カテゴリ != 定理事実
表示順 != 定理順位付け
```

## Phase 104–108 qualified execution provenance

Phase 104–108 は applicability candidate から安全な qualified execution と user-facing execute workflow までを構築した。

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

第2 family は既存の

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
\]

を導く2前提 production rule である。

複数前提候補から companion premise を任意探索せず、同じ root / rule / goal / source identity を満たす既存 production application を一意に recovery する。

利用者向け workflow:

```text
生成元入力
→ 実行可能対象の解決
→ 曖昧性に安全な候補選択
→ qualified execution
→ 実行済み goal_step
→ 結果 + 証明
```

```text
候補番号 != 定理順位付け
```

Phase 108 final:

```text
8850 passed in 380.25s
```

## Phase 109 既知群同一性 / 証明再生 provenance

新しい独立した数学的定理 root は追加していない。

Toda Proposition 5.15:

\[
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
\]

known-group proof replay:

```text
generator
→ unique 既知群同一性 node
→ existing ProofStep
→ bounded ancestry
→ 表示
```

```text
show-proof != execute
```

```text
8998 passed in 493.70s (0:08:13)
```

## Phase 110 operation query / 証明再生 provenance

Phase 110 は新しい数学的定理事実を追加していない。

```text
検索 != 推論 != evaluator
deduplicated 表示 != provenance deletion
query-proof replay != enclosing theorem replay
```

```text
9055 passed in 455.09s (0:07:35)
```

## Phase 111 CLI capability / user pressure audit

```text
3-term query != new theorem
--depth != new proof search
safe type-name fallback != 推測した定理 branch
```

```text
9074 passed in 446.27s (0:07:26)
```

## Phase 112 operation / workflow capability audit

```text
LOOKUP_MISS != evaluator required
```

既存 capability の未接続箇所を優先する方針を確定した。

## Phase 113 TodaGroupQuery / \(\sigma_n\) specialization provenance

既存 symbolic Proposition 5.15 の theorem-specific concrete specialization を `TodaGroupQuery` 経路で再利用。

```text
9081 passed in 434.58s (0:07:14)
```

## Phase 114 `E(nu_5)` existing-inference handoff provenance

既存 Toda Proposition 5.6 を再利用して、

\[
E(\nu_5)=\nu_6
\]

を exact handoff として接続した。

```text
concrete specialization
!= new theorem root
!= general E evaluator
```

```text
9097 passed in 449.47s (0:07:29)
```

## Phase 115 `E(sigma_11)` existing-mathematics handoff provenance

既存 Toda Lemma 5.14 を再利用して、

\[
E(\sigma_{11})=\sigma_{12}
\]

を exact handoff として接続した。

```text
concrete definitional specialization
!= new theorem root
!= general E(sigma_n) evaluator
!= general E evaluator
```

```text
9111 passed in 432.54s (0:07:12)
```

## Phase 116–122 Web presentation / exploration provenance boundary

Phase 116–122 は新しい数学的定理事実を追加していない。

Web UI は既存 structured result / presentation / `ProofStep` ancestry を表示する layer である。

```text
Web UI != proof truth
Web proof replay != new proof search
direct Web explore != recursive proof-scope explore
safe fallback != inferred theorem statement
```

Phase 122 final:

```text
9212 passed in 455.16s (0:07:35)
```

## Phase 123 applicability Web presentation provenance boundary

Phase 123 は新しい mathematical theorem root、`ProofStep`、proof-search rule、qualified execution family を追加していない。

既存 applicability infrastructure を read-only Web view に射影した。

```text
applicability candidate
!= proof
!= theorem ranking
!= selected theorem application
!= qualified execution
!= executed result

Web source limit
!= source-result deletion

Web rule-family limit
!= applicability-candidate deletion
```

`nu_prime` underlying result:

```text
626 proof-scope occurrences
176616 applicability candidates
542 source statements with candidates
123300 rule groups
29308 rule families
```

Phase 123 final:

```text
9229 passed in 509.16s (0:08:29)
```

## Phase 124 Web workflow organization provenance boundary

Phase 124 は新しい theorem root、`ProofStep`、proof-search rule、qualified execution family、candidate-selection semantics、execution semantics を追加していない。

```text
Workflow navigation
→ existing section anchor

anchor link
!= proof edge
!= theorem application
!= candidate selection
!= qualified execution
```

Phase 124 final:

```text
9234 passed in 522.10s (0:08:42)
```

## Phase 125 Web qualified-execution presentation provenance boundary

Phase 125 は新しい数学的 theorem root、`ProofStep`、proof-search rule、qualified execution family、operation-query grammar、candidate-ranking semantics を追加していない。

既存 user execution workflow:

```text
generator input
→ executable target resolution
→ NONE / AMBIGUOUS / EXECUTED
→ explicit candidate selection when required
→ qualified execution
→ executed goal_step
→ RepositoryGeneratorUserExecutionPresentation
```

を Web UI へ接続した。

重要な境界:

```text
Web execution adapter
!= proof engine
!= resolver
!= qualified execution engine
!= theorem ranking

candidate number
!= theorem priority

AMBIGUOUS
!= permission to auto-select

NONE
!= mathematical impossibility

Web Result + Proof
!= new proof
```

### `nu_prime`

Web / CLI の executable candidates:

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\},
\]

\[
\Delta(\iota_9)=\pm(2\nu_4-E\nu').
\]

candidate 1 / 2 は既存 workflow の 1-based addressing であり、数学的優先順位を意味しない。

### `eta_999`

```text
No executable target found for this generator.
```

は `NONE` の正常表示であり、

```text
数学的に何も言えない
```

ことを意味しない。

### `nu_5`

Phase 125 manual audit では Web execution が

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
\]

を返した。

CLI:

```text
python main.py execute nu_5
```

も同じ結果を返した。

したがってこの挙動は Phase 125 Web adapter が新しく作った定理関係ではなく、既存 executable-target resolution の結果である。

```text
Web result == CLI result
```

を確認したため Phase 125 の接続境界としては PASS。

利用者 expectation と resolver semantics の整合性は Phase 126 の監査対象とした。

Phase 125 focused:

```text
14 passed in 29.80s
```

Phase 125 final regression:

```text
9243 passed in 555.37s (0:09:15)
```

Phase 125 の proof truth は従来どおり既存 repository と実際の executed `ProofStep` provenance に残る。

## Phase 126 executable relevance provenance boundary

Phase 126 は新しい数学的 theorem root、`ProofStep`、proof-search rule、qualified execution family を追加していない。

Phase 125 で観測した

```text
nu_5
→ pi6_2
```

の executable path を監査した。

原因は Toda Proposition 5.6 aggregate の broad source relevance だった。

同一 aggregate には、

\[
\pi_6^3=\mathbb Z/4\{\nu'\},
\]

\[
\pi_7^4=\mathbb Z\{\nu_4\}\oplus\mathbb Z/4\{E\nu'\},
\]

\[
\pi_8^5=\mathbb Z/8\{\nu_5\}
\]

などが含まれる。

旧 resolver では、

```text
nu_5 が pi8_5_group_relation に出現
→ Prop.5.6 ProofStep 全体が generator relevant
→ 第2 qualified family が同じ ProofStep の pi6_3_group_relation を利用
→ pi6_2 executable target
```

となっていた。

Phase 126 では次を区別した。

```text
proof-scope relevance
!= applicability relevance
!= executable relevance
```

executable relevance は、

```text
queried generator occurrence
→ actual source component used by qualified family
```

の対応を要求する。

現在の第2 qualified family

```text
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

について、

```text
pi6_3_group_relation
```

内の occurrence だけを executable source relevance とする最小 guard を追加した。

結果:

### `nu_prime`

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\},
\]

\[
\Delta(\iota_9)=\pm(2\nu_4-E\nu')
\]

の2 executable targets を維持。

### `nu_5`

```text
No executable target found for nu_5.
```

`pi8_5_group_relation` に occurrence は存在するため proof-scope / applicability relevance 自体は維持されるが、第2 family の executable relevance は満たさない。

### `sigma_11`

```text
No executable target found for sigma_11.
```

admitted qualified family がないため既存 `NONE` を維持。

重要な境界:

```text
aggregate statement の同居
!= executable source relevance

executable relevance filtering
!= theorem ranking

executable target exclusion
!= mathematical impossibility

proof-scope applicability result
!= executable target set
```

focused regression:

```text
13 passed in 14.86s
```

Phase 126 final regression:

```text
9246 passed in 556.62s (0:09:16)
```

## Phase 127 capability pressure provenance audit

Phase 127 は新しい数学的 theorem root、`ProofStep`、proof-search rule、query grammar を追加せず、既存 repository の provenance を監査した。

監査対象:

```text
H(nu_5)
H(sigma_11)
Delta(sigma_11)
E(nu_prime)
Delta(nu_prime)
E(nu_5 o eta_8)
```

### `H(nu_5)`

Phase 68 の `TodaHopfInvariantZeroStatement` は \(\pi_9^5\) を source とする。

したがってその provenance は \(\nu_5\eta_8\) 側の Hopf-zero machinery であり、`H(nu_5)` の element-level proof ではない。

```text
H(nu_5)
→ existing element-level proof absent
→ DEFER
```

### `E(nu_prime)`

\[
E\nu'
\]

は既存の

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}
\]

の generator として存在し、Phase 66 の

\[
\Delta(\iota_9)=\pm(2\nu_4-E\nu')
\]

でも同じ suspension expression が再利用される。

ただし `E(nu_prime)` の user-facing operation result の形は別途意味論監査が必要。

```text
E(nu_prime)
→ provenance exists
→ result semantics unresolved
→ KEEP
```

### `Delta(nu_prime)`

既存 Delta facts の値側に \(\nu'\) が現れることと、\(\nu'\) 自身を Delta 入力にすることは別である。

```text
Delta(nu_prime)
→ element-level Delta proof absent
→ DEFER
```

### `H(sigma_11)` / `Delta(sigma_11)`

\(\sigma_8\) の Hopf relation および \(\sigma\)-chain の Delta machinery は存在するが、`sigma_11` を入力とする element-level relation はない。

```text
H(sigma_11)
Delta(sigma_11)
→ DEFER
```

### `E(nu_5 o eta_8)`

既存 Proposition 5.8 provenance:

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\]

\[
\pi_{10}^6=0.
\]

result semantics は

\[
E(\nu_5\eta_8)=0
\]

と明確。

Phase 127-4 で Phase 128 の対象に選定。

## Phase 128 `E(nu_5 o eta_8)=0` handoff provenance

Phase 128 は新しい独立 theorem root を repository に登録していない。

query:

```text
E(nu_5 o eta_8)
```

に対して direct lookup を先に実行する。

direct miss の場合だけ exact handoff guard が作動する。

specialized conclusion:

\[
E(\nu_5\eta_8)=0.
\]

コード上の relation shape:

```text
Relation
lhs = Suspension(Composition(nu_5, eta_8))
rhs = Zero()
relation_type = ZERO
```

これは既存 `E(eta_2 o nu_prime)=0` と同じ operation-query zero-relation 表現を再利用する。

### provenance root

handoff は

```text
standard.toda.prop58
```

の proof-scope に限定する。

これは同じ Prop.5.8 ancestry が後続 theorem root の proof-scope にも現れ、同一 specialized conclusion が重複生成されることを防ぐためである。

```text
root restriction
!= theorem ranking
```

### specialized ProofStep ancestry

Depth 0:

\[
E(\nu_5\eta_8)=0.
\]

Depth 1:

\[
\pi_{10}^6=0.
\]

Depth 2:

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\]

\[
E:\pi_9^5\to\pi_{10}^6
\text{ is surjective},
\]

\[
\nu_6\eta_9=0.
\]

`pi_10^6=0` は `ProofRule.INFERENCE` であり、`pi_9^5` relation を直接 premise として持つことを handoff guard が確認する。

したがって、

```text
target group is zero
```

という表面的条件だけで arbitrary element の suspension-zero fact を生成していない。

### repository boundary

handoff は query ごとに specialized `ProofStep` を組み立てる。

```text
before repository.entries()
==
after repository.entries()
```

を focused test で固定。

```text
theorem-specific specialized query fact
!= repository mutation
!= new independent theorem root
```

### regression

focused:

```text
40 passed in 15.43s
```

manual query:

\[
E(\nu_5\eta_8)=0.
\]

manual query-proof で Toda Proposition 5.8, Phase 68 の provenance を確認。

final:

```text
9256 passed in 570.10s (0:09:30)
```

---

# 記録原則

数学的な根拠は `ProofStep` と、その実際の premise ancestry である。

```text
証明記録 != 証明事実
表示 != proof truth
production repository の組み立て != 定理事実
探索結果 != 新しい定理事実
proof-scope 走査 != 定理探索
適用候補 != 成功した証明
関連度カテゴリ != 定理事実
candidate ordering != 定理順位付け
候補番号 != theorem priority
qualified 候補 != 一意な実行対象
production-application recovery != 新しい定理事実
family dispatch != 定理順位付け
性能最適化 != 定理事実
known-group 証明再生 != theorem application execution
show-proof != execute
operation-query 検索 != evaluator
operation-query 結果 != 新しい独立 theorem root
deduplicated 表示 != provenance deletion
query-proof replay != enclosing theorem replay
--depth != new proof search
safe type-name fallback != 推測した定理 branch
LOOKUP_MISS != evaluator required
TodaGroupQuery specialization reuse != new theorem
limited operation handoff != general query inference
theorem-specific concrete specialization != general evaluator
target-zero theorem-specific specialization != general target-zero evaluator
Web applicability view != proof truth
Web source truncation != source-result deletion
Web rule-family truncation != candidate deletion
Workflow navigation != proof structure
navigation order != theorem ranking
section anchor != proof reference
UI organization != new capability
explore-applicable != execute
Web execution adapter != execution semantics
Web execution result != new theorem
candidate selection form != theorem ranking
CLI/Web consistency != semantic correctness proof
proof-scope relevance != executable relevance
applicability relevance != executable relevance
aggregate statement の同居 != executable source relevance
executable relevance filtering != theorem ranking
```

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。
