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

利用者向け workflow:

```text
生成元入力
→ 実行可能対象の解決
→ 曖昧性に安全な候補選択
→ qualified execution
→ 実行済み goal_step
→ 結果 + 証明
```

Phase 108 final:

```text
8850 passed in 380.25s
```

## Phase 109

known-group identity / indexed \(\sigma_n\) / proof replay を整備。

```text
show-proof != execute
```

final:

```text
8998 passed in 493.70s
```

## Phase 110

operation query / query-proof。

```text
検索 != 推論 != evaluator
deduplicated 表示 != provenance deletion
query-proof replay != enclosing theorem replay
```

final:

```text
9055 passed in 455.09s
```

## Phase 111–113

CLI capability audit、operation/workflow pressure audit、symbolic \(\sigma_n\) specialization reuse。

Phase 113 final:

```text
9081 passed in 434.58s
```

## Phase 114 `E(nu_5)` handoff provenance

\[
E(\nu_5)=\nu_6.
\]

```text
concrete specialization
!= new theorem root
!= general E evaluator
```

final:

```text
9097 passed in 449.47s
```

## Phase 115 `E(sigma_11)` handoff provenance

\[
E(\sigma_{11})=\sigma_{12}.
\]

```text
concrete definitional specialization
!= new theorem root
!= general E(sigma_n) evaluator
!= general E evaluator
```

final:

```text
9111 passed in 432.54s
```

## Phase 116–125 Web provenance boundary

Web UI は既存 structured result / presentation / `ProofStep` ancestry を表示する layer である。

```text
Web UI != proof truth
Web proof replay != new proof search
Web execution adapter != execution semantics
candidate selection form != theorem ranking
```

Phase 125 final:

```text
9243 passed in 555.37s
```

## Phase 126 executable relevance provenance boundary

```text
proof-scope relevance
!= applicability relevance
!= executable relevance
```

aggregate Proposition 5.6 内の別 branch occurrence を executable source relevance とみなさないよう修正。

結果:

```text
nu_prime → 2 executable targets
nu_5 → NONE
sigma_11 → NONE
```

final:

```text
9246 passed in 556.62s
```

## Phase 127 capability pressure provenance audit

監査対象:

```text
H(nu_5)
H(sigma_11)
Delta(sigma_11)
E(nu_prime)
Delta(nu_prime)
E(nu_5 o eta_8)
```

`E(nu_prime)` は既存 Proposition 5.6 decomposition に \(E\nu'\) の provenance があるが、user-facing result semantics は未確定として KEEP。

`E(nu_5 o eta_8)` は result semantics が明確なため Phase 128 へ送った。

## Phase 128 `E(nu_5 o eta_8)=0` handoff provenance

query:

```text
E(nu_5 o eta_8)
```

specialized conclusion:

\[
E(\nu_5\eta_8)=0.
\]

直接 premise:

\[
\pi_{10}^6=0.
\]

その ancestry:

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

```text
theorem-specific specialized query fact
!= repository mutation
!= new independent theorem root
```

final:

```text
9256 passed in 570.10s (0:09:30)
```

## Phase 129 `E(nu_prime)` membership handoff provenance

Phase 129 は新しい独立 theorem root を repository に登録していない。

### source fact

既存 Toda Proposition 5.6:

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}.
\]

この relation では \(E\nu'\) が order-four cyclic summand の generator として保持される。

### semantics audit

`E(nu_prime)` の候補を比較した。

```text
E(nu') = E nu'
E nu' in pi_7^4
pi_7^4 decomposition
```

採用:

\[
E\nu' \in \pi_7^4.
\]

理由:

```text
membership は既存 group decomposition から theorem-backed に言える
自己同一的 equality を作らない
decomposition 全体を query result に置き換えない
```

### specialized ProofStep

Depth 0:

\[
E\nu' \in \pi_7^4.
\]

Depth 1:

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}.
\]

specialized root は `ProofRule.INFERENCE`。

直接 premise は既存 Proposition 5.6 decomposition `ProofStep`。

したがって provenance は

```text
membership specialized step
→ existing pi_7^4 decomposition
→ existing Proposition 5.6 ancestry
```

となる。

### representation

user-facing membership は既存

```text
HomotopyGroupMembershipStatement
```

を再利用する。

```text
element = Suspension(nu_prime)
group_dimension = 7
sphere_dimension = 4
```

### match kind

Phase 129 で

```text
RepositoryOperationQueryMatchKind.GROUP_MEMBERSHIP
```

を追加。

これは presentation / result classification であり、

```text
general membership evaluator
arbitrary containment search
general E evaluator
```

ではない。

### direct lookup boundary

`query_repository_operation()` の direct `E` lookup は従来どおり、

```text
Relation.lhs が MapApplication(E, ...)
Relation.lhs が Suspension(...)
```

の direct operation relation のみを対象とする。

Proposition 5.6 group structure 内部を recursive containment で operation result に昇格させる変更は行っていない。

### repository boundary

handoff は query ごとに specialized `ProofStep` を作る。

```text
before repository.entries()
==
after repository.entries()
```

を focused test で固定。

### regression

focused:

```text
12 passed in 6.28s
```

関連 regression:

```text
63 passed in 12.54s
```

manual query:

\[
E\nu' \in \pi_7^4.
\]

manual query-proof:

```text
Depth 0:
E nu' in pi_7^4

Depth 1:
pi_7^4 = Z{nu_4} ⊕ Z/4{E nu'}
```

final:

```text
9268 passed in 569.71s (0:09:29)
```

Phase 129 完了。

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
候補番号 != theorem priority
known-group 証明再生 != theorem application execution
show-proof != execute
operation-query 検索 != evaluator
operation-query 結果 != 新しい独立 theorem root
query-proof replay != enclosing theorem replay
LOOKUP_MISS != evaluator required
limited operation handoff != general query inference
theorem-specific concrete specialization != general evaluator
target-zero theorem-specific specialization != general target-zero evaluator
theorem-specific membership handoff != general membership evaluator
GROUP_MEMBERSHIP != recursive containment semantics
Web execution adapter != execution semantics
proof-scope relevance != executable relevance
applicability relevance != executable relevance
aggregate statement の同居 != executable source relevance
executable relevance filtering != theorem ranking
```

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。
