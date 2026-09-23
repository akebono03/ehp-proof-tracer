# EHP Proof Tracer 開発記録

この文書は開発履歴の索引である。

現在の仕様・設計は `README.md` と `docs/design.md` を優先する。
今後の計画は `docs/roadmap.md`、代表的な数学的証明・証明基盤の記録は `docs/proof_records.md` を参照する。

過去の詳細な開発記録は、内容を削除せず `docs/development_log/` 以下へ分割して保存する。

---

# 開発履歴アーカイブ

## Phase 1–48

`docs/development_log/phases_001_048.md`

可換群計算、汎用推論、EHP、Toda の基礎表現から Proposition 4.4 周辺まで。

## Phase 49–64

`docs/development_log/phases_049_064.md`

\(\pi_3^2\)、\(\pi_4^3\)、Toda Proposition 5.1、Lemma 5.2、\(\nu'\)、\(\nu_4\)、\(\nu\)-family、性能安定化まで。

## Phase 65–78

`docs/development_log/phases_065_078.md`

Toda Proposition 5.6 から Lemma 5.16、安定 \(G_0\) から \(G_7\) までの主要な数学的証明経路。

## Phase 79–89

`docs/development_log/phases_079_089.md`

証明 Repository、repository 支援推論、自動規則選択、有界 producer 探索、診断、depth パラメータ化、有限 retry、具体的定理 instance 適合性まで。

## Phase 90–95

`docs/development_log/phases_090_095.md`

Toda 群問い合わせ、正規化済み群結果、EHP provenance、flat / recursive 証明 provenance、計算オーケストレーションの記録。

## Phase 96–111

```text
Phase 96:
構造化表示 / 読みやすい完全証明レポート

Phase 97:
計算からレポートまでのオーケストレーション

Phase 98:
生の n,k 入力用簡易 facade

Phase 99:
生成元中心 repository 探索

Phase 100:
標準運用 repository / build_standard_toda_report / main.py n k

Phase 101:
標準 repository と generator explore

Phase 102:
再帰的 proof-scope 探索

Phase 103:
適用可能定理 / 補題探索と関連度分類

Phase 104:
候補 → READY → bounded search → execution

Phase 105:
第1 qualified production family

Phase 106:
applicability performance audit

Phase 107:
multi-family qualified execution

Phase 108:
user-facing execute workflow / CLI

Phase 109:
known-group identity / indexed sigma / show-proof

Phase 110:
operation query / query-proof

Phase 111:
CLI audit / 3-term query / --depth / safe fallback
```

代表 regression:

```text
Phase 108:
8850 passed in 380.25s

Phase 109:
8998 passed in 493.70s

Phase 110:
9055 passed in 455.09s

Phase 111:
9074 passed in 446.27s
```

---

# 現在の運用方針

`development_log.md` は索引として維持する。

詳細な新規開発記録は archive file に追記するか、Phase 範囲に応じて新しい archive file を追加する。

既存履歴は原則として削除せず、誤りが確定した場合のみ必要な訂正を行う。

## Phase 112

実際の数学的 workflow で capability pressure を監査。

```text
LOOKUP_MISS != evaluator required
```

を重要境界として確認し、`sigma_11` group-query orchestration gap を Phase 113 の対象に選定。

## Phase 113

既存 indexed \(\sigma_n\) specialization を `TodaGroupQuery` 経路へ最小接続。

```text
9081 passed in 434.58s (0:07:14)
```

## Phase 114

既存 Toda Proposition 5.6 を再利用し、

\[
E(\nu_5)=\nu_6
\]

を exact handoff として operation query へ接続。

```text
9097 passed in 449.47s (0:07:29)
```

## Phase 115

既存 Toda Lemma 5.14 の \(\sigma\)-family definition を再利用し、

\[
E(\sigma_{11})=\sigma_{12}
\]

を exact handoff として接続。

```text
9111 passed in 432.54s (0:07:12)
```

## Phase 116

TeX-capable Web UI の readiness audit。

```text
Flask
KaTeX
thin Web adapter
structured presentation reuse
CLI output / Markdown は再解析しない
```

## Phase 117

最小 group-query Web UI を実装し、KaTeX 表示を確認。

## Phase 118

operation query / query-proof を Web UI へ接続。

```text
9169 passed in 465.97s (0:07:45)
```

## Phase 119

次の Web capability を監査し、`show-proof` を選定。

## Phase 120

known-group `show-proof` を Web UI へ接続。

```text
9184 passed in 453.04s (0:07:33)
```

## Phase 121

`explore` を read-only direct generator exploration として Web UI へ接続。

```text
nu_prime
→ Occurrences: 6

sigma_11
→ Occurrences: 0

eta_999
→ Occurrences: 0
```

```text
9197 passed in 455.68s (0:07:35)
```

## Phase 122

`explore-proof` を既存 recursive proof-scope semantics のまま Web UI へ接続。

```text
9212 passed in 455.16s (0:07:35)
```

## Phase 123

残っていた read-only Web capability `explore-applicable` を compact Web surface として接続。

`nu_prime`:

```text
Proof-scope occurrences: 626
Applicability candidates: 176616
Source statements with candidates: 542
Rule groups: 123300
Rule families: 29308
```

browser 描画量のみ制限:

```text
各 category 先頭 5 source
各 displayed source 先頭 10 rule family
details 初期折りたたみ
全 summary count 維持
```

focused:

```text
13 passed in 61.24s
17 passed in 69.57s
```

final:

```text
9229 passed in 509.16s (0:08:29)
```

Phase 123 は完了。

## Phase 124

`execute` を直ちに Web 化する前に current single-page Web UI と既存 user execution workflow を監査。

UI organization を先に選定し、workflow navigation を追加。

```text
Calculation and queries
Proof and exploration
Applicability
```

Phase 124 では execute / candidate selection を追加しなかった。

focused:

```text
5 passed in 3.83s
38 passed in 44.51s
```

final:

```text
9234 passed in 522.10s (0:08:42)
```

Phase 124 は完了。

## Phase 125

Phase 125 は既存 `execute` workflow を current single-page Web UI へ接続した。

新しい数学的 theorem、proof-search rule、qualified execution family、operation-query grammar、candidate-ranking semantics は追加していない。

### Phase 125-1: current execute workflow audit

確認対象:

```text
repository_generator_user_execution_facade.py
repository_generator_user_execution_candidate_presentation.py
repository_generator_user_execution_presentation.py
repository_generator_user_execution_handoff.py
repository_generator_user_execution_proof_step.py
main.py execute
Phase 108 execute tests
web_app.py
templates/index.html
```

確認結果:

```text
NONE
AMBIGUOUS
EXECUTED
```

が既に structured workflow status として存在。

candidate list、qualified execution、executed `ProofStep`、result + proof presentation も既存実装を再利用可能と判断。

### Phase 125-2: Web integration scope freeze

対象:

```text
generator
→ executable candidates
→ candidate selection
→ execution
→ Result + Proof
```

境界:

```text
AMBIGUOUS
→ candidate list
→ auto-select しない

NONE
→ normal no-target result

one target
→ existing facade の挙動どおり実行
```

対象外:

```text
new qualified family
candidate ranking
general proof search
general E/H/Delta evaluator
```

### Phase 125-3: thin Web adapter design

新規 Web adapter は existing facade / presentation の structured object のみを利用。

```text
Web input
→ existing execution facade
→ structured workflow result
→ Web view
```

CLI Markdown は解析しない。

### Phase 125-4: minimal implementation + focused tests

追加:

```text
web_generator_execution.py
tests/test_phase125_4_web_generator_execution.py
```

変更:

```text
web_app.py
templates/index.html
tests/test_phase124_4_web_workflow_navigation.py
```

focused regression:

```text
14 passed in 29.80s
```

### Phase 125-5: browser/manual audit

`nu_prime`:

```text
AMBIGUOUS
→ 2 executable candidates
```

候補:

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\},
\]

\[
\Delta(\iota_9)=\pm(2\nu_4-E\nu').
\]

candidate 1 / 2 は既存 CLI と一致。

`eta_999`:

```text
No executable target found for this generator.
```

`nu_5`:

Phase 125 時点では Web result が一見 generator-centered でないため CLI と比較した。

```text
python main.py execute nu_5
```

も Web と同じ

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
\]

を返したため、Phase 125 の Web adapter mismatch ではなく existing target-resolution semantics の結果として Phase 126 監査へ送った。

この挙動は Phase 126 で semantic leak と確認され、現在は修正済みである。

KaTeX と既存 Group / Query / Proof / Explore / Applicability との共存も確認。

### Phase 125-final: documentation / completion

repository-wide regression:

```text
python -m pytest -q
9243 passed in 555.37s (0:09:15)
```

Phase 125 は完了。

## Phase 126

Phase 125 の `nu_5` 実行結果を起点に、executable-target resolution semantics を監査し、必要な最小修正を行った。

### Phase 126-1: resolver tracing

現行経路:

```text
generator input
→ proof-scope occurrences
→ applicability candidates
→ qualified selection
→ execution-family grouping
→ matching target step
→ executable target
```

を追跡。

旧 resolver は generator occurrence が source `ProofStep` のどの component にあるかを executable target inclusion で確認していなかった。

### Phase 126-2: semantics boundary

次の3層を区別する方針を確定。

```text
proof-scope relevance
→ generator が ProofStep のどこかに出現

applicability relevance
→ その ProofStep が rule premise として適用可能

executable relevance
→ generator occurrence が rule が実際に利用する source component に対応
```

`proof-scope relevance` と `applicability relevance` は broad のまま維持し、execute 境界だけを狭める方針とした。

### Phase 126-3: representative comparison

比較:

```text
nu_prime
nu_5
sigma_11
```

`nu_prime` は qualified rule が利用する component に対応する occurrence を持つ。

`nu_5` は Toda Proposition 5.6 aggregate 内の

```text
pi8_5_group_relation
```

に occurrence を持つが、第2 qualified family が利用するのは

```text
pi6_3_group_relation
```

である。

`sigma_11` は proof-scope / applicability があっても admitted qualified execution family がなく、既存どおり `NONE`。

### Phase 126-4: minimal executable relevance guard

変更:

```text
repository_generator_user_execution_resolver.py
```

追加:

```text
tests/test_phase126_executable_target_relevance.py
```

第2 qualified family

```text
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

に対してのみ、source-step identity と occurrence path の先頭 branch

```text
pi6_3_group_relation
```

を executable relevance guard として確認するようにした。

第1 qualified family

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

は aggregate Prop. 5.6 ではなく独立した \(\pi_7^4\) relation を直接 source とするため、追加 branch guard は入れていない。

focused regression:

```text
13 passed in 14.86s
```

### Phase 126 CLI audit

```text
python main.py execute nu_prime
```

結果:

```text
2 executable candidates
```

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\},
\]

\[
\Delta(\iota_9)=\pm(2\nu_4-E\nu').
\]

```text
python main.py execute nu_5
→ No executable target found for nu_5.

python main.py execute sigma_11
→ No executable target found for sigma_11.
```

### Phase 126-final: completion

repository-wide regression:

```text
python -m pytest -q
9246 passed in 556.62s (0:09:16)
```

Phase 126 は完了。

確定境界:

```text
proof-scope relevance != executable relevance
applicability relevance != executable relevance
aggregate statement の同居 != executable source relevance
executable relevance filtering != theorem ranking
candidate number != theorem priority
nu_prime の2 targetを維持
nu_5 → pi6_2 を除外
sigma_11 → NONE を維持
```

## Phase 127

Phase 126 後にすぐ新機能を追加せず、post-Phase 126 capability priority audit を実施した。

### Phase 127-1: current capability re-audit

対象:

```text
n k
query / query-proof
show-proof
explore
explore-proof
explore-applicable
execute
Web UI
```

既存利用経路は接続済みであり、次の具体的 pressure は operation query の残件と判断。

### Phase 127-2: remaining mathematical pressure

監査対象:

```text
H(nu_5)
H(sigma_11)
Delta(sigma_11)
E(nu_prime)
Delta(nu_prime)
E(nu_5 o eta_8)
```

いずれも direct query では `No known repository fact found` だった。

### Phase 127-3A: `H(nu_5)`

Phase 68 の Hopf-zero machinery は \(\pi_9^5\) を source とするため、`H(nu_5)` ではなく \(\nu_5\eta_8\) 側の事実に対応することを確認。

`H(nu_5)` の element-level proof は既存 repository にないため DEFER。

### Phase 127-3B: `E(nu_5 o eta_8)`

既存 provenance:

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\]

\[
\pi_{10}^6=0.
\]

結果 semantics が

\[
E(\nu_5\eta_8)=0
\]

と明確で、parser も既に二項 composition operand に対応しているため KEEP。

### Phase 127-3C: `E(nu_prime)` / `Delta(nu_prime)`

`E\nu'` は既に

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}
\]

の generator として存在する。

ただし `E(nu_prime)` に何を operation result として返すかは意味論整理が必要なため KEEP。

`Delta(nu_prime)` は element-level Delta proof が不足するため DEFER。

### Phase 127-3D: `H(sigma_11)` / `Delta(sigma_11)`

\(\sigma_8\) の Hopf relation や \(\sigma\)-chain の Delta machinery はあるが、`sigma_11` を入力とする element-level H / Delta proof はないため両方 DEFER。

### Phase 127-4: 次の1機能の選定

比較対象を

```text
E(nu_prime)
E(nu_5 o eta_8)
```

に絞った。

`E(nu_prime)` は user-facing result semantics の監査が必要。

`E(nu_5 o eta_8)` は existing source / target-zero provenance と current `RelationType.ZERO` semantics がそのまま使える。

そのため Phase 128 は

\[
E(\nu_5\eta_8)=0
\]

の theorem-specific handoff を1機能だけ実装することに決定。

## Phase 128

### Phase 128-1: 実装前監査

変更範囲を次に固定。

```text
新規:
repository_nu5_eta8_suspension_zero_specialization.py
tests/test_phase128_nu5_eta8_operation_query_handoff.py

変更:
repository_operation_query_facade.py
tests/test_phase114_3_nu5_operation_query_handoff.py
```

parser、direct lookup、presentation、proof replay、Web adapter は変更不要と確認。

根拠 provenance は Toda Proposition 5.8 の

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\]

および derived

\[
\pi_{10}^6=0
\]

を再利用する方針に固定。

### Phase 128-2: theorem-specific handoff 実装

追加した handoff:

```text
E(nu_5 o eta_8)
→ direct lookup miss
→ exact query guard
→ existing Prop.5.8 proof-scope
→ specialized E(nu_5 eta_8)=0 ProofStep
```

specialized root:

\[
E(\nu_5\eta_8)=0.
\]

直接 premise:

\[
\pi_{10}^6=0.
\]

その下の既存 premise:

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\]

\[
E:\pi_9^5\to\pi_{10}^6
\text{ is surjective},
\]

\[
\nu_6\eta_9=0.
\]

最初の focused test では、同じ Prop.5.8 proof ancestry が複数 repository root から見えるため同一 specialized match が複数生成されることを検出。

Phase 128-2b で、

```text
root_entry.key == standard.toda.prop58
```

へ theorem-specific に限定し、同一 specialized conclusion を dedup。

これは theorem ranking ではなく、今回の handoff が再利用する正規 provenance root の固定である。

focused regression:

```text
40 passed in 15.43s
```

### Phase 128 manual audit

```text
python main.py query "E(nu_5 o eta_8)"
```

結果:

\[
E(\nu_5\eta_8)=0.
\]

first provenance:

```text
Toda Proposition 5.8
Phase 68
depth 3
```

```text
python main.py query-proof "E(nu_5 o eta_8)" --depth 2
```

で specialized root と既存 Prop.5.8 ancestry を確認。

### Phase 128-final: completion

repository-wide regression:

```text
python -m pytest -q
9256 passed in 570.10s (0:09:30)
```

Phase 128 は完了。

確定境界:

```text
direct lookup first
exact query guard
standard.toda.prop58 provenance
repository 非破壊
query-proof replay
existing E(nu_5) / E(sigma_11) handoff 維持
parser 変更なし
general E evaluator なし
general target-zero evaluator なし
new theorem root なし
new qualified execution family なし
ranking なし
```

次 Phase 129 は `E(nu_prime)` の operation-result semantics を audit first で扱う。

## Phase 129

### Phase 129-1: representation / provenance 再監査

`E(nu_prime)` の direct lookup は miss する一方、既存 Toda Proposition 5.6 には

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}
\]

が保持されていることを確認した。

`E\nu'` は独立した element-level equality としてではなく、第2 cyclic summand の generator として表現されている。

### Phase 129-2: operation-result semantics 決定

候補:

```text
E(nu') = E nu'
E nu' in pi_7^4
pi_7^4 decomposition
```

を比較し、user-facing result は

\[
E\nu' \in \pi_7^4
\]

と決定した。

`E(\nu')=E\nu'` は表記上の自己同一視であり採用しない。

また、group relation 内の arbitrary containment を operation result とする一般規則には広げない。

### Phase 129-3: 最小 handoff 実装前監査

実装境界:

```text
exact E(nu_prime) guard
specific Proposition 5.6 decomposition shape
membership ProofStep
existing decomposition ProofStep as direct premise
repository non-mutation
```

対象外:

```text
general E evaluator
general membership evaluator
recursive arbitrary containment
parser expansion
new theorem root
new qualified execution family
ranking
```

### Phase 129-4: 最小実装

追加:

```text
repository_nu_prime_suspension_membership_specialization.py
tests/test_phase129_nu_prime_operation_query_handoff.py
```

変更:

```text
repository_operation_query_facade.py
repository_operation_query_lookup.py
```

`repository_operation_query_lookup.py` は direct lookup ロジックを変更せず、

```text
RepositoryOperationQueryMatchKind.GROUP_MEMBERSHIP
```

を追加した。

specialized result:

\[
E\nu' \in \pi_7^4.
\]

直接 premise:

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}.
\]

focused:

```text
12 passed in 6.28s
```

関連 regression:

```text
63 passed in 12.54s
```

manual:

```text
python main.py query "E(nu_prime)"
→ E nu' in pi_7^4
→ First provenance: Toda Proposition 5.6, Phase 65

python main.py query-proof "E(nu_prime)" --depth 1
→ Depth 0: E nu' in pi_7^4
→ Depth 1: pi_7^4 = Z{nu_4} ⊕ Z/4{E nu'}
```

### Phase 129-5: documentation / completion audit

旧文書に残っていた

```text
E(nu_prime) → future semantics audit
```

を完了状態へ更新した。

確定境界:

```text
membership result
theorem-specific handoff
Proposition 5.6 provenance
direct lookup unchanged
repository non-mutation
general E evaluator なし
general membership evaluator なし
arbitrary containment なし
parser expansion なし
```

repository-wide regression:

```text
python -m pytest -q
9268 passed in 569.71s (0:09:29)
```

Phase 129 は完了。

次は Phase 130 で current capability pressure を再監査する。
