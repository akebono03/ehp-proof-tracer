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

Phase 108 final:

```text
8850 passed in 380.25s
```

## Phase 109–113

known-group identity、indexed \(\sigma_n\)、proof replay、operation query、CLI audit、symbolic specialization reuse を整備。

```text
Phase 109: 8998 passed in 493.70s
Phase 110: 9055 passed in 455.09s
Phase 113: 9081 passed in 434.58s
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

## Phase 115 `E(sigma_11)` handoff provenance

\[
E(\sigma_{11})=\sigma_{12}.
\]

```text
concrete definitional specialization
!= new theorem root
!= general E evaluator
```

## Phase 116–125 Web provenance boundary

```text
Web UI != proof truth
Web proof replay != new proof search
Web execution adapter != execution semantics
candidate selection form != theorem ranking
```

## Phase 126 executable relevance provenance boundary

```text
proof-scope relevance
!= applicability relevance
!= executable relevance
```

## Phase 127 capability pressure provenance audit

operation-query 残件を監査。

## Phase 128 `E(nu_5 o eta_8)=0` handoff provenance

\[
E(\nu_5\eta_8)=0.
\]

直接 premise:

\[
\pi_{10}^6=0.
\]

```text
theorem-specific specialized query fact
!= repository mutation
!= new independent theorem root
```

## Phase 129 `E(nu_prime)` membership handoff provenance

source fact:

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}.
\]

採用:

\[
E\nu' \in \pi_7^4.
\]

```text
membership specialized step
→ existing pi_7^4 decomposition
→ existing Proposition 5.6 ancestry
```

final:

```text
9268 passed in 569.71s (0:09:29)
```

Phase 129 完了。

---

# Phase 130 standard-query provenance

Phase 130 は新しい数学定理を増やすのではなく、既存証明を standard query から正しく利用できるようにする provenance orchestration を整備した。

## low-dimensional recovery

既存 proof ancestry から concrete group result を回収。

代表:

\[
\pi_3^2,\quad
\pi_4^3,\quad
\pi_4^2,\quad
\pi_5^3.
\]

```text
existing ProofStep reuse
!= new theorem fact
```

## stable family specialization

\[
\pi_{n+1}^n=\mathbb Z/2\{\eta_n\},
\]

\[
\pi_{n+2}^n=\mathbb Z/2\{\eta_n\eta_{n+1}\},
\]

\[
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\},
\]

\[
\pi_{n+4}^n=0,
\]

\[
\pi_{n+5}^n=0,
\]

\[
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\}.
\]

generic specialization は theorem の range guard を維持し、低次元 concrete branch を上書きしない。

## foundational query results

### diagonal

\[
\pi_n^n\cong\mathbb Z\{\iota_n\}.
\]

### circle

既存 Phase 56 symbolic result を再利用:

\[
\pi_{i-1}^1=0.
\]

### connectivity

\[
1\le n+k<n
\Rightarrow
\pi_{n+k}^n=0.
\]

### \(\pi_0\) boundary

\[
n+k=0
\]

は ordinary `TodaGroupResult` とせず、path component information として分離。

### negative dimension

\[
n+k<0
\]

は classical unstable domain 外として分離。

```text
negative stem accepted
!= negative homotopy group normalized to zero
```

## \(\pi_{16}^9\) concrete sigma provenance

Toda Proposition 5.15 ancestry には既に

\[
\pi_{16}^{9}
=
\mathbb Z/16\{\sigma_9\}
\]

の concrete `ProofStep` が存在する。

Phase 130-11 はこの node を standard query に接続した。

```text
n=9,k=7
→ standard.toda.prop515 proof scope
→ exact pi16_9 concrete node
→ normalized group result
```

generic indexed sigma specialization の境界は \(n\ge10\) のまま。

```text
pi16_9 concrete recovery
!= generic sigma specialization
!= new theorem root
```

## repository boundary

Phase 130 の specialization / concrete recovery は standard repository root を変更しない。

```text
standard.toda.prop56
standard.toda.prop58
standard.toda.prop511
standard.toda.prop515
```

を維持。

## regression boundary

```text
python -m pytest tests -q
9308 passed in 577.02s (0:09:37)
```

Phase 130 完了。

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
stable group specialization != unrestricted AST substitution
concrete proof recovery != new theorem root
negative stem acceptance != negative homotopy-group theorem
pi_0 boundary information != ordinary group result
Web execution adapter != execution semantics
proof-scope relevance != executable relevance
applicability relevance != executable relevance
aggregate statement の同居 != executable source relevance
executable relevance filtering != theorem ranking
```

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。
