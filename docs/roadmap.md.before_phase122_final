# EHP Proof Tracer ロードマップ

この文書は**今後の機能依存関係と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

標準 group query:

```text
n,k
→ standard production repository
→ TodaGroupQuery
→ direct known-group lookup
→ 必要なら theorem-specific specialization
→ structured presentation
→ report
```

現在の Web UI:

```text
group query
operation query
query-proof
generator show-proof
generator explore
```

generator explore:

```text
generator input
→ thin Web generator-exploration adapter
→ existing standard repository exploration
→ existing structured exploration presentation
→ grouping + metadata + LaTeX
→ KaTeX
```

現在利用できる限定 handoff:

\[
E(\nu_5)=\nu_6,
\]

\[
E(\sigma_{11})=\sigma_{12}.
\]

基本境界:

```text
direct lookup first
limited theorem-specific handoff != general query inference
query != general evaluator
LOOKUP_MISS != evaluator required
Web UI != new mathematical engine
depth control != new proof search
show-proof != execute
explore != explore-proof
explore != execute
```

---

# 2. 完了済み機能

Phase 90–111:

```text
Toda group query / normalization
EHP / proof provenance
reporting
generator exploration
recursive proof scope
applicability discovery
qualified execution
known-group identity
indexed sigma specialization
show-proof
operation query / query-proof
3-term top-level composition query
replay --depth
```

Phase 112–115:

```text
real workflow pressure audit
symbolic sigma_n → TodaGroupQuery integration
E(nu_5)=nu_6 existing-proof handoff
E(sigma_11)=sigma_12 existing-proof handoff
```

Phase 116–117:

```text
Web readiness audit
Flask / KaTeX selection
minimal group-query Web UI
Web / CLI result regression
browser smoke
```

Phase 118:

```text
operation-query Web boundary audit
operation-query Web UI
explicit fact selection + query-proof Web
depth 0 / 1 / 2 + safe fallback + browser audit
```

Phase 119–120:

```text
next Web capability pressure audit
show-proof selected
generator show-proof Web integration
depth 0 / 1 / 2
safe unsupported-statement fallback
browser/manual integration
```

Phase 121:

```text
remaining read-only Web capability audit
explore selected ahead of explore-proof / explore-applicable
web_generator_exploration thin adapter
existing structured exploration presentation reuse
grouped occurrence metadata
KaTeX rendering
zero-occurrence semantics preserved
browser/manual integration
```

Phase 121 final regression:

```text
9197 passed in 455.68s (0:07:35)
```

---

# 3. 現在の Web UI

起動:

```text
python -m flask --app web_app run --debug
```

generator exploration:

```text
generator input
generator LaTeX
occurrence count
Toda bracket grouping
map-input grouping
group-generator grouping
composition-left grouping
composition-right grouping
other-occurrence grouping
roles
phase
theorem
KaTeX
```

代表例:

```text
nu_prime
→ 6 direct standard-repository occurrences

sigma_11
→ 0 direct explore occurrences

eta_999
→ 0 occurrences as a normal result
```

`sigma_11` の direct `explore` が 0 件でも、recursive proof-scope の `explore-proof sigma_11` では既存 specialization により occurrence を得られる。

```text
explore
!= explore-proof
```

---

# 4. Phase 121 完了境界

```text
generator を browser から入力できる
existing standard repository exploration を使う
existing structured exploration presentation を使う
CLI Markdown を解析しない
generator / occurrence conclusion を LaTeX 表示する
roles / phase / theorem を表示する
grouped section が空でも正常に扱う
unknown indexed generator の 0 occurrence を正常結果として扱う
explore sigma_11 の direct 0 occurrence semantics を維持する
explore-proof semantics を混入させない
group query を壊さない
operation query / query-proof を壊さない
generator proof を壊さない
browser KaTeX smoke が通る
repository-wide pytest が通る
```

Phase 121 は完了。

---

# 5. 次 Phase: remaining read-only Web capability audit

remaining read-only capability:

```text
explore-proof
explore-applicable
```

優先して確認する観点:

```text
既存 structured presentation の完成度
Web 専用 presentation boundary を追加する必要があるか
generator 入力だけで成立するか
結果量が browser usability に与える影響
recursive proof-scope の root / depth / provenance をどう表示するか
applicability の source / rule family / candidate grouping をどう表示するか
CLI-only Markdown に依存していないか
proof / provenance semantics を変えずに接続できるか
```

現時点では `explore-proof` は read-only で利用価値が高いが、`explore` より dedicated presentation boundary が弱い。

`explore-applicable` は structured presentation がある一方、候補量と UI 階層が大きく、次の候補選択 / execute workflow に近い。

したがって次 Phase は両者を再監査し、実装する場合も1 capability に限定する。

---

# 6. `execute` Web integration の境界

`execute` は read-only capability と同列に扱わない。

現在の user execution workflow は、

```text
generator
→ executable target resolution
→ NONE / AMBIGUOUS / EXECUTED
→ candidate selection
→ qualified execution
→ proof result
```

を含む。

Web 公開には少なくとも、

```text
candidate selection UI
ambiguity handling
execution status presentation
既存 execution semantics の非変更
```

を専用に監査する必要がある。

したがって `execute` は remaining read-only Web capability より後段とする。

---

# 7. 数学的 capability pressure

Web UI の発展とは別に、残存数学 pressure を保持する。

```text
H(nu_5)
H(sigma_11)
Delta(sigma_11)
E(nu_prime)
Delta(nu_prime)
E(nu_5 o eta_8)
```

今後も

```text
実利用
→ pressure
→ existing mathematics reuse audit
→ minimum missing capability
```

の順で扱う。

---

# 8. 長期保留

```text
operation-query grammar generalization
general E/H/Delta evaluator
general Toda bracket solver
coset / indeterminacy computation
semantic theorem ranking
proof-cost optimization
producer ranking
unbounded backtracking
persistent cache / parallelization
repository snapshot / versioning
rich graph proof visualization
odd-primary integration
all-primary ordinary sphere-homotopy calculation
authentication
database persistence
deployment automation
rich SPA architecture
```

---

# 9. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい theorem root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
Web UI から数学 semantics を変更しない
CLI と Web の数学結果を分岐させない
focused regression で境界を固定する
browser/manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```
