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
運用リポジトリの組み立て != 定理事実
証明範囲の走査 != 定理探索
既知関係の発見 != 写像評価
Toda bracket membership の発見 != bracket の解法
適用可能候補 != 証明成功
関連度カテゴリ != 定理順位
handoff 検証 != 定理事実
実行資格を満たす候補 != 一意な実行対象
実行ファミリーのグループ化 != 生カタログの重複除去
代表候補の選択 != 定理順位付け
generic qualification != family-specific execution strategy
family dispatch != theorem ranking
production application recovery != arbitrary companion-premise search
性能最適化 != 数学的意味論の変更
user-facing target resolver != theorem ranking
candidate number != mathematical priority
presentation != proof object
repository target goal equality != executed conclusion object identity
CLI addressing != proof-graph internal addressing
known-group identity lookup != qualified execution
known-group proof replay != theorem application execution
symbolic theorem specialization != arbitrary symbolic AST rewriting
specialization provenance != production-rule re-execution
operation query lookup != operation evaluator
deduplicated presentation != raw provenance deletion
operation-query proof replay != enclosing theorem replay
safe type fallback != invented mathematical explanation
```

---

# 2. 現在の主要経路

計算:

```text
式 / statement
→ proof / inference
→ Toda 固有知識
→ ProofRepository / rule catalog
→ bounded search
→ TodaGroupQuery / lookup
→ group result
→ EHP / proof provenance
→ presentation
→ report
```

generator / applicability:

```text
generator 文字列
→ GeneratorSymbol
→ standard production repository
→ recursive ProofStep ancestry
→ generator-specific proof-scope specialization
→ occurrence
→ Toda membership / known map relation
→ premise-pattern compatibility
→ applicability candidates
→ relevance-classified presentation
```

known-group proof replay:

```text
generator
→ known-group identity
→ source ProofStep
→ bounded direct ancestry
→ replay presentation
→ show-proof
```

qualified execution:

```text
generator
→ executable-target resolver
→ candidate selection
→ qualified execution handoff
→ bounded execution
→ actual executed ProofStep
→ Result + Proof
→ execute
```

operation query:

```text
operation query string
→ minimal query parser
→ repository / proof-scope lookup
→ raw matches
→ mathematical-statement presentation grouping
→ stable prioritization
→ query CLI
```

operation-query proof replay:

```text
query result
→ selected presented fact
→ primary provenance match
→ selected fact's own ProofStep
→ bounded direct premise replay
→ statement presentation
→ query-proof CLI
```

---

# 3. 主要モジュール

基礎:

```text
expression.py
proof.py
proof_repository.py
rule_catalog.py
repository_inference.py
homotopy_groups.py
toda_rules.py
```

探索 / applicability:

```text
generator_input.py
repository_proof_scope.py
repository_proof_scope_exploration.py
repository_proof_scope_facade.py
repository_proof_scope_applicability.py
repository_generator_applicability_facade.py
repository_generator_applicability_selection.py
repository_generator_applicability_presentation.py
repository_generator_applicability_renderer.py
```

known-group / specialization / replay:

```text
repository_generator_known_group_identity_lookup.py
repository_generator_known_group_identity_presentation.py
repository_generator_known_group_identity_renderer.py
repository_symbolic_sigma_specialization.py
repository_generator_known_group_proof_replay.py
repository_generator_known_group_proof_replay_presentation.py
repository_generator_known_group_proof_replay_renderer.py
```

operation query / replay:

```text
repository_operation_query.py
repository_operation_query_lookup.py
repository_operation_query_facade.py
repository_operation_query_presentation.py
repository_operation_query_renderer.py
repository_operation_query_proof_replay.py
repository_operation_query_proof_replay_presentation.py
repository_operation_query_proof_replay_statement_presentation.py
repository_operation_query_proof_replay_renderer.py
```

qualified execution:

```text
repository_generator_applicability_execution_seed.py
repository_generator_applicability_execution_entry.py
repository_generator_applicability_execution_orchestration.py
repository_generator_production_application_recovery.py
repository_generator_production_application_execution_seed.py
repository_generator_two_premise_execution_integration.py
repository_generator_qualified_execution_selection.py
repository_generator_qualified_execution_family.py
repository_generator_qualified_execution_family_selection.py
repository_generator_qualified_execution_dispatch.py
repository_generator_standard_qualified_execution_facade.py
```

user-facing execution:

```text
repository_generator_user_execution_resolver.py
repository_generator_user_execution_handoff.py
repository_generator_user_execution_proof_step.py
repository_generator_user_execution_presentation.py
repository_generator_user_execution_renderer.py
repository_generator_user_execution_facade.py
repository_generator_user_execution_candidate_presentation.py
repository_generator_user_execution_candidate_renderer.py
main.py
```

---

# 4. 証明事実と metadata

証明事実の中心:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata である。

renderer、facade、CLI、resolver、探索、applicability 分類、presentation grouping は証明事実を追加しない。

---

# 5. Repository 非破壊

query / exploration / applicability / execution planning / known-group replay / operation query / operation-query proof replay は元の repository を読み取り専用として扱う。

execution は新しい inference result を構成できるが、元 repository を変更しない。

```text
entries before == entries after
```

必要な経路では既存 `ProofStep` identity を保持する。

---

# 6. Applicability semantics

candidate は概念的に

```text
catalog_entry
premise_index
premise_pattern
source_step
bindings
```

を保持する。

```text
premise compatibility != 全 premise 成立
candidate != rule execution
candidate != proof success
candidate != theorem truth
```

relevance category は theorem ranking ではない。

---

# 7. Qualified-execution boundary

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

multi-premise candidate から companion premise を任意探索しない。

一致条件:

```text
same root_entry identity
same inference_rule identity
target conclusion == explicit goal
target premises[candidate premise_index] is candidate.source_step
```

`UNIQUE` のときだけ exact `premises` tuple を利用する。

recovered premise tuple は同じ順序・同じ `ProofStep` identity のまま execution seed に使う。

---

# 8. User-facing executable-target semantics

workflow status:

```text
NONE
AMBIGUOUS
EXECUTED
```

規則:

```text
0 executable targets
→ NONE

1 executable target + candidate_number omitted
→ automatic execution

multiple executable targets + candidate_number omitted
→ AMBIGUOUS

candidate_number supplied
→ select that one-based target
```

`candidate_number` は表示順に対応する 1-based addressing であり、数学的優先度を意味しない。

```text
candidate number != theorem ranking
```

---

# 9. Executed final ProofStep boundary

user-facing execution は repository 側の original target step を presentation しない。

実際に bounded execution が生成した

```text
repository_inference_result.goal_step
```

を final executed `ProofStep` とする。

```text
executed goal_step
is not necessarily original repository target_step
```

ただし

```text
executed goal_step.conclusion == selected target goal
```

である。

---

# 10. Known-group identity semantics

known-group identity lookup は、まず explicit ambient-group fact を利用する。

explicit fact がない場合でも、限定された generator に対して既存 proof scope の group relation から ambient group を導出できる。

代表例:

```text
nu_5
sigma'''
sigma''
sigma'
sigma_8
sigma_9
generic concrete sigma_n specialization
```

target group が一意に定まる場合だけ known-group identity node を返す。

```text
known-group identity lookup
!= theorem search
!= qualified execution
```

---

# 11. Indexed sigma specialization boundary

Toda Proposition 5.15 の symbolic higher step は

\[
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9
\]

を表す。

concrete generic specialization は indexed `GeneratorSymbol(family="σ", index=n)` の concrete integer \(n\ge 10\) に限定する。

specialization step は symbolic higher step を direct premise として保持する。

```text
concrete sigma_n group step
→ premise: symbolic Proposition 5.15 higher step
```

任意の symbolic AST substitution engine は導入しない。

---

# 12. show-proof と execute の分離

```text
show-proof
→ 既知 group の proof を表示 / replay

execute
→ generator に関連する qualified theorem application を実行
```

したがって、

```text
show-proof != execute
```

---

# 13. Operation query semantics

Phase 110 の operation query は「既存の proof fact を探す」ための経路である。

対象 query:

```text
H(<operand>)
E(<operand>)
Delta(<operand>)
<generator> o <generator>
```

operand は Phase 110 では generator または 1 個の binary composition に限定する。

代表:

```text
H(nu_prime)
Delta(iota_9)
E(eta_2 o nu_prime)
eta_2 o nu_prime
```

重要:

```text
operation query lookup
!= inference
!= mathematical evaluation
```

該当 fact が見つからない場合も、それは「repository / proof scope に対応する既知 fact がない」ことだけを意味する。

---

# 14. Operation query lookup boundary

`H` は既存 map-relation path を利用する。

`E` は repository 内で既存表現が複数あるため、既存 `MapApplication(E, ...)` と `Suspension(...)` の意味を lookup 時に認識する。

\(\Delta\) は `TodaDeltaImageUpToSignStatement` を既存 statement のまま保持する。

composition query は exact composition の structural containment を探す。

parser / lookup は evaluator input を生成しない。

---

# 15. Raw occurrence と presentation grouping

proof scope は同じ `ProofStep` が複数 repository root から到達可能なことを provenance として保持する。

したがって raw lookup 結果を削除してはいけない。

Phase 110 の deduplication は presentation layer だけで行う。

```text
raw lookup result
→ equal mathematical statement grouping
→ presentation item
```

各 presentation item は、その statement に対応する全 raw match を保持する。

```text
deduplicated display
!= provenance deletion
```

---

# 16. Operation query prioritization

primary display order は概念的に

```text
minimum proof-scope depth
→ stable original source order
```

である。

これは user-facing readability のための順序であり、

```text
presentation order != theorem ranking
```

である。

---

# 17. Operation-query proof replay boundary

query fact replay の root は enclosing repository theorem root ではない。

```text
presentation item
→ primary_match
→ primary_match.scope_node.proof_step
→ replay root
```

つまり、例えば

\[
H(\nu')=\eta_5
\]

を replay する場合、depth 0 はこの relation 自身である。

```text
operation-query proof replay
!= repository theorem replay
```

---

# 18. Multiple fact selection

query に複数の mathematical fact がある場合、自動で先頭を proof replay しない。

```text
1 fact
→ --fact 省略可

multiple facts
→ fact list
→ --fact N が必要
```

`--fact` は 1-based addressing である。

```text
fact number != theorem ranking
```

---

# 19. Operation-query replay depth

Phase 110 の replay default は direct premises の 1 段。

```text
max_depth = 1
```

CLI `--depth` はまだ追加しない。

必要性が確認された場合のみ次 Phase 以降で検討する。

---

# 20. Operation-query statement presentation

statement 表示は次の優先順を取る。

```text
existing Toda proof statement renderer
→ existing repository conclusion renderer
→ Phase 110 narrow statement-specific presentation
→ safe class-name fallback
```

user-facing replay で dataclass の巨大な raw `repr` に落とさない。

Phase 110 で明示的に追加した presentation coverage:

```text
Toda53NuPrimeBracketSpecializationStatement
TodaLemma57TwoIota5ImageMembershipStatement
TodaDeltaSurjectiveStatement
```

例:

\[
\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1,
\]

\[
E^2\nu'\in2\iota_5\circ\pi_8^5,
\]

\[
\Delta:\pi_8^5\to\pi_6^2
\quad\text{is surjective}.
\]

aggregate theorem statement は branch を推測せず、

```text
`TodaProp56FiniteDimensionalStatement`
```

のような safe type fallback を使う。

---

# 21. CLI boundary

現行:

```text
python main.py n k
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
python main.py show-proof nu_prime
python main.py show-proof sigma_11
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"
python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "E(eta_2 o nu_prime)"
```

`query-proof`:

```text
no known fact
→ message + exit 1

multiple facts + --fact omitted
→ list facts + request --fact N + exit 1

selected fact
→ proof replay + exit 0

invalid query / invalid fact number
→ argparse error + exit 2
```

---

# 22. Windows UTF-8 CLI boundary

Windows の既定 CP932 では `η₂`、`ν₄` などの Unicode 数学文字を stdout に出力できない場合がある。

実プロセス CLI のみ stdout / stderr を UTF-8 に再構成する。

---

# 23. Phase 110 closure

Phase 110 は user-facing operation query の実需要監査から開始し、既存 proof fact lookup と proof replay を閉じた。

確定した意味論:

```text
lookup != evaluator
```

```text
deduplicated presentation != raw provenance deletion
```

```text
query-proof root = selected fact's own ProofStep
```

```text
multiple facts
→ no silent auto-selection
```

```text
unknown replay statement
→ safe type fallback
```

最終 repository-wide regression:

```text
9055 passed in 455.09s (0:07:35)
```

最終 whitespace check:

```text
git diff --check
clean
```

---

# 24. Deferred capabilities

```text
semantic auto-selection among multiple executable targets
theorem ranking
proof-cost optimization
producer ranking
general unbounded backtracking
persistent cache / parallelization
repository snapshot / versioning
stale-search-report detection
third qualified family without new production pressure
arbitrary nested operation-query grammar
Unicode composition input
LaTeX operation-query parser
operation-query CLI --depth
manual alternate provenance selection
general Toda-bracket solver
general composition evaluator
general E / H / Δ evaluator
coset / indeterminacy computation
broader unstable stems
odd-primary full integration
all-primary ordinary sphere-homotopy calculation
unrestricted symbolic AST substitution
rich recursive proof visualization
Web UI
```

---

# 25. 次 Phase との境界

Phase 110 は完了。

Phase 111 では general evaluator を自動的に開始しない。

まず、Phase 110 までに揃った CLI capability 全体を利用者視点で監査し、次に実際に不足している操作・表示・query grammar・proof replay depth などの pressure を確認する。

```text
current CLI capability audit
→ actual user pressure
→ next smallest missing capability
```
