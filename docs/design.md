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
カタログのメタデータ != 証明事実
探索計画 != 証明結果
計算結果 != 証明事実
表示層 != 証明事実
運用リポジトリの組み立て != 定理事実
探索結果 != 新しい定理事実
証明範囲の走査 != 定理探索
既知関係の発見 != 写像評価
Toda bracket membership の発見 != bracket の解法
適用可能候補 != 証明成功
関連度カテゴリ != 定理順位
候補選択 != 証明成功
handoff 検証 != 定理事実
有界探索結果 != 実行済み証明
実行資格を満たす候補 != 一意な実行対象
実行ファミリーのグループ化 != 生カタログの重複除去
代表候補の選択 != 定理順位付け
性能最適化 != 数学的意味論の変更
```

---

# 2. 現在の主要経路

計算経路:

```text
式 / statement 表現
↓
汎用 proof / inference 機構
↓
Toda 固有の定理知識
↓
ProofRepository / rule catalog
↓
有界証明探索
↓
TodaGroupQuery / lookup
↓
計算 goal の発見 / 復元 / 正規化
↓
群結果
↓
EHP / 完全性の provenance
↓
証明 provenance
↓
構造化表示
↓
人間向け証明レポート
```

generator 探索 / applicability 経路:

```text
generator 文字列
↓
resolve_generator_input()
↓
GeneratorSymbol
↓
標準運用リポジトリ
↓
登録済み結論 / 再帰的 ProofStep ancestry
↓
構造的 occurrence
↓
Toda membership / 既知 map relation
↓
premise pattern compatibility
↓
適用可能候補
↓
rule group / rule family
↓
関連度分類済み表示
```

Phase 104 の handoff / execution:

```text
選択済み適用可能候補
↓
RepositoryGeneratorApplicabilityCandidateHandoff
↓
READY 検証
↓
最終 rule 明示の有界探索
↓
事前構築済み BoundedProducerSearchReport
↓
選択経路の実行
↓
実際の ProofStep provenance
```

Phase 105 の標準運用・実行資格付き経路:

```text
RepositoryGeneratorApplicabilityExplorationResult
↓
実行資格を満たす候補の抽出
↓
実行ファミリーのグループ化
↓
root_entry + source_step の明示選択
↓
代表候補
↓
運用実行オーケストレーション
↓
実際の ProofStep
```

Phase 106 の applicability 性能経路:

```text
generator occurrence を含む scope_node identity 集合
↓
関連する証明範囲だけを構成
↓
既存 applicability finder
↓
既存と同一順序・同一 provenance の候補
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

計算 / provenance:

```text
toda_group_query.py
toda_group_lookup.py
toda_group_result.py
toda_calculation_goal*.py
toda_calculation.py
toda_calculation_result.py
toda_ehp_*.py
toda_proof_dependency.py
toda_explanation.py
```

探索 / applicability:

```text
generator_input.py
repository_element_*.py
repository_proof_scope.py
repository_proof_scope_exploration.py
repository_proof_scope_facade.py
repository_proof_scope_applicability.py
repository_generator_applicability_facade.py
repository_generator_applicability_selection.py
```

実行資格判定 / 実行:

```text
repository_generator_applicability_execution_seed.py
repository_generator_applicability_execution_entry.py
repository_generator_applicability_execution_orchestration.py
repository_generator_qualified_execution_selection.py
repository_generator_qualified_execution_handoff.py
repository_generator_qualified_execution_family.py
repository_generator_qualified_execution_family_selection.py
repository_generator_standard_qualified_execution_facade.py
```

---

# 4. 証明事実とメタデータ

証明事実の中心は次である。

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry.key / phase / theorem` は provenance のメタデータである。

表示、renderer、facade、標準運用リポジトリ、CLI、探索、resolver、証明範囲走査、applicability 分類は、証明事実を追加してはならない。

---

# 5. リポジトリ読み取り専用の不変条件

query / calculation / reporting / exploration / applicability discovery / bounded execution planning は、元のリポジトリを読み取り専用として扱う。

実行は新しい inference result を構成できるが、元の `ProofRepository` 自体を変更しない。

```text
実行前の repository entries == 実行後の repository entries
```

必要な経路では `ProofStep` identity も保持する。

---

# 6. 計算結果の意味論

```text
候補0件  → NOT_FOUND
候補1件  → FOUND
候補2件以上 → MULTIPLE_RESULTS
```

複数候補を暗黙に順位付けしたり、自動選択したりしない。

---

# 7. EHP / 完全性 provenance

根拠は最終的な theorem-backed `ProofStep` から到達可能な ancestry である。

代表例:

$$
\pi_{10}^9
\xrightarrow{\Delta}
\pi_8^4
\xrightarrow{E}
\pi_9^5
\xrightarrow{H}
\pi_9^9
\xrightarrow{\Delta}
\pi_7^4.
$$

---

# 8. Generator input の意味論

`resolve_generator_input()` は明示的なユーザー入力を exact `GeneratorSymbol` へ変換する。

```text
η / eta
ν / nu
σ / sigma
ι / iota

ν′ / ν' / nu' / nu_prime
σ' / sigma_prime
σ'' / sigma_double_prime
σ''' / sigma_triple_prime
```

重要:

```text
添字なし generator != wildcard
```

自由形式の typo correction や数学的同値判定は行わない。

---

# 9. 証明範囲走査の意味論

`RepositoryProofScopeNode`:

```text
root_entry
proof_step
shortest_depth
```

不変条件:

```text
depth 0 = root_entry.step

同じ root 配下の同一 ProofStep identity
= 最短 depth の1 node のみ

異なる root 配下の同一 ProofStep identity
= provenance が異なる別 node

cycle
= 安全に停止
```

---

# 10. Applicability discovery の意味論

候補は概念的に次を保持する。

```text
catalog_entry
premise_index
premise_pattern
source_step
bindings
```

重要:

```text
premise compatibility != 全 premise 成立
適用可能候補 != rule 実行
適用可能候補 != 証明成功
適用可能候補 != 定理事実
```

`RuleRelevanceCategory`:

```text
THEOREM_SPECIFIC
MAP_PROPERTY
STRUCTURAL
GENERIC_RELATION
BRIDGE
UNCLASSIFIED
```

カテゴリ順序は定理順位ではない。

---

# 11. Phase 104 handoff の不変条件

`READY` 検証後の最終 rule は再選択しない。

```text
candidate rule
is validation.execution_entry.rule
is search_result.final_rule
is goal_step.inference_rule
```

事前構築済み report は再生成しない。

```text
execution_result.report
is search_report.report
```

選択された producer も identity を保持する。

```text
producer_node.producer_rule
is executed_producer_step.inference_rule
```

---

# 12. Phase 105 の実行資格判定

Phase 105 は relevance 分類を execution safety とみなさない。

最初に標準運用で実行資格を与えた family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

標準 applicability catalog では、この factory に由来する構造的に同値な3つの clone entry が存在する。

監査結果:

```text
qualified raw candidates = 744
source+rule-name groups = 248
unique source-step identities = 124
```

3つの clone は

```text
同じ factory
同じ rule signature
同じ entry metadata signature
異なる catalog-entry identity
異なる rule identity
```

である。

生の catalog から重複除去せず、実行選択層で family grouping を行う。

---

# 13. 実行ファミリーのグループ化

同一 source 上の構造的に同値な qualified clone candidate を1つの family group にまとめる。

概念的な grouping key:

```text
scope_node identity
source_step identity
qualified family name
premise_index
bindings
```

group は元の候補を全件保持する。

代表候補:

```text
group.representative is group.candidates[0]
```

これは定理順位付けではなく、同一 clone family 内で実行 identity を1つ選ぶ規約である。

---

# 14. Root/source の曖昧性解消

標準 `nu_prime` には248個の execution-family group がある。

```text
standard.toda.prop56  = 14
standard.toda.prop58  = 34
standard.toda.prop511 = 76
standard.toda.prop515 = 124
```

124個の source-step identity はすべて2つの root に現れる。

```text
source-step identity のみ
!= 一意な実行 provenance
```

root だけでも複数 group が残る。

global minimum `shortest_depth = 1` にも6 group が残るため、

```text
shortest_depth
!= 暗黙の選択方針
```

とする。

一方、

```text
root_entry identity
+
source_step identity
```

は全248 group で一意である。

---

# 15. 明示的 family 選択

`RepositoryGeneratorQualifiedExecutionFamilySelection` は、明示された `root_entry` と `source_step` identity を入力として0件または1件の group を返す。

外部の別 graph に属する identity は拒否する。

root の自動優先、depth ranking、group order ranking は行わない。

---

# 16. 標準実行 facade

```text
execute_standard_repository_generator_applicability_result_by_root_and_source(
  applicability_result,
  root_entry,
  source_step,
  goal,
  max_depth=2,
  retry_policy=None,
)
```

この facade は generator 文字列から proof graph を作り直さない。

```text
root_entry / source_step identity
は同一 applicability_result graph に属していなければならない
```

という不変条件を守るためである。

identity chain:

```text
元の applicability_result
→ qualified_selection.applicability_result
→ family_grouping.selection
→ family_selection.grouping
→ representative
→ execution.candidate
```

---

# 17. Phase 106 の性能境界

Phase 106 では、Phase 105 の実行経路を拡張する前に性能と複雑性を監査した。

初期計測:

```text
catalog 構築:
4.44 s / 4.37 MiB

nu_prime applicability exploration:
27.89 s / 274.10 MiB

qualified filtering:
1.11 s / 25.00 MiB

family grouping:
0.025 s / 0.28 MiB

標準実行 facade:
1.09 s / 25.00 MiB
```

主要な圧力は bounded execution ではなく applicability discovery にあった。

詳細監査:

```text
証明範囲 node = 3889
generator occurrence = 626
generator に関係する一意な scope_node = 542

full-scope candidates = 797573
最終 candidates = 176616

compatible references = 797573
match attempts = 797573
successful matches = 797573
```

したがって問題は「大量の失敗 match」ではなく、**generator に無関係な証明範囲も含めて正当な candidate object を大量構築し、その後で捨てていること**だった。

同一 proof graph 上の監査で、generator-relevant scope prefilter は次を完全に保持した。

```text
candidate sequence
candidate multiset
scope_node identity
root_entry identity
source_step identity
catalog_entry identity
rule identity
premise_index
premise_pattern
bindings
```

実装は `_build_generator_applicability_result()` のみを対象とし、既存の finder や Phase 105 execution layer は変更していない。

Phase 106 完了時:

```text
nu_prime applicability exploration:
8.16 s / 62.42 MiB

raw candidates = 176616
qualified candidates = 744
family groups = 248
unique source-step identities = 124
selected family size = 3
execution = True
```

性能改善は**証明事実、候補意味論、provenance identity を変更しない**。

---

# 18. CLI 境界

```text
python main.py 5 7
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

Phase 106 は新しい execution CLI を追加しない。

---

# 19. 現在の未実装境界

```text
自由形式自然言語検索
wildcard family search
一般 composition evaluation
一般 Toda-bracket solving
bracket value computation
一般 coset / indeterminacy computation
一般 E / H / Δ evaluation
既に表現された ancestry を超える recursive theorem solving
未記載数学的帰結の自動列挙
symbolic higher-range auto-instantiation
一般 theorem ranking
producer ranking
proof-cost optimization
best-proof selection
一般 unbounded backtracking
persistent proof cache
repository snapshot / versioning
stale-search-report detection
production root/source の自動選択
全 production-rule family への一般 execution qualification
user-facing execution CLI
Web UI
odd-primary full integration
all-primary ordinary sphere-homotopy calculation
```

---

# 20. 文書 TeX 方針

GitHub Markdown では数式に

```text
行内数式: $...$
独立数式: $$...$$
```

を使用する。

コードや CLI は backtick / code block、数式は数式 delimiter を使う。

---

# 21. 完了基準

Phase 103:

```text
PHASE103_7_CLOSURE_AUDIT = PASS
409 passed in 186.07s
```

Phase 104:

```text
repository-wide after Phase 104-4P closure check:
8644 passed in 374.63s

残存する運用実装は不要
```

Phase 105:

```text
Phase 105-17 focused:
8 passed in 142.33s

Phase 105-7 / 10 / 14 / 16 / 17 related:
40 passed in 174.89s

repository-wide Phase 105 closure:
8709 passed in 659.02s
```

Phase 106:

```text
Phase 106-4 focused:
22 passed in 57.94s

repository-wide Phase 106 closure:
8712 passed in 337.86s

監査内の再実行:
8712 passed in 220.35s
```

正式な Phase 106 closure の基準値は、独立実行した `337.86s` を採用する。

Phase 106 は完了。

---

# 22. 次 Phase との境界

Phase 107-1 は、Phase 106 で性能問題を閉じた後の **qualified-execution expansion pressure audit** とする。

最初から複数 family を実装しない。

監査対象は次である。

```text
複数 production rule family への qualification 拡張が本当に必要か
user-facing workflow で root/source をどう指定するか
goal の明示入力を維持するか
goal discovery が必要か
execution CLI が必要か
execution result と表示層の接続が必要か
```

Phase 107 は性能最適化の続きではなく、実際の利用圧力に基づいて実行経路を広げるかどうかを判断する段階である。
