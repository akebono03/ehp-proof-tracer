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
運用 repository の組み立て != 定理事実
proof-scope 走査 != 定理探索
既知関係の発見 != 写像評価
適用可能候補 != 証明成功
候補番号 != 数学的優先度
既知群同一性検索 != qualified execution
symbolic theorem の具体化 != 任意の symbolic AST 書き換え
演算問い合わせ検索 != 演算 evaluator
CLI --depth != 新しい proof search
TodaGroupQuery specialization reuse != 新しい定理 root
LOOKUP_MISS != evaluator 不足の確定
```

---

# 2. 現在の主要経路

計算:

```text
ProofRepository
→ TodaGroupQuery
→ direct group lookup
→ 必要なら限定的 theorem-specific specialization
→ group result
→ proof / EHP provenance
→ report
```

生成元探索:

```text
generator input
→ GeneratorSymbol
→ recursive proof scope
→ generator-specific specialization
→ occurrence / applicability
```

known-group replay:

```text
generator
→ known-group identity
→ source ProofStep
→ bounded ancestry
→ show-proof
```

operation query:

```text
query string
→ minimal parser
→ repository / proof-scope lookup
→ presentation grouping
→ query
```

現在の基本意味論:

```text
query = existing fact lookup
lookup != inference != evaluator
```

---

# 3. 主要モジュール

Toda group calculation:

```text
toda_group_query.py
toda_group_lookup.py
toda_group_result.py
toda_calculation.py
toda_calculation_facade.py
toda_calculation_report.py
```

proof scope / specialization:

```text
repository_proof_scope.py
repository_symbolic_sigma_specialization.py
repository_generator_known_group_identity_lookup.py
```

operation query:

```text
repository_operation_query.py
repository_operation_query_lookup.py
repository_operation_query_facade.py
repository_operation_query_presentation.py
repository_operation_query_proof_replay.py
```

qualified execution:

```text
repository_generator_production_application_recovery.py
repository_generator_qualified_execution_selection.py
repository_generator_qualified_execution_family.py
repository_generator_qualified_execution_dispatch.py
repository_generator_standard_qualified_execution_facade.py
```

CLI:

```text
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

renderer、facade、CLI、resolver、探索、表示 grouping は証明事実を追加しない。

---

# 5. Repository 非破壊

元 repository は読み取り専用として扱う。

Phase 113 の TodaGroupQuery specialization も元 repository に root を追加しない。

```text
entries before == entries after
```

---

# 6. Indexed sigma specialization

Toda Proposition 5.15:

$$
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
$$

concrete indexed $\sigma_n$ の theorem-specific specialization は整数 $n\ge 10$ に限定する。

```text
concrete sigma_n group step
→ premise: symbolic Proposition 5.15 higher step
```

任意の symbolic AST substitution engine は導入しない。

---

# 7. Phase 113: TodaGroupQuery specialization reuse

Phase 113 では既存の specialization capability を `TodaGroupQuery` 経路から再利用する。

対象:

```text
query.k == 7
query.n >= 10
```

流れ:

```text
build_known_toda_calculation_result
→ direct normalized group lookup
→ direct result が無い場合のみ
→ build_repository_proof_scope(repository)
→ GeneratorSymbol(family="σ", index=query.n)
→ specialize_repository_proof_scope_for_generator(...)
→ added specialized node
→ query.target と一致する concrete group relation
→ TodaGroupResult
→ existing report pipeline
```

不変条件:

```text
direct lookup first
specialization is fallback only
empty repository → NOT_FOUND
specialized result premise = symbolic Proposition 5.15 step
root phase / theorem provenance を保持
repository root entries は変更しない
k != 7 では使わない
n < 10 では使わない
```

例:

$$
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\}.
$$

これは新しい数学的定理の追加ではない。

---

# 8. show-proof と execute の分離

```text
show-proof
→ 既知群 proof を表示 / 再生

execute
→ qualified theorem application
```

```text
show-proof != execute
```

Phase 113 は `execute sigma_11` の意味論を変更しない。

---

# 9. 演算問い合わせの意味論

現在の operation query は既存 fact lookup である。

```text
operation query lookup
!= inference
!= mathematical evaluation
```

Phase 112 で、`E(nu_5)` のように lookup miss でも既存 symbolic inference に関連数学が存在する例を確認した。

したがって:

```text
LOOKUP_MISS
!= mathematical unknown
!= evaluator required
```

---

# 10. Operation-query parser の境界

現在対応:

```text
二項 top-level composition
三項 top-level composition
E / H の generator operand
E / H の二項 composition operand
Delta の generator operand
```

意図的に未対応:

```text
四項以上
E(a o b o c)
H(a o b o c)
Delta(a o b o c)
Unicode ∘
一般再帰 parser
```

---

# 11. 証明再生

default:

```text
max_depth = 1
```

CLI:

```text
python main.py show-proof sigma_11 --depth 2
python main.py query-proof "H(nu_prime)" --fact 1 --depth 2
```

`--depth` は既存 ancestry の表示範囲であり、新しい proof search ではない。

---

# 12. CLI 境界

`n,k` は project quantity

$$
\pi_{n+k}^n
$$

すなわち free part + 2-primary component を表す。

stable 7-stem 例:

```text
python main.py 10 7
python main.py 11 7
python main.py 12 7
```

---

# 13. Phase 112 / 113 closure

Phase 112:

```text
real workflow pressure audit
→ gap classification
→ lookup vs inference vs evaluator boundary
→ highest-pressure minimal capability selection
```

Phase 113:

```text
existing sigma_n specialization
→ TodaGroupQuery integration
```

full regression:

```text
9081 passed in 434.58s (0:07:14)
```

---

# 14. 次 Phase との境界

次候補 Phase 114:

```text
operation query
→ direct lookup
→ lookup miss
→ 許可された最小 existing inference handoff
```

最初の代表対象:

$$
E(\nu_5)=\nu_6.
$$

先取りしない:

```text
general E evaluator
general H evaluator
general Delta evaluator
arbitrary query-to-inference fallback
four-term composition
three-term map-operation operand
Unicode composition parser
execute sigma_11 expansion
```
