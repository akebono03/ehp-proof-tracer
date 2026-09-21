# EHP Proof Tracer ロードマップ

この文書は**今後の capability dependency と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

運用計算:

```text
raw n,k
→ python main.py n k
→ standard production repository
→ proof report
```

generator exploration:

```text
generator
→ recursive proof scope
→ generator-specific specialization
→ Toda membership / known map relation
→ applicability candidates
→ relevance-classified presentation
```

known-group proof replay:

```text
generator
→ known-group identity
→ existing ProofStep
→ direct proof replay
→ python main.py show-proof ...
```

user-facing qualified execution:

```text
generator input
→ executable-target resolution
→ NONE / AMBIGUOUS / executable target
→ candidate list / one-based candidate selection
→ qualified execution
→ final executed ProofStep
→ Result + Proof
→ python main.py execute ...
```

operation query:

```text
operation query
→ existing repository / proof-scope fact lookup
→ deduplicated mathematical presentation
→ preserved provenance
→ python main.py query ...
```

operation-query proof replay:

```text
selected query fact
→ primary provenance
→ fact's own ProofStep
→ bounded direct replay
→ safe mathematical rendering
→ python main.py query-proof ...
```

最新:

```text
Phase 110 closure:
9055 passed in 455.09s (0:07:35)
git diff --check: clean
```

Phase 110 は完了。

---

# 2. 完了済み capability

Phase 90–104:

```text
query / normalization
EHP / proof provenance
calculation orchestration / report
generator exploration
recursive proof scope
applicability discovery
relevance classification
safe candidate handoff
bounded execution provenance
```

Phase 105:

```text
first qualified family
exact source seed
family grouping
explicit root + source selection
standard first-family facade
```

Phase 106:

```text
applicability performance audit
generator-relevant scope prefilter
```

Phase 107:

```text
multi-premise recovery
exact premise-tuple seed
second qualified family
explicit root + source + family selection
family dispatch
multi-family standard facade
```

Phase 108:

```text
user-facing executable-target resolver
ambiguity-safe workflow
one-based candidate addressing
final executed ProofStep extraction
minimal Result + Proof presentation
candidate-list presentation
execute CLI
Windows UTF-8 CLI boundary
```

Phase 109:

```text
known-group identity integration
proof-derived ambient-group fallback
generic concrete indexed sigma_n specialization
proof-scope specialization integration
known-group proof replay
show-proof CLI
known-group-first ambiguous execute presentation
candidate-order / theorem-ranking boundary closure
```

Phase 110:

```text
minimal operation-query parser
existing H / E / Delta / composition fact lookup
query CLI
raw occurrence preservation
equal-statement deduplicated presentation
shallow-depth prioritization
query fact selection
fact-rooted proof replay
query-proof CLI
narrow mathematical statement presentation
safe aggregate type fallback
completion regression
```

---

# 3. 現在の execution API

Phase 107 multi-family:

```text
execute_standard_repository_generator_applicability_result_by_root_source_and_family(
  applicability_result,
  root_entry,
  source_step,
  family_name,
  goal,
  max_depth=2,
  retry_policy=None,
)
```

Phase 108 user workflow:

```text
run_standard_repository_generator_user_execution_workflow(
  generator_input,
  candidate_number=None,
  max_depth=2,
  retry_policy=None,
)
```

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

third qualified family はまだ追加していない。

---

# 4. 現在の replay API

known-group replay:

```text
build_standard_repository_generator_known_group_proof_replay_input(
  generator_input,
  max_depth=1,
)
```

operation-query replay:

```text
build_repository_operation_query_proof_replay(
  presentation,
  fact_number=None,
  max_depth=1,
)
```

両者は別 semantics。

```text
show-proof
→ known-group identity proof replay

query-proof
→ selected operation fact proof replay
```

---

# 5. 現在の CLI

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

---

# 6. 確定した user-facing 境界

ambiguity:

```text
multiple executable targets
→ 自動選択しない
```

candidate number:

```text
1-based addressing
!= theorem ranking
```

known-group replay:

```text
show-proof
!= execute
```

operation query:

```text
lookup
!= inference
!= evaluator
```

deduplication:

```text
deduplicated presentation
!= raw provenance deletion
```

query-proof:

```text
selected fact's ProofStep
!= enclosing repository theorem root
```

multiple query facts:

```text
--fact omitted
→ silent auto-selection しない
```

unknown replay statement:

```text
safe type-name fallback
!= invented branch explanation
```

---

# 7. Phase 111 第一候補：CLI capability / user pressure audit

Phase 110 までで calculation、exploration、applicability、known-group replay、qualified execution、operation fact query、operation fact proof replay が CLI から利用可能になった。

次は general evaluator を先に実装せず、利用者視点で現在の CLI capability を監査する。

監査候補:

```text
どの操作が discoverable か
query / query-proof / show-proof / execute の役割分離
operation query grammar の実際の不足
proof replay depth 1 の十分性
alternate provenance 選択の必要性
composition query の見つけやすさ
CLI help / command discoverability
既存 full proof report の presentation 残課題
```

実需要が確認された項目だけを次の実装 Phase にする。

---

# 8. 保留：operation query grammar expansion

現在の最小 grammar:

```text
H(<operand>)
E(<operand>)
Delta(<operand>)
<generator> o <generator>
```

保留:

```text
nested composition
3-term composition
Unicode ∘
LaTeX input
implicit composition
general expression parser
```

grammar 拡張だけを目的に先取りしない。

---

# 9. 保留：operation evaluator

未実装:

```text
general composition evaluator
general E evaluator
general H evaluator
general Delta evaluator
repository に未表現の fact の自動導出
```

Phase 110 の `query` は lookup のまま維持する。

---

# 10. 保留：proof replay 拡張

現在の `show-proof` / `query-proof` は default direct-premise depth 1。

必要性が確認された場合のみ検討:

```text
CLI --depth
recursive ancestry presentation
dependency-first narrative
shared dependency display
alternate provenance selection
rich proof visualization
```

---

# 11. 保留：semantic automatic target selection

複数候補から数学的に「最善」を選ぶ機能は未実装。

```text
theorem ranking
shortest-proof ranking
proof-cost optimization
semantic goal priority
automatic target preference
```

候補順を ranking と解釈しない。

---

# 12. 保留：additional qualified families

third family 以降は coverage 拡張だけを目的に admission しない。

次を確認する。

```text
actual production source
execution safety
goal compatibility
required seed context
rule identity preservation
producer-search behavior
user-facing need
new architectural pressure
```

---

# 13. 保留：数学的 broader coverage

```text
general Toda-bracket solver
indeterminacy / coset normalization
broader unstable stems
odd-primary integration
all-primary ordinary sphere-homotopy calculation
```

---

# 14. 保留：optimization / versioning

```text
general backtracking
producer ranking
proof-cost optimization
best-proof selection
persistent cache
parallelization
repository snapshot / versioning
stale-search-report detection
```

Phase 106 の prefilter 以降、次の optimization は実測圧力を確認してから行う。

---

# 15. 保留：UI 拡張

現在 CLI で calculation / exploration / applicability / replay / execution / operation query が利用できる。

未実装:

```text
Web UI
interactive candidate selection
persistent execution history
rich recursive proof visualization
```

---

# 16. 次 Phase の開始境界

Phase 110 の operation-query capability を機械的に拡張しない。

次はまず:

```text
Phase 111
CLI capability / user pressure audit
```

その監査結果から、実際に不足している最小 capability を次の実装範囲にする。
