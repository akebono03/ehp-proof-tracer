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

## 安定 stem $G_0$ から $G_7$

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

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
$$

## Phase 103

`docs/proof_records/applicable_theorem_relevance_103.md`

```text
適用候補 != 証明成功
関連度カテゴリ != 定理事実
表示順 != 定理順位付け
```

## Phase 104

選択候補を READY 検証、明示的 final rule による有界探索、事前構築済み report の実行へ接続。

```text
8644 passed in 374.63s
```

## Phase 105

最初の標準 qualified family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

```text
8709 passed in 659.02s
```

## Phase 106

`docs/proof_records/performance_applicability_106.md`

```text
797573 全 scope 候補
→ 176616 生成元関連候補

8.16 s / 62.42 MiB
8712 passed in 337.86s
```

## Phase 107 multi-family qualified execution provenance

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

第2 family は既存の

$$
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
$$

を導く2前提 production rule である。

複数前提候補から companion premise を任意探索せず、同じ root / rule / goal / source identity を満たす既存 production application を一意に recovery する。

```text
8783 passed in 290.63s
```

Phase 107 は完了。

## Phase 108 利用者向け実行 provenance

新しい数学的定理事実は追加していない。

```text
生成元入力
→ 実行可能対象の解決
→ 曖昧性に安全な候補選択
→ qualified execution
→ 実行済み goal_step
→ 結果 + 証明
```

```text
候補番号 != 定理順位付け
```

```text
8850 passed in 380.25s
```

Phase 108 は完了。

## Phase 109 既知群同一性 / 証明再生 provenance

新しい独立した数学的定理 root は追加していない。

Toda Proposition 5.15:

$$
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
$$

具体 integer index $n\ge 10$ に対して定理固有の具体化を導入。

例:

$$
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\},
\qquad
\pi_{19}^{12}=\mathbb Z/16\{\sigma_{12}\}.
$$

```text
concrete specialization
→ symbolic Proposition 5.15 higher step
```

known-group proof replay:

```text
generator
→ unique 既知群同一性 node
→ existing ProofStep
→ bounded ancestry
→ 表示
```

```text
show-proof != execute
```

```text
8998 passed in 493.70s (0:08:13)
```

Phase 109 は完了。

## Phase 110 operation query / 証明再生 provenance

Phase 110 は新しい数学的定理事実を追加していない。

既存 repository / proof-scope に存在する relation・map statement・composition を利用者向け query から検索し、既存 `ProofStep` provenance を保持したまま表示・replay する経路を追加した。

最小文法:

```text
H(<operand>)
E(<operand>)
Delta(<operand>)
<generator> o <generator>
```

代表結果:

$$
H(\nu')=\eta_5,
\qquad
H(\nu')=E^2\eta_3,
$$

$$
\Delta(\iota_9)
=
\pm(2\nu_4-E\nu'),
$$

$$
E\eta_2\nu'=0.
$$

```text
検索 != 推論 != evaluator
```

raw lookup occurrence は削除せず、表示 layer のみ同一 statement を grouping する。

```text
deduplicated 表示
!= provenance deletion
```

`query-proof` は selected fact の `ProofStep` を replay root とする。

```text
operation-query 証明再生
!= repository theorem replay
```

unknown aggregate statement は安全な type-name fallback を使う。

```text
9055 passed in 455.09s (0:07:35)
```

Phase 110 は完了。

## Phase 111 CLI capability / user pressure audit

Phase 111 は新しい数学的定理事実を追加していない。

既存 CLI capability を利用者視点で監査し、実際に確認された usability pressure だけを最小実装した。

### Global CLI discoverability

主要コマンドを global help から発見可能にした。

`n,k` は project quantity

$$
\pi_{n+k}^{n}
$$

すなわち free part + 2-primary component と明示し、通常の all-primary sphere homotopy group と混同しないようにした。

### Symbolic dimension presentation

Toda group の symbolic dimension で Python AST repr が露出する問題を修正。

$$
\pi_{n+7}^{n}
$$

のように表示する。

これは数学的定理事実の追加ではなく presentation 修正である。

### Three-term composition query

実際に repository に存在する

$$
\eta_2\circ(\nu'\circ\eta_6)
$$

への問い合わせ需要に対して、

```text
eta_2 o nu_prime o eta_6
```

を top-level query として追加した。

代表既存 fact:

$$
\pi_7^2
=
\mathbb Z/2\{\eta_2\nu'\eta_6\},
$$

$$
E\eta_2\nu'\eta_6=0.
$$

この対応は既存 proof fact lookup であり、新しい演算 evaluator ではない。

```text
3-term query
!= new theorem
!= composition evaluation
```

### Replay depth exposure

既存 replay API の `max_depth` を CLI `--depth` として公開。

```text
show-proof --depth N
query-proof --depth N
```

`--depth` は既存 ancestry の可視範囲を変えるだけであり、新しい proof search を行わない。

### Deep replay safe fallback

深い `show-proof` で unsupported aggregate statement の raw dataclass repr が漏れる問題を修正。

例:

```text
`Toda45IsomorphismStatement`
`TodaSigmaFamilyDefinitionStatement`
```

既に数式表示可能な

$$
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\},
$$

$$
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
$$

$$
\pi_{16}^{9}=\mathbb Z/16\{\sigma_9\}
$$

は維持した。

```text
safe fallback
!= 推測した数学的説明
```

### Phase 111 完了

repository 全体:

```text
9074 passed in 446.27s (0:07:26)
```

whitespace:

```text
git diff --check
clean
```

Phase 111 は完了。

## Phase 112 operation / workflow capability audit

Phase 112 は新しい数学的定理事実を追加していない。

代表元:

```text
nu_prime
nu_5
sigma_11
```

を用いて、次の end-to-end 経路を監査した。

```text
known group
→ proof replay
→ operation query
→ query-proof
→ applicable theorem exploration
→ execute
```

重要な分類:

```text
parser boundary
repository lookup miss
existing inference / specialization handoff gap
workflow orchestration gap
possible new inference / evaluator gap
```

### `nu_prime`

既存 fact:

$$
H(\nu')=\eta_5,
$$

$$
E(\eta_2\nu')=0.
$$

`E(nu_prime)` と `Delta(nu_prime)` は lookup miss。

### `nu_5`

既存 fact:

$$
\Delta(\nu_5)=\pm(\eta_2\nu').
$$

また既存 proof infrastructure には $\nu$-family stable transport があり、

$$
E^{n-5}\nu_5=\nu_n
$$

を表現している。

したがって $n=6$ では数学的に

$$
E(\nu_5)=\nu_6.
$$

Phase 112 時点では `query` がその symbolic inference を起動せず lookup で停止していた。

このため、

```text
LOOKUP_MISS != evaluator required
```

という境界を確認した。

### `sigma_11`

known-group proof replay は

$$
\pi_{18}^{11}
=
\mathbb Z/16\{\sigma_{11}\}
$$

を再生できた。

一方、Phase 112 時点の

```text
python main.py 11 7
```

は同じ既存 specialization を利用できなかった。

これは新しい数学の不足ではなく、

```text
generator-side theorem-specific specialization
→ TodaGroupQuery orchestration 未接続
```

という workflow gap と分類した。

### Phase 112 結論

一般 parser や一般 $E/H/\Delta$ evaluator を先に作らず、既存 capability の未接続箇所を優先する方針を確定した。

## Phase 113 TodaGroupQuery / $\sigma_n$ specialization provenance

Phase 113 は新しい数学的定理 root を追加していない。

既存 symbolic Proposition 5.15:

$$
\pi_{n+7}^{n}
=
\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9
$$

から、既存 theorem-specific concrete specialization を `TodaGroupQuery` 経路で再利用するようにした。

対象:

```text
k = 7
n >= 10
```

例:

$$
\pi_{17}^{10}
=
\mathbb Z/16\{\sigma_{10}\},
$$

$$
\pi_{18}^{11}
=
\mathbb Z/16\{\sigma_{11}\},
$$

$$
\pi_{19}^{12}
=
\mathbb Z/16\{\sigma_{12}\}.
$$

provenance:

```text
concrete TodaGroupQuery result
→ specialized ProofStep
→ symbolic Proposition 5.15 higher step
→ existing Proposition 5.15 ancestry
```

重要:

```text
specialized result
!= new independent theorem root

TodaGroupQuery fallback
!= arbitrary AST specialization

empty repository
→ NOT_FOUND

repository roots
→ unchanged
```

Phase 113 によって、

```text
python main.py show-proof sigma_11
```

と

```text
python main.py 11 7
```

の間にあった既存 theorem capability の不一致を解消した。

focused tests:

```text
7 + 26 + 10 + 5 + 5 = 53 passed
```

full regression:

```text
9081 passed in 434.58s (0:07:14)
```

Phase 113 は完了。

## Phase 114 `E(nu_5)` existing-inference handoff provenance

Phase 114 は新しい独立 theorem root や general operation evaluator を追加していない。

既存 Toda Proposition 5.6 の symbolic bridge:

$$
E^{n-5}\nu_5=\nu_n,
\qquad n\ge 6
$$

を再利用する。

$n=6$ に限定して、

$$
E(\nu_5)=\nu_6
$$

を concrete `ProofStep` として構成する。

provenance:

```text
concrete E(nu_5) = nu_6 step
→ symbolic E^(n-5)nu_5 = nu_n bridge
→ nu_5 definition
→ nu_n definition
→ n >= 6
```

concrete step の rule は inference であり、direct premise は existing symbolic bridge である。

したがって:

```text
concrete specialization
!= new theorem root
!= general E evaluator
!= arbitrary symbolic substitution
```

operation-query handoff:

```text
query
→ direct lookup
→ direct hit なら既存結果
→ miss
→ exact E(nu_5) guard
→ concrete specialization
→ query / query-proof
```

重要な boundary:

```text
direct lookup has priority
H(nu_5) は対象外
Delta(nu_5) は対象外
E(nu_6) は対象外
E(sigma_11) は対象外
E(nu_5 o eta_8) は対象外
三項 map-operation operand は対象外
四項 composition は対象外
repository roots は変更しない
```

query-proof は concrete fact 自身の `ProofStep` を root とし、既存 symbolic bridge を ancestry として再生する。

focused boundary tests:

```text
16 passed
```

Phase 110 / 111 / 114 関連回帰:

```text
60 passed
```

full regression:

```text
9097 passed in 449.47s (0:07:29)
```

Phase 114 は完了。

## Phase 115 `E(sigma_11)` existing-mathematics handoff provenance

Phase 115 は新しい独立 theorem root や general operation evaluator を追加していない。

既存 Toda Lemma 5.14 の $\sigma$-family definition:

$$
\sigma_n=E^{n-8}\sigma_8,
\qquad n\ge 8
$$

を再利用する。

具体的には、

$$
\sigma_{11}=E^3\sigma_8,
\qquad
\sigma_{12}=E^4\sigma_8
$$

を同じ `sigma8_statement` provenance から構成し、

$$
E(\sigma_{11})=\sigma_{12}
$$

を operation-query 用 concrete `Relation` として生成する。

provenance:

```text
concrete E(sigma_11) = sigma_12 step
→ symbolic TodaSigmaFamilyDefinitionStatement
→ TodaLemma514Sigma8Statement
→ ScalarGreaterEqualStatement
```

concrete step の rule は inference であり、direct premise は existing symbolic $\sigma$-family definition である。

したがって:

```text
concrete definitional specialization
!= new theorem root
!= general E(sigma_n) evaluator
!= general E evaluator
!= arbitrary symbolic substitution
```

operation-query handoff:

```text
query
→ direct lookup
→ direct hit なら既存結果
→ miss
→ exact E(sigma_11) guard
→ concrete specialization
→ query / query-proof
```

CLI で確認した結果:

$$
E\sigma_{11}=\sigma_{12}.
$$

`query-proof "E(sigma_11)" --depth 2` は、

```text
Depth 0:
E sigma_11 = sigma_12

Depth 1:
TodaSigmaFamilyDefinitionStatement

Depth 2:
TodaLemma514Sigma8Statement
ScalarGreaterEqualStatement
```

を再生する。

重要な boundary:

```text
direct lookup has priority
E(sigma_10) は対象外
E(sigma_12) は対象外
E(sigma_100) は対象外
H(sigma_11) は対象外
Delta(sigma_11) は対象外
E(sigma_11 o eta_18) は対象外
repository roots は変更しない
parser grammar は変更しない
```

Phase 115-5 では残存 pressure を次のように再分類した。

```text
H(nu_5)
→ new mathematical inference required

H(sigma_11)
→ related low-dimensional mathematics exists
→ reusable family operation bridge is not currently present

Delta(sigma_11)
→ reusable concrete / family relation is not currently present

E(nu_prime)
→ E nu_prime appears as a subexpression
→ operation-result relation is not present

Delta(nu_prime)
→ direct / reusable family inference is not currently present

E(nu_5 o eta_8)
→ composition-operation inference boundary
```

したがって Phase 115 は exact `E(sigma_11)` handoff で停止した。

focused:

```text
Phase 115 dedicated:
14 passed

Phase 114 compatibility:
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

Phase 115 は完了。

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
関連度カテゴリ != 定理事実
candidate ordering != 定理順位付け
引き渡し検証 != 定理事実
有界探索 report != 実行済み証明
qualified 候補 != 一意な実行対象
production-application recovery != 新しい定理事実
family dispatch != 定理順位付け
性能最適化 != 定理事実
user-facing resolver != 定理順位付け
候補番号 != theorem priority
CLI 表示 != 新しい定理事実
既知群同一性 lookup != qualified execution
symbolic 具体化 != 任意の AST 書き換え
known-group 証明再生 != theorem application execution
show-proof != execute
operation-query 検索 != evaluator
operation-query 結果 != 新しい定理事実
deduplicated 表示 != provenance deletion
表示順 != 定理順位付け
query-proof fact number != theorem priority
query-proof replay != enclosing theorem replay
--depth != new proof search
three-term query != composition evaluator
safe type-name fallback != 推測した定理 branch
LOOKUP_MISS != evaluator required
TodaGroupQuery specialization reuse != new theorem
limited operation handoff != general query inference
theorem-specific concrete specialization != general evaluator
expression occurrence != operation result relation
related mathematics exists != reusable operation bridge
```

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。
