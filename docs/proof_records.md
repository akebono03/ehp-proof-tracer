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

## 安定 stem $G_0$ から $G_7$

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

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
$$

## Phase 103

`docs/proof_records/applicable_theorem_relevance_103.md`

```text
適用候補 != 証明成功
関連度カテゴリ != 定理事実
表示順 != 定理順位付け
```

## Phase 104

選択候補を READY 検証、明示的 final rule による有界探索、事前構築済み report の実行へ接続。

```text
8644 passed in 374.63s
```

## Phase 105

最初の標準 qualified family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

```text
8709 passed in 659.02s
```

## Phase 106

`docs/proof_records/performance_applicability_106.md`

```text
797573 全 scope 候補
→ 176616 生成元関連候補

8.16 s / 62.42 MiB
8712 passed in 337.86s
```

## Phase 107 multi-family qualified execution provenance

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

第2 family は既存の

$$
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
$$

を導く2前提 production rule である。

複数前提候補から companion premise を任意探索せず、同じ root / rule / goal / source identity を満たす既存 production application を一意に recovery する。

```text
8783 passed in 290.63s
```

Phase 107 は完了。

## Phase 108 利用者向け実行 provenance

新しい数学的定理事実は追加していない。

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

```text
8850 passed in 380.25s
```

Phase 108 は完了。

## Phase 109 既知群同一性 / 証明再生 provenance

新しい独立した数学的定理 root は追加していない。

Toda Proposition 5.15:

$$
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
$$

具体 integer index $n\ge 10$ に対して定理固有の具体化を導入。

例:

$$
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\},
\qquad
\pi_{19}^{12}=\mathbb Z/16\{\sigma_{12}\}.
$$

```text
concrete specialization
→ symbolic Proposition 5.15 higher step
```

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

Phase 109 は完了。

## Phase 110 operation query / 証明再生 provenance

Phase 110 は新しい数学的定理事実を追加していない。

既存 repository / proof-scope に存在する relation・map statement・composition を利用者向け query から検索し、既存 `ProofStep` provenance を保持したまま表示・replay する経路を追加した。

```text
検索 != 推論 != evaluator
deduplicated 表示 != provenance deletion
query-proof replay != enclosing theorem replay
```

```text
9055 passed in 455.09s (0:07:35)
```

Phase 110 は完了。

## Phase 111 CLI capability / user pressure audit

Phase 111 は新しい数学的定理事実を追加していない。

```text
3-term query != new theorem
--depth != new proof search
safe type-name fallback != 推測した定理 branch
```

```text
9074 passed in 446.27s (0:07:26)
```

Phase 111 は完了。

## Phase 112 operation / workflow capability audit

Phase 112 は新しい数学的定理事実を追加していない。

```text
LOOKUP_MISS != evaluator required
```

既存 capability の未接続箇所を優先する方針を確定した。

## Phase 113 TodaGroupQuery / $\sigma_n$ specialization provenance

Phase 113 は新しい数学的定理 root を追加していない。

既存 symbolic Proposition 5.15:

$$
\pi_{n+7}^{n}
=
\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9
$$

から、既存 theorem-specific concrete specialization を `TodaGroupQuery` 経路で再利用する。

```text
9081 passed in 434.58s (0:07:14)
```

Phase 113 は完了。

## Phase 114 `E(nu_5)` existing-inference handoff provenance

既存 Toda Proposition 5.6:

$$
E^{n-5}\nu_5=\nu_n,
\qquad n\ge 6
$$

を再利用して、

$$
E(\nu_5)=\nu_6
$$

を exact handoff として接続した。

```text
concrete specialization
!= new theorem root
!= general E evaluator
```

```text
9097 passed in 449.47s (0:07:29)
```

Phase 114 は完了。

## Phase 115 `E(sigma_11)` existing-mathematics handoff provenance

既存 Toda Lemma 5.14:

$$
\sigma_n=E^{n-8}\sigma_8,
\qquad n\ge 8
$$

を再利用して、

$$
E(\sigma_{11})=\sigma_{12}
$$

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

Phase 115 は完了。

## Phase 116–122 Web presentation / exploration provenance boundary

Phase 116–122 は新しい数学的定理事実を追加していない。

Web UI は既存 structured result / presentation / `ProofStep` ancestry を表示する layer である。

```text
Web UI != proof truth
Web proof replay != new proof search
direct Web explore != recursive proof-scope explore
safe fallback != inferred theorem statement
```

Phase 122 final regression:

```text
9212 passed in 455.16s (0:07:35)
```

## Phase 123 applicability Web presentation provenance boundary

Phase 123 は新しい数学的 theorem root、`ProofStep`、proof-search rule、qualified execution family を追加していない。

既存 applicability infrastructure:

```text
RepositoryGeneratorApplicabilityExplorationResult
RepositoryGeneratorApplicabilityPresentation
ApplicabilitySourceGroupPresentation
ApplicabilityRuleFamilyPresentation
```

を read-only Web view に射影した。

重要な境界:

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

collapsed details
!= provenance removal
```

`nu_prime` の underlying result:

```text
626 proof-scope occurrences
176616 applicability candidates
542 source statements with candidates
123300 rule groups
29308 rule families
```

Web は summary counts を保持したまま、browser 描画量だけを

```text
source:
各 category 最大 5

rule family:
各 displayed source 最大 10
```

へ制限する。

`sigma_11`:

```text
1 proof-scope occurrence
686 applicability candidates
1 source statement
472 rule groups
112 rule families
```

既存 known-group statement

$$
\pi_{18}^{11}
=
\mathbb Z/16\{\sigma_{11}\}
$$

が source として表示されるが、Phase 123 がこの数学的 statement を新しく証明したわけではない。

`eta_999`:

```text
0 / 0 / 0 / 0 / 0
```

は normal zero applicability result である。

Phase 123 focused:

```text
13 passed in 61.24s
17 passed in 69.57s
```

Phase 123 final regression:

```text
9229 passed in 509.16s (0:08:29)
```

Phase 123 は presentation / read-only exploration の Phase であり、proof truth は既存 repository と `ProofStep` provenance に残る。

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
引き渡し検証 != 定理事実
有界探索 report != 実行済み証明
qualified 候補 != 一意な実行対象
production-application recovery != 新しい定理事実
family dispatch != 定理順位付け
性能最適化 != 定理事実
user-facing resolver != 定理順位付け
候補番号 != theorem priority
CLI 表示 != 新しい定理事実
既知群同一性 lookup != qualified execution
symbolic 具体化 != 任意の AST 書き換え
known-group 証明再生 != theorem application execution
show-proof != execute
operation-query 検索 != evaluator
operation-query 結果 != 新しい定理事実
deduplicated 表示 != provenance deletion
表示順 != 定理順位付け
query-proof fact number != theorem priority
query-proof replay != enclosing theorem replay
--depth != new proof search
three-term query != composition evaluator
safe type-name fallback != 推測した定理 branch
LOOKUP_MISS != evaluator required
TodaGroupQuery specialization reuse != new theorem
limited operation handoff != general query inference
theorem-specific concrete specialization != general evaluator
expression occurrence != operation result relation
related mathematics exists != reusable operation bridge
Web applicability view != proof truth
Web source truncation != source-result deletion
Web rule-family truncation != candidate deletion
explore-applicable != execute
```

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。
