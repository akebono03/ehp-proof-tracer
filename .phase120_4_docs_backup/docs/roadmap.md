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

Web group query:

```text
browser
→ Flask
→ thin Web group adapter
→ existing calculation facade
→ structured presentation
→ existing LaTeX renderer
→ KaTeX
```

Web operation query:

```text
browser query
→ thin Web operation adapter
→ existing operation-query facade
→ existing structured presentation
→ statement_latex
→ KaTeX
```

Web query-proof:

```text
selected fact
→ existing proof replay
→ replay presentation
→ provenance + proof steps
→ KaTeX / safe fallback
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
118-1 operation-query Web boundary audit
118-2 operation-query Web UI
118-3 explicit fact selection + query-proof Web
118-4 depth 0 / 1 / 2 + safe fallback + browser audit
118-5 documentation / completion
```

Final regression:

```text
9169 passed in 465.97s (0:07:45)
```

---

# 3. 現在の Web UI

起動:

```text
python -m flask --app web_app run --debug
```

group query:

```text
n
k
FOUND
NOT_FOUND
MULTIPLE_RESULTS
KaTeX
```

operation query:

```text
H(nu_prime)
Delta(iota_9)
E(nu_5)
E(sigma_11)
```

query-proof:

```text
explicit fact selection
conclusion
theorem / phase provenance
repository depth
proof steps
rule names
depth 0 / 1 / 2
safe unsupported-statement fallback
KaTeX
```

まだ Web に接続していない主要 capability:

```text
show-proof
explore
explore-proof
explore-applicable
execute
```

---

# 4. Phase 118 完了境界

完了条件:

```text
operation query を browser から入力できる
existing structured presentation を使う
statement_latex を KaTeX 表示する
複数 fact を自動選択しない
fact を明示選択して query-proof を replay できる
selected fact の provenance を保持する
proof depth 0 / 1 / 2 を browser から選べる
unsupported statement を safe fallback できる
raw Python repr を browser へ漏らさない
group query を壊さない
browser smoke が通る
repository-wide pytest が通る
```

Phase 118 は完了。

---

# 5. Phase 119: next Web capability pressure audit

Phase 119 は新機能を先に決め打ちせず、Phase 118 までの Web UI を実利用したうえで、次に Web 接続する価値が高い既存 capability を監査する。

監査候補:

```text
show-proof
explore
explore-proof
explore-applicable
execute
```

優先して確認する観点:

```text
read-only か execution か
利用者が何を選択する必要があるか
既存 structured presentation が十分か
CLI-only formatting に依存していないか
Web で ambiguity を安全に扱えるか
proof / provenance semantics を変えずに接続できるか
```

`execute` は qualified candidate selection を伴うため、read-only exploration より慎重に扱う。

Phase 119 の終了時に、次の実装 Phase を1つだけ選ぶ。

---

# 6. 数学的 capability pressure

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

# 7. 長期保留

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

# 8. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい theorem root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
Web UI から数学 semantics を変更しない
CLI と Web の結果を分岐させない
focused regression で境界を固定する
repository-wide regression で Phase を閉じる
```
