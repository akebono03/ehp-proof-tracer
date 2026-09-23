# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の**現在有効なアーキテクチャ、意味論、不変条件、設計境界**を記録する。

過去の実装経緯は `docs/development_log.md`、証明記録は `docs/proof_records.md`、今後の計画は `docs/roadmap.md`、コード探索は `docs/code_reference.md` を参照する。

---

# 1. 基本設計原則

```text
実際の数学的・証明探索上の必要
↓
不足している最小表現
↓
必要な領域固有規則 / オーケストレーション
↓
既存の汎用基盤
```

次を混同しない。

```text
表現 != 型付け != 定理知識
構造的等値 != 数学的等値
探索計画 != 証明結果
表示層 != 証明事実
proof-scope 走査 != 定理探索
proof-scope relevance != executable relevance
applicability relevance != executable relevance
aggregate statement 内の別 branch occurrence != executable source relevance
既知関係の発見 != 写像評価
適用可能候補 != 証明成功
候補番号 != 数学的優先度
operation query != general evaluator
limited theorem-specific handoff != general query inference
theorem-specific membership handoff != general membership evaluator
group-generator containment != operation result
target group zero specialization != general zero-target evaluator
Web UI != 新しい数学エンジン
TeX rendering != 数学的 normalization
proof depth control != 新しい proof search
safe fallback != 推測した数学的説明
candidate selection != theorem ranking
Web execution != second execution engine
executable relevance filtering != theorem ranking
```

---

# 2. 現在の主要経路

## Toda group calculation

```text
ProofRepository
→ TodaGroupQuery
→ direct group lookup
→ 必要なら限定的 theorem-specific specialization
→ group result
→ proof / EHP provenance
→ structured presentation
→ report
```

## operation query

```text
query string
→ minimal parser
→ direct repository / proof-scope lookup
→ direct hit はそのまま返す
→ direct miss のうち許可された exact handoff のみ具体化
→ structured presentation
→ CLI / Web
```

現在許可される exact handoff:

```text
E(nu_5)
E(sigma_11)
E(nu_5 o eta_8)
E(nu_prime)
```

対応する user-facing result:

\[
E(\nu_5)=\nu_6,
\]

\[
E(\sigma_{11})=\sigma_{12},
\]

\[
E(\nu_5\eta_8)=0,
\]

\[
E\nu' \in \pi_7^4.
\]

`E(nu_prime)` だけは equality ではなく membership を返す。これは既存 Proposition 5.6 decomposition から直接読み取れる theorem-backed result を user-facing に具体化するためである。

## query-proof / generator show-proof

```text
selected existing fact / known-group identity
→ existing or theorem-specific specialized ProofStep
→ bounded ancestry
→ replay presentation
→ CLI / Web
```

depth は表示範囲であり、新しい proof search ではない。

## generator explore

```text
generator input
→ standard production repository
→ existing direct generator exploration
→ RepositoryGeneratorExplorationPresentation
→ CLI / Web
```

## generator explore-proof

```text
generator input
→ standard production repository
→ recursive proof scope
→ existing generator specialization
→ RepositoryProofScopeExplorationResult
→ CLI / Web
```

## generator explore-applicable

```text
generator input
→ existing applicability facade
→ RepositoryGeneratorApplicabilityExplorationResult
→ presentation
→ CLI / Web
```

## generator execute

```text
generator input
→ standard applicability exploration
→ qualified-family grouping
→ executable relevance guard
→ executable target resolution
→ NONE / AMBIGUOUS / EXECUTED
→ candidate number selection when required
→ existing qualified execution
→ executed ProofStep
→ structured presentation
→ CLI / Web
```

---

# 3. 主要 operation-query モジュール

```text
repository_operation_query.py
repository_operation_query_lookup.py
repository_operation_query_facade.py
repository_operation_query_presentation.py
repository_operation_query_proof_replay.py
repository_operation_query_proof_replay_presentation.py
repository_operation_query_proof_replay_statement_presentation.py
repository_operation_query_proof_replay_renderer.py
repository_nu5_stable_bridge_specialization.py
repository_sigma11_suspension_specialization.py
repository_nu5_eta8_suspension_zero_specialization.py
repository_nu_prime_suspension_membership_specialization.py
```

Phase 129 で `RepositoryOperationQueryMatchKind.GROUP_MEMBERSHIP` を追加した。

これは operation query の結果分類であり、direct lookup の探索範囲を広げるものではない。

---

# 4. 証明事実と provenance

証明事実の中心は

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

である。

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata である。

renderer、facade、CLI、Web adapter、表示 grouping、candidate selection form は独立した定理事実を追加しない。

```text
theorem-specific operation handoff
!= independent theorem root

theorem-specific membership step
!= general inference rule

GROUP_MEMBERSHIP match kind
!= membership evaluator
```

---

# 5. Repository 非破壊

Phase 113 の TodaGroupQuery specialization、Phase 114 の `E(nu_5)` handoff、Phase 115 の `E(sigma_11)` handoff、Phase 128 の `E(nu_5 o eta_8)` handoff、Phase 129 の `E(nu_prime)` handoff は元 repository に独立 root を追加しない。

Phase 129 の specialized membership step は query ごとに組み立てられる。

```text
before repository.entries()
==
after repository.entries()
```

を focused regression で固定する。

---

# 6. operation query の意味論

operation query は lookup-first である。

```text
operation query
→ direct existing-fact lookup
→ hit ならそのまま返す
→ miss なら exact handoff guard
→ 許可された場合だけ theorem-specific specialization
```

## `E(nu_5)`

\[
E(\nu_5)=\nu_6.
\]

既存 Proposition 5.6 stable-family bridge を具体化する。

## `E(sigma_11)`

\[
E(\sigma_{11})=\sigma_{12}.
\]

既存 \(\sigma\)-family definition を具体化する。

## `E(nu_5 o eta_8)`

\[
E(\nu_5\eta_8)=0.
\]

既存 Proposition 5.8 の \(\pi_{10}^6=0\) provenance を利用する。

## `E(nu_prime)`

Phase 129 で意味論を確定した。

既存 repository では

\[
E\nu'
\]

は

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}
\]

の第2 cyclic summand generator として保持されている。

この情報から自然に言える user-facing result は

\[
E\nu' \in \pi_7^4
\]

である。

次は採用しない。

\[
E(\nu')=E\nu'
\]

理由は、これは表記上の自己同一視であり、新しい theorem-backed operation information を表さないためである。

また、group relation 内に `Suspension(nu_prime)` が含まれているというだけで任意の containment を operation result にする一般規則も採用しない。

Phase 129 の handoff は exact query `E(nu_prime)` と Proposition 5.6 の特定 decomposition shape に限定する。

---

# 7. `E(nu_prime)` provenance shape

specialized root:

\[
E\nu' \in \pi_7^4.
\]

表現:

```text
HomotopyGroupMembershipStatement(
  element=Suspension(nu_prime),
  group_dimension=7,
  sphere_dimension=4,
)
```

直接 premise:

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}.
\]

この decomposition step 自体が Proposition 5.6 の既存 ancestry を保持する。

したがって、

```text
Depth 0:
E nu' in pi_7^4

Depth 1:
pi_7^4 = Z{nu_4} ⊕ Z/4{E nu'}
```

と再生できる。

---

# 8. `GROUP_MEMBERSHIP` の境界

Phase 129 では `RepositoryOperationQueryMatchKind` に

```text
GROUP_MEMBERSHIP
```

を追加した。

目的:

```text
operation query が membership statement を返した
```

ことを型として明示する。

これは次を意味しない。

```text
group relation 内部を一般再帰探索する
arbitrary element containment を membership に昇格する
任意の E(x) の target group を自動推定する
general membership evaluator を追加する
```

direct lookup の `_find_e_matches()` は従来どおり direct `MapApplication` / `Suspension` relation のみを見る。

---

# 9. parser の境界

Phase 129 は parser を変更していない。

現在の grammar boundary を維持する。

```text
二項 top-level composition
三項 top-level composition
E / H の generator operand
E / H の二項 composition operand
Delta の generator operand
```

未対応:

```text
四項以上
E(a o b o c)
H(a o b o c)
Delta(a o b o c)
Unicode ∘
一般再帰 parser
```

---

# 10. Web / CLI の共通 semantics

Web は CLI output / Markdown を再解析しない。

```text
existing structured object
→ thin Web adapter
→ presentation
```

Phase 129 の handoff は operation-query facade より下層にあるため、CLI と Web で別の数学 semantics を作らない。

---

# 11. Generator execution の意味論

既存 status:

```text
NONE
AMBIGUOUS
EXECUTED
```

Phase 126 以降、

```text
proof-scope relevance
applicability relevance
executable relevance
```

を区別する。

Phase 129 は execution semantics を変更していない。

---

# 12. Phase 129 regression boundary

focused:

```text
tests/test_phase129_nu_prime_operation_query_handoff.py
12 passed in 6.28s
```

関連 regression:

```text
tests/test_phase110_5_minimal_operation_query_core.py
tests/test_phase114_3_nu5_operation_query_handoff.py
tests/test_phase115_sigma11_operation_query_handoff.py
tests/test_phase118_web_operation_query.py
tests/test_phase128_nu5_eta8_operation_query_handoff.py

63 passed in 12.54s
```

manual CLI:

```text
python main.py query "E(nu_prime)"
→ E nu' in pi_7^4

python main.py query-proof "E(nu_prime)" --depth 1
→ specialized membership root
→ Proposition 5.6 pi_7^4 decomposition
```

repository-wide:

```text
python -m pytest -q
9268 passed in 569.71s (0:09:29)
```

---

# 13. Phase 129 完了境界

```text
E(nu_prime) result semantics = membership
exact theorem-specific guard
Proposition 5.6 provenance reuse
repository non-mutation
query-proof replay
direct lookup first
GROUP_MEMBERSHIP classification
existing handoffs preserved
parser unchanged
general E evaluator absent
general membership evaluator absent
recursive arbitrary containment absent
new independent theorem root absent
new qualified execution family absent
ranking absent
```

---

# 14. 次 Phase との境界

Phase 130 は新機能実装から始めず、current capability pressure の再監査から始める。

既存の deferred pressure:

```text
H(nu_5)
Delta(nu_prime)
H(sigma_11)
Delta(sigma_11)
```

これらは Phase 127 時点で element-level proof support が不足していると分類した。

Phase 130 ではまず現行 repository / proof support を再確認し、実利用上もっと優先すべき capability があるかを比較する。

---

# 15. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい theorem root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
containment を operation result と混同しない
membership handoff を general membership evaluator に拡張しない
CLI と Web の数学結果を分岐させない
proof-scope relevance と executable relevance を混同しない
candidate number を theorem priority と解釈しない
focused regression で境界を固定する
manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
