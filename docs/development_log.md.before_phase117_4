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

$\pi_3^2$、$\pi_4^3$、Toda Proposition 5.1、Lemma 5.2、$\nu'$、$\nu_4$、$\nu$-family、性能安定化まで。

## Phase 65–78

`docs/development_log/phases_065_078.md`

Toda Proposition 5.6 から Lemma 5.16、安定 $G_0$ から $G_7$ までの主要な数学的証明経路。

## Phase 79–89

`docs/development_log/phases_079_089.md`

証明 Repository、repository 支援推論、自動規則選択、有界 producer 探索、診断、depth パラメータ化、有限 retry、具体的定理 instance 適合性まで。

## Phase 90–95

`docs/development_log/phases_090_095.md`

Toda 群問い合わせ、正規化済み群結果、EHP provenance、flat / recursive 証明 provenance、計算オーケストレーションの記録。

## Phase 96–98

```text
Phase 96:
構造化表示 / 読みやすい完全証明レポート
7609 passed in 121.63s

Phase 97:
計算からレポートまでのオーケストレーション
7609 passed in 121.63s

Phase 98:
生の n,k 入力用簡易 facade
7643 passed in 123.73s
```

詳細:

```text
docs/development_log/phases_096.md
docs/development_log/phases_097.md
docs/development_log/phases_098.md
```

## Phase 99

生成元中心の repository 探索を追加。

```text
GeneratorSymbol
→ 出現
→ 意味論的役割
→ グループ化表示
→ Markdown
→ 一括探索 facade
```

```text
7824 passed in 136.59s
```

## Phase 100

標準運用 repository、`build_standard_toda_report(n,k)`、`python main.py n k` を統合。

```text
8010 passed in 179.65s
```

## Phase 101

`docs/development_log/phases_101.md`

生成元中心の探索を標準 repository と `main.py explore` へ接続。

```text
8058 passed in 133.01s
```

## Phase 102

`docs/development_log/phases_102.md`

再帰的 proof-scope 探索、Toda membership、既知の写像関係探索を追加。

代表結果:

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
$$

```text
8142 passed in 129.93s
```

## Phase 103

`docs/development_log/phases_103.md`

適用可能な定理 / 補題の探索と関連度分類を追加。

```text
409 passed in 186.07s
```

## Phase 104

選択された適用候補を READY 検証、明示的 final rule による有界探索、事前構築済み report の実行へ接続。

```text
8644 passed in 374.63s
```

## Phase 105

第1 qualified production family を標準 applicability workflow へ接続。

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

```text
8709 passed in 659.02s
```

## Phase 106

`docs/development_log/phases_106.md`

適用可能性の性能 / 複雑性監査。

```text
797573 全 scope 候補
→ 176616 生成元関連候補
```

生成元関連 scope prefilter を実装。

```text
8.16 s / 62.42 MiB
8712 passed in 337.86s
```

## Phase 107

`docs/development_log/phases_107.md`

第1 family 限定実行を multi-family 実行へ拡張。

第2 qualified family:

```text
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

主要機能:

```text
正確な production application recovery
NONE / UNIQUE / AMBIGUOUS recovery 状態
正確な複数前提 seed
2前提有界実行の統合
明示的 root + source + family 選択
一般 qualified-family admission
family 名 dispatch
multi-family 標準 facade
```

repository 全体:

```text
8783 passed in 290.63s
```

Phase 107 は完了。

## Phase 108

Phase 107 の内部 qualified execution を利用者向け workflow と CLI へ接続。

主要機能:

```text
生成元入力
→ 実行可能対象の解決
→ 曖昧性処理
→ 候補一覧
→ 候補選択
→ qualified execution
→ 最終実行済み ProofStep
→ 結果 + 証明表示
→ CLI
```

CLI:

```text
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
```

Windows CP932 boundary を実 subprocess smoke で検出し、script entry point の stdout / stderr を UTF-8 化した。

repository 全体:

```text
8850 passed in 380.25s
```

Phase 108 は完了。

## Phase 109

Phase 108 後の運用監査から開始し、生成元問い合わせの利用者向け意味論と既知群の証明再生を閉じた。

主要な流れ:

```text
既知群同一性
→ 証明由来の ambient fallback
→ indexed sigma 具体化
→ proof-scope 統合
→ qualified execution 境界監査
→ 既知群の証明再生
→ show-proof
→ statement 表示 coverage
→ 利用者向け表示順の確定
```

Toda Proposition 5.15:

$$
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
$$

concrete indexed 具体化は $n\ge 10$ に限定し、symbolic higher step を直接 premise として保持する。

```text
show-proof != execute
候補番号 != 定理順位付け
concrete sigma_n specialization != 第3 qualified execution family
```

最終 repository 全体 regression:

```text
8998 passed in 493.70s (0:08:13)
```

Phase 109 は完了。

## Phase 110

Phase 110 は利用者向け数学演算問い合わせの実需要監査から開始し、既存 repository / proof-scope にすでに表現されている数学的演算事実を直接検索・表示・証明再生できる経路を追加した。

主要機能:

```text
最小 operation-query parser
既存 H / E / Delta / 二項 composition 事実検索
query CLI
raw occurrence 保持
同一 statement の表示 grouping
浅い depth と安定 source 順による表示
問い合わせ事実選択
選択事実自身を root とする証明再生
query-proof CLI
限定的数学 statement 表示
安全な aggregate type-name fallback
```

代表 CLI:

```text
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"

python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "H(nu_prime)" --fact 2
python main.py query-proof "E(eta_2 o nu_prime)"
```

確定した境界:

```text
lookup != inference != evaluation
deduplicated presentation != provenance deletion
query-proof root = selected fact's own ProofStep
fact number != theorem priority
```

最終 repository 全体 regression:

```text
9055 passed in 455.09s (0:07:35)
```

Phase 110 は完了。

## Phase 111

Phase 111 は新しい evaluator を先に作らず、Phase 110 までに揃った CLI capability を利用者視点で監査した。

主要サブフェーズ:

```text
111-1:
CLI inventory / discoverability audit

111-2:
command overlap / semantic boundary audit

111-3:
operation query grammar pressure audit

111-4:
proof replay usability audit

111-5:
full proof report presentation residual audit

111-6:
priority audit

111-7:
global CLI help / project-quantity wording minimal fix

111-8:
symbolic dimension presentation minimal fix

111-9:
3-term composition query minimal implementation

111-10:
proof replay --depth minimal exposure

111-11:
deep proof replay presentation residual audit

111-12:
deep show-proof safe fallback minimal fix

final:
residual audit / repository-wide regression
```

### 111-7: global CLI help

主要コマンドを global help から発見可能にした。

`n,k` の説明を通常の all-primary $\pi_{n+k}(S^n)$ と誤認しないよう、project quantity

$$
\pi_{n+k}^{n}
$$

すなわち free part + 2-primary component として明示した。

### 111-8: symbolic dimension presentation

symbolic dimension の表示で `ScalarSum(...)` / `ScalarSymbol(...)` が漏れる問題を修正。

$$
\pi_{n+7}^{n}
$$

を既存 scalar LaTeX renderer で表示するよう統一した。

### 111-9: 3-term composition query

実際の production fact

$$
\eta_2\circ(\nu'\circ\eta_6)
$$

に対応する最小 query として、

```text
eta_2 o nu_prime o eta_6
```

を追加した。

CLI では

$$
\pi_7^2=\mathbb Z/2\{\eta_2\nu'\eta_6\}
$$

および

$$
E\eta_2\nu'\eta_6=0
$$

を既存 repository 事実として取得できることを確認した。

一般 parser、四項以上、Unicode `∘`、三項 map-operation operand は追加していない。

### 111-10: replay `--depth`

既存 replay API の `max_depth` を CLI に最小公開。

```text
python main.py show-proof sigma_11 --depth 2
python main.py query-proof "H(nu_prime)" --fact 1 --depth 2
```

default は従来どおり 1。

```text
--depth 0
→ root のみ

negative depth
→ argparse error
```

### 111-11 / 111-12: deep replay presentation

`show-proof sigma_11 --depth 2` で unsupported aggregate statement の巨大な dataclass repr が露出する問題を確認。

fallback を安全な type-name 表示へ変更した。

```text
`Toda45IsomorphismStatement`
`TodaSigmaFamilyDefinitionStatement`
```

既に数式表示可能な

$$
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\},
\qquad
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad
\pi_{16}^{9}=\mathbb Z/16\{\sigma_9\}
$$

はそのまま維持した。

### Phase 111 完了確認

最終 repository 全体 regression:

```text
python -m pytest -q
9074 passed in 446.27s (0:07:26)
```

whitespace:

```text
git diff --check
clean
```

Phase 111 は完了。

---

# 現在の運用方針

`development_log.md` は索引として維持する。

詳細な新規開発記録は archive file に追記するか、Phase 範囲に応じて新しい archive file を追加する。

既存履歴は原則として削除せず、誤りが確定した場合のみ必要な訂正を行う。

現在機能の確認では次を優先する。

```text
README.md
docs/design.md
docs/roadmap.md
docs/code_reference.md
docs/proof_records.md
```

## Phase 112

Phase 112 は、Phase 111 で defer した syntax 項目を機械的に実装せず、現在の CLI を実際の数学的 workflow で使った際の capability pressure を監査した。

代表元:

```text
nu_prime
nu_5
sigma_11
```

### Phase 112-1A: `nu_prime`

通常経路は成功。

pressure:

```text
E(nu_prime)       → LOOKUP_MISS
Delta(nu_prime)   → LOOKUP_MISS
E(3-term comp.)   → parser boundary
```

### Phase 112-1B: `nu_5`

通常経路は成功。

pressure:

```text
E(nu_5)                   → LOOKUP_MISS
H(nu_5)                   → LOOKUP_MISS
E(nu_5 o eta_8)           → LOOKUP_MISS
E(3-term comp.)            → parser boundary
four-term composition      → parser boundary
```

### Phase 112-1C: `sigma_11`

```text
show-proof sigma_11
→ pi_18^11 = Z/16{sigma_11}
```

は成功した一方、

```text
python main.py 11 7
```

は当時 `NOT_FOUND`。

これを

```text
generator-side specialization exists
but TodaGroupQuery path does not reuse it
```

という orchestration gap と分類した。

`execute sigma_11` は既存仕様どおり `NONE`。

### Phase 112-2: operation / workflow capability gap classification

観測結果を次に分類した。

```text
parser boundary
repository lookup miss
workflow / orchestration gap
execution coverage boundary
possible new inference / evaluator gap
```

最重要 gap は `sigma_11` group-query の orchestration 不一致。

### Phase 112-3: lookup vs inference vs evaluator boundary

重要な結論:

```text
LOOKUP_MISS != evaluator required
```

Phase 65 の既存 $\nu$-family stable transport には

$$
E^{n-5}\nu_5=\nu_n
$$

があり、$n=6$ では

$$
E(\nu_5)=\nu_6.
$$

したがって general evaluator を作る前に既存 inference / specialization への最小 handoff を検討すべきと確定した。

### Phase 112-4: highest-pressure minimal capability selection

最優先として、

```text
python main.py 11 7
→ pi_18^11 = Z/16{sigma_11}
```

を既存 symbolic Proposition 5.15 specialization から再利用することを選定した。

Phase 112 は audit / selection で閉じ、実装は Phase 113 に分離した。

Phase 112 は完了。

## Phase 113

Phase 113 は既存 indexed $\sigma_n$ specialization を `TodaGroupQuery` 経路へ最小接続した。

既存 direct group lookup を優先し、見つからない場合のみ

```text
query.k == 7
query.n >= 10
```

に限定して、既存 proof scope と

```text
specialize_repository_proof_scope_for_generator(...)
```

を再利用する。

例:

$$
\pi_{17}^{10}=\mathbb Z/16\{\sigma_{10}\},
$$

$$
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\},
$$

$$
\pi_{19}^{12}=\mathbb Z/16\{\sigma_{12}\}.
$$

重要な境界:

```text
empty repository → NOT_FOUND
repository root を追加しない
k != 7 には適用しない
n < 10 には適用しない
symbolic Proposition 5.15 provenance を保持
operation-query semantics は変更しない
execute sigma_11 semantics は変更しない
```

focused tests:

```text
Phase 113 new tests: 7 passed
Phase 109-22: 26 passed
Phase 109-24: 10 passed
Phase 100-12c1: 5 passed
Phase 100-12c2: 5 passed
```

full regression:

```text
python -m pytest -q
9081 passed in 434.58s (0:07:14)
```

Phase 113 は完了。

### Phase 113 後の運用方針（当時）

次候補 Phase 114 は、general evaluator を作るのではなく、

$$
E(\nu_5)=\nu_6
$$

のような既存 inference capability を operation query へ最小 handoff できるかを扱う方針とした。

```text
direct lookup first
→ lookup miss
→ 許可された最小 existing inference handoff
→ provenance 保持
```

## Phase 114

Phase 114 は Phase 112 で確認した `E(nu_5)` の lookup miss を、general evaluator ではなく既存 symbolic inference への最小 handoff として解消した。

### Phase 114-1: existing inference path audit

Phase 65 の既存 production proof に

$$
E^{n-5}\nu_5=\nu_n
$$

が存在し、

```text
toda_prop56_higher_nu_family_bridge_inference_rule()
```

によって構築されていることを確認した。

既存 bridge の provenance は

```text
nu_5 definition
nu_n definition
n >= 6
```

を保持している。

したがって $n=6$ では

$$
E(\nu_5)=\nu_6
$$

を既存数学から得られることを確認した。

新しい定理規則は不要と判定した。

### Phase 114-2: minimal handoff design audit

operation query の既存意味論を維持するため、

```text
query
→ direct lookup
→ hit なら従来結果
→ miss
→ exact E(nu_5) guard
→ theorem-specific concrete specialization
→ result + provenance
```

とする設計を採用した。

一般 `repository_inference.py` を query miss 全般に接続しない。

Phase 109 の $\sigma_n$ specialization と同様に、

```text
concrete ProofStep
→ premise: existing symbolic ProofStep
```

という provenance-preserving specialization を用いる。

### Phase 114-3: `E(nu_5)` minimal handoff implementation

追加:

```text
repository_nu5_stable_bridge_specialization.py
```

変更:

```text
repository_operation_query_facade.py
```

direct lookup の結果がある場合は必ずそのまま返す。

direct miss かつ exact `E(nu_5)` の場合のみ、

$$
E(\nu_5)=\nu_6
$$

の concrete `ProofStep` を生成する。

concrete step の direct premise は既存 symbolic bridge である。

`repository_operation_query_lookup.py`、`repository_operation_query_proof_replay.py`、`main.py` は変更しなかった。

focused tests:

```text
9 passed
```

Phase 110 operation-query / proof replay regression:

```text
24 passed
```

CLI:

```text
python main.py query "E(nu_5)"
→ Eν_5 = ν_6

python main.py query-proof "E(nu_5)"
→ concrete specialization
→ symbolic Proposition 5.6 bridge

python main.py query-proof "E(nu_5)" --depth 2
→ ν_5 definition
→ ν_n definition
→ n >= 6
```

### Phase 114-4: minimal handoff regression / boundary audit

production code は追加変更せず、境界テストを拡張した。

固定した境界:

```text
direct E fact は優先
direct H fact は優先
direct Delta fact は優先
H(nu_5) には拡張しない
Delta(nu_5) には拡張しない
E(nu_6) には拡張しない
E(sigma_11) には拡張しない
E(nu_5 o eta_8) には拡張しない
三項 map-operation operand は parser boundary のまま
四項 composition は parser boundary のまま
repository は非変更
```

Phase 114 focused boundary tests:

```text
16 passed
```

Phase 110 / 111 / 114 関連回帰:

```text
60 passed
```

repository 全体 regression:

```text
python -m pytest -q
9097 passed in 449.47s (0:07:29)
```

Phase 114 は完了。

### Phase 114 後の残件

symbolic bridge の表示が

```text
E^{n + -1\,5}ν_5 = ν_n
```

となる箇所がある。

数学的内容は

$$
E^{n-5}\nu_5=\nu_n
$$

であり、これは Phase 114 の inference handoff ではなく scalar LaTeX presentation の残件として分離する。

次 Phase は Phase 114 の handoff を機械的に一般化せず、残存する operation / workflow pressure を再監査して最小の次対象を選ぶ。

## Phase 115

Phase 115 は Phase 114 の成功を一般化することから始めず、残存する operation / workflow pressure を再監査した。

### Phase 115-1: post-Phase 114 capability pressure audit

代表候補:

```text
E(sigma_11)
H(nu_5)
H(sigma_11)
Delta(sigma_11)
E(nu_prime)
Delta(nu_prime)
```

を、

```text
existing direct fact
existing symbolic inference / specialization
new inference required
presentation-only issue
parser boundary
execution boundary
```

へ分類する方針を採用した。

### Phase 115-2: existing mathematics reuse audit

最も明確な reuse candidate は `E(sigma_11)` と判定した。

既存 Toda Lemma 5.14 の $\sigma$-family definition:

$$
\sigma_n=E^{n-8}\sigma_8
$$

から、

$$
\sigma_{11}=E^3\sigma_8,
\qquad
\sigma_{12}=E^4\sigma_8
$$

を既存 infrastructure で具体化できる。

一方で operation-query が直接検索できる

$$
E(\sigma_{11})=\sigma_{12}
$$

という `Relation` は repository root に存在していなかった。

したがって、

```text
new mathematics is not required
but theorem-specific definitional handoff is required
```

と分類した。

`E(nu_prime)` については既存 proof 内に $E\nu'$ や $E^2\nu'$ が部分式として現れるが、

```text
expression occurrence
!= operation result relation
```

であり、同じ reuse pattern とは分類しなかった。

### Phase 115-3: next minimal capability selection / design audit

exact

```text
E(sigma_11)
```

のみを次の最小対象として選定した。

設計:

```text
query
→ direct lookup
→ hit なら従来結果
→ miss
→ exact E(sigma_11) guard
→ existing symbolic sigma-family definition
→ sigma_11 / sigma_12 concrete definitions
→ E(sigma_11) = sigma_12
→ provenance
```

general `E(sigma_n)` evaluator は対象外とした。

`repository_operation_query_lookup.py`、parser、renderer、repository root は変更しない方針とした。

### Phase 115-4: `E(sigma_11)` minimal operation-query handoff implementation

追加:

```text
repository_sigma11_suspension_specialization.py
tests/test_phase115_sigma11_operation_query_handoff.py
```

変更:

```text
repository_operation_query_facade.py
tests/test_phase114_3_nu5_operation_query_handoff.py
```

Phase 114 の $\nu_5$-specific guard 自体は `E(sigma_11)` を受理しないことを維持しつつ、facade に独立した exact $\sigma_{11}$ handoff を追加した。

concrete result:

$$
E(\sigma_{11})=\sigma_{12}.
$$

provenance:

```text
E(sigma_11) = sigma_12
→ TodaSigmaFamilyDefinitionStatement
→ TodaLemma514Sigma8Statement
→ ScalarGreaterEqualStatement
```

CLI:

```text
python main.py query "E(sigma_11)"
→ E sigma_11 = sigma_12

python main.py query-proof "E(sigma_11)" --depth 2
→ concrete operation relation
→ Toda Lemma 5.14 sigma-family definition
→ sigma_8 branch / range premise
```

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

実装途中で PowerShell の既定文字コードにより `ν` / `σ` を含むテストファイルが文字化けする問題が発生した。

これは production semantics の問題ではなく編集手順上の encoding issue であり、Git HEAD / package から UTF-8 を復元し、以後の修正を Python UTF-8 I/O で行って解消した。

### Phase 115-5: post-implementation boundary audit

`E(sigma_11)` 解消後、残存 pressure を再分類した。

```text
H(nu_5)
→ new mathematical inference required

H(sigma_11)
→ related low-dimensional mathematics exists
→ reusable H family bridge is not currently present

Delta(sigma_11)
→ reusable concrete / family relation is not currently present

E(nu_prime)
→ E nu_prime occurs as an expression
→ operation-result relation is not present

Delta(nu_prime)
→ direct / reusable family inference is not currently present

E(nu_5 o eta_8)
→ composition-operation inference boundary

three-term map-operation operand
→ parser boundary

four-term composition
→ parser boundary

execute sigma_11
→ execution coverage boundary
```

したがって Phase 115 では追加 capability を広げず、exact `E(sigma_11)` で停止することを確定した。

### Phase 115-6: documentation / closure

Phase 115 の current architecture、proof provenance、remaining boundary を文書へ反映した。

repository 全体 regression:

```text
python -m pytest -q
9111 passed in 432.54s (0:07:12)
```

Phase 115 は完了。

次 Phase は Phase 115 の handoff を自動的に一般化せず、残存する数学的 pressure、presentation-only residual、parser / execution boundary の優先度を再監査してから最小対象を選ぶ。
