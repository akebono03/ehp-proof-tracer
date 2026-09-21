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
限定 theorem-specific handoff != general query inference
CLI --depth != 新しい proof search
TodaGroupQuery specialization reuse != 新しい定理 root
LOOKUP_MISS != evaluator 不足の確定
expression occurrence != operation result
related mathematics exists != reusable operation relation exists
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
→ direct repository / proof-scope lookup
→ direct hit はそのまま返す
→ direct miss のうち許可された exact handoff のみ具体化
→ presentation grouping
→ query
```

現在の基本意味論:

```text
direct lookup first
query != general inference engine
query != general evaluator
```

現在許可される exact handoff:

```text
E(nu_5)
E(sigma_11)
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
repository_nu5_stable_bridge_specialization.py
repository_sigma11_suspension_specialization.py
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

renderer、facade、CLI、resolver、探索、表示 grouping は独立した定理事実を追加しない。

theorem-specific specialization は新しい独立 theorem root を追加せず、既存 `ProofStep` を premise とする concrete `ProofStep` を生成する。

---

# 5. Repository 非破壊

元 repository は読み取り専用として扱う。

Phase 113 の TodaGroupQuery specialization、Phase 114 の `E(nu_5)` handoff、Phase 115 の `E(sigma_11)` handoff は元 repository に root を追加しない。

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

Phase 113–115 は `execute sigma_11` の意味論を変更しない。

---

# 9. 演算問い合わせの意味論

operation query は lookup-first である。

```text
operation query
→ direct existing-fact lookup
→ hit ならそのまま返す
→ miss なら exact handoff guard
→ 許可された場合だけ theorem-specific specialization
```

現在許可される handoff:

```text
E(nu_5)
E(sigma_11)
```

Phase 114 の既存 symbolic bridge:

$$
E^{n-5}\nu_5=\nu_n.
$$

$n=6$ への concrete specialization:

$$
E(\nu_5)=\nu_6.
$$

```text
concrete E(nu_5) ProofStep
→ premise: existing symbolic Proposition 5.6 bridge
```

Phase 115 の既存 $\sigma$-family definition:

$$
\sigma_n=E^{n-8}\sigma_8.
$$

concrete operation result:

$$
E(\sigma_{11})=\sigma_{12}.
$$

```text
concrete E(sigma_11) ProofStep
→ premise: existing symbolic TodaSigmaFamilyDefinitionStatement
```

したがって:

```text
LOOKUP_MISS
!= mathematical unknown
!= evaluator required

limited handoff
!= arbitrary query-to-inference fallback
!= general E evaluator
```

direct lookup は常に handoff より優先される。

---

# 10. Exact handoff guards

## `E(nu_5)`

`repository_nu5_stable_bridge_specialization.py` は対象を exact に判定する。

```text
RepositoryMapOperationQuery
operation == "E"
operand == RepositoryGeneratorQuery(GeneratorSymbol("ν", index=5))
direct lookup result is empty
```

## `E(sigma_11)`

`repository_sigma11_suspension_specialization.py` も対象を exact に判定する。

```text
RepositoryMapOperationQuery
operation == "E"
operand == RepositoryGeneratorQuery(GeneratorSymbol("σ", index=11))
direct lookup result is empty
```

対象外:

```text
E(sigma_10)
E(sigma_12)
E(sigma_100)
H(sigma_11)
Delta(sigma_11)
E(sigma_11 o eta_18)
```

これらを同じ handoff が発火させない。

---

# 11. `E(sigma_11)` specialization semantics

Phase 115 は group specialization そのものを operation result とみなさない。

既存 `TodaSigmaFamilyDefinitionStatement` から、

```text
sigma_11 concrete definition
sigma_12 concrete definition
```

を同じ `sigma8_statement` provenance で構成する。

そのうえで、

$$
E(\sigma_{11})=\sigma_{12}
$$

という concrete `Relation` を生成する。

重要:

```text
TodaSigmaFamilyDefinitionStatement
!= operation-query Relation
```

Phase 115 の新規 concrete step は、この不足を theorem-specific definitional specialization として埋める。

```text
concrete operation step
→ premise: symbolic sigma-family definition
```

これは新しい独立 theorem root ではない。

---

# 12. Operation-query parser の境界

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

Phase 115 は parser grammar を変更しない。

---

# 13. 証明再生

default:

```text
max_depth = 1
```

CLI:

```text
python main.py show-proof sigma_11 --depth 2
python main.py query-proof "H(nu_prime)" --fact 1 --depth 2
python main.py query-proof "E(nu_5)"
python main.py query-proof "E(nu_5)" --depth 2
python main.py query-proof "E(sigma_11)"
python main.py query-proof "E(sigma_11)" --depth 2
```

`--depth` は既存 ancestry の表示範囲であり、新しい proof search ではない。

`E(nu_5)`:

```text
concrete E(nu_5) = nu_6
→ symbolic Proposition 5.6 bridge
```

`E(sigma_11)`:

```text
concrete E(sigma_11) = sigma_12
→ TodaSigmaFamilyDefinitionStatement
→ TodaLemma514Sigma8Statement
→ ScalarGreaterEqualStatement
```

---

# 14. 表示と provenance

同一数学 statement が複数 proof-scope path から得られる場合、表示 layer は grouping できる。

```text
deduplicated presentation
!= provenance deletion
```

proof replay の root は選択された query fact 自身の `ProofStep` である。

```text
query-proof root
!= enclosing repository theorem root
```

`E(sigma_11)` の CLI 表示:

$$
E\sigma_{11}=\sigma_{12}.
$$

Phase 114 の symbolic bridge の scalar 表示が

```text
E^{n + -1\,5}ν_5
```

のように現れる場合がある。これは scalar LaTeX presentation の既存残件であり、operation handoff 意味論とは分離する。

---

# 15. Expression occurrence と operation result

Phase 115-5 で次を明示的に区別した。

既存 proof 内に

$$
E\nu'
$$

や

$$
E^2\nu'
$$

が部分式として現れていても、

$$
E(\nu')=\alpha
$$

という `Relation` が存在することを意味しない。

したがって:

```text
expression occurrence
!= operation result relation
```

同様に、$\sigma_8$ 周辺で

$$
H(\sigma_8)=\iota_{15}
$$

に関連する数学が存在していても、現在の proof infrastructure に

$$
H(\sigma_{11})
$$

を導く family bridge が自動的に存在することにはならない。

```text
related mathematics exists
!= reusable family operation bridge
```

---

# 16. 残存 operation pressure

Phase 115-5 の分類:

```text
H(nu_5)
→ new mathematical inference required

H(sigma_11)
→ related low-dimensional mathematics exists
→ reusable family bridge is not currently present

Delta(sigma_11)
→ reusable concrete / family relation is not currently present

E(nu_prime)
→ expression occurrence exists
→ operation-result relation is not present

Delta(nu_prime)
→ direct / reusable family inference is not currently present

E(nu_5 o eta_8)
→ composition-operation inference boundary
```

これらを Phase 115 の handoff mechanism へ機械的に追加しない。

---

# 17. CLI 境界

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

operation-query 例:

```text
python main.py query "E(nu_5)"
python main.py query-proof "E(nu_5)" --depth 2
python main.py query "E(sigma_11)"
python main.py query-proof "E(sigma_11)" --depth 2
```

---

# 18. Phase 112–115 closure

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

Phase 114:

```text
existing nu-family symbolic bridge
→ exact E(nu_5) concrete specialization
→ operation-query minimal handoff
→ query-proof provenance
```

Phase 115:

```text
post-Phase 114 pressure audit
→ existing mathematics reuse audit
→ exact E(sigma_11) concrete specialization
→ operation-query minimal handoff
→ remaining pressure reclassification
```

Phase 115 focused:

```text
14 passed
```

Phase 114 compatibility:

```text
16 passed
```

関連回帰:

```text
97 passed in 19.14s
```

full regression:

```text
9111 passed in 432.54s (0:07:12)
```

---

# 19. 次 Phase との境界

Phase 116 は Phase 115 の handoff を一般化することから始めない。

まず残存 pressure の優先度を再監査する。

候補:

```text
symbolic scalar LaTeX presentation
H(nu_5) dependency audit
H(sigma_11) dependency audit
Delta(sigma_11) dependency audit
E(nu_prime) / Delta(nu_prime) semantics audit
```

先取りしない:

```text
general E evaluator
general H evaluator
general Delta evaluator
general E(sigma_n) evaluator
arbitrary query-to-inference fallback
four-term composition
three-term map-operation operand
Unicode composition parser
execute sigma_11 expansion
第3 qualified execution family
```
