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
Phase 96: 構造化表示 / 読みやすい完全証明レポート
Phase 97: 計算からレポートまでのオーケストレーション
Phase 98: 生の n,k 入力用簡易 facade
Phase 99: 生成元中心 repository 探索
Phase 100: 標準運用 repository / build_standard_toda_report / main.py n k
Phase 101: 標準 repository と generator explore
Phase 102: 再帰的 proof-scope 探索
Phase 103: 適用可能定理 / 補題探索と関連度分類
Phase 104: 候補 → READY → bounded search → execution
Phase 105: 第1 qualified production family
Phase 106: applicability performance audit
Phase 107: multi-family qualified execution
Phase 108: user-facing execute workflow / CLI
Phase 109: known-group identity / indexed sigma / show-proof
Phase 110: operation query / query-proof
Phase 111: CLI audit / 3-term query / --depth / safe fallback
```

代表 regression:

```text
Phase 108: 8850 passed in 380.25s
Phase 109: 8998 passed in 493.70s
Phase 110: 9055 passed in 455.09s
Phase 111: 9074 passed in 446.27s
```

---

# Phase 112–129

## Phase 112–113

実際の workflow pressure を監査し、symbolic \(\sigma_n\) specialization を `TodaGroupQuery` へ接続。

```text
Phase 113 final:
9081 passed in 434.58s
```

## Phase 114

$$
E(\nu_5)=\nu_6
$$

を exact handoff として operation query へ接続。

```text
9097 passed in 449.47s
```

## Phase 115

$$
E(\sigma_{11})=\sigma_{12}
$$

を exact handoff として接続。

```text
9111 passed in 432.54s
```

## Phase 116–125

Flask + KaTeX Web UI を段階的に構築。

```text
Phase 117: group query
Phase 118: operation query / query-proof
Phase 120: show-proof
Phase 121: explore
Phase 122: explore-proof
Phase 123: explore-applicable
Phase 124: workflow navigation
Phase 125: execute
```

Phase 125 final:

```text
9243 passed in 555.37s
```

## Phase 126

proof-scope relevance、applicability relevance、executable relevance を分離。

```text
nu_prime → 2 executable targets
nu_5 → NONE
sigma_11 → NONE
```

final:

```text
9246 passed in 556.62s
```

## Phase 127

operation-query capability pressure を監査。

## Phase 128

$$
E(\nu_5\eta_8)=0
$$

を exact theorem-specific handoff として実装。

final:

```text
9256 passed in 570.10s (0:09:30)
```

## Phase 129

既存 Proposition 5.6:

$$
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}
$$

を再利用し、

$$
E\nu' \in \pi_7^4
$$

という membership result を実装。

final:

```text
9268 passed in 569.71s (0:09:29)
```

Phase 129 完了。

---

# Phase 130 — standard query coverage / boundary semantics

Phase 130 は operation evaluator の一般化ではなく、既存 theorem-backed group result を standard query から利用できるようにすることを目的とした。

## Phase 130-1〜4: low-dimensional query recovery

standard query で未表示だった低次元群を proof ancestry から回収。

対象例:

$$
\pi_3^2,\quad
\pi_4^3,\quad
\pi_4^2,\quad
\pi_5^3.
$$

focused:

```text
6 passed in 5.30s
```

## Phase 130-5〜6: stem 1–3 stable specialization

$$
\pi_{n+1}^n=\mathbb Z/2\{\eta_n\},
$$

$$
\pi_{n+2}^n=\mathbb Z/2\{\eta_n\eta_{n+1}\},
$$

$$
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\}.
$$

focused:

```text
14 passed in 3.47s
```

## Phase 130-7〜8: stem 4–6

$$
\pi_{n+4}^n=0
\qquad (n\ge6),
$$

$$
\pi_{n+5}^n=0
\qquad (n\ge7),
$$

$$
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\}.
$$

focused:

```text
24 passed in 9.23s
```

## Phase 130-9: foundational semantics audit

確定 semantics:

$$
k=0
\Rightarrow
\pi_n^n\cong\mathbb Z\{\iota_n\},
$$

$$
n=1,\ k\ge1
\Rightarrow
\pi_{1+k}^1=0,
$$

$$
1\le n+k<n
\Rightarrow
\pi_{n+k}^n=0.
$$

```text
n+k = 0
→ pi_0 boundary information

n+k < 0
→ classical unstable homotopy-group domain 外
```

## Phase 130-10: foundational query implementation

negative `k` を許可し、CLI / Web で domain semantics を分離。

focused:

```text
44 passed in 12.27s
```

## Phase 130-11: \(\pi_{16}^9\) standard-query connection

既存 Proposition 5.15 ancestry の concrete proof

$$
\pi_{16}^{9}
=
\mathbb Z/16\{\sigma_9\}
$$

を standard query に接続。

generic indexed \(\sigma_n\) specialization は \(n\ge10\) を維持。

focused:

```text
26 passed in 7.14s
```

## Phase 130-12: completion regression

repo 内 backup directory の copied `test_*.py` が pytest collection conflict を起こすことを確認。

運用を

```text
backup は repo 外
full regression は python -m pytest tests -q
```

へ修正。

旧 Phase 100 test の negative-k rejection expectation も新仕様へ更新。

focused:

```text
4 passed in 3.17s
```

最終 repository-wide regression:

```text
9308 passed in 577.02s (0:09:37)
```

Phase 130 完了。

---

# Phase 131 — group-result proof replay

Phase 131 は、標準 group query の結果から既存証明へ直接進める user-facing path を整備した。

新しい数学定理や一般 proof search は追加していない。

## Phase 131-1: 現行経路監査

既存データ経路:

```text
n,k
→ TodaCalculationResult
→ TodaCalculationCandidate
→ TodaGroupResult
→ ProofStep
```

を監査。

`TodaGroupResult` が

```text
source_entry
proof_step
```

を保持し、

```text
proof_step is source_entry.step
```

を維持していることを確認。

また既存

```text
extract_toda_recursive_proof_provenance()
```

が root から再帰 ancestry を取得できるため、新しい探索アルゴリズムは不要と判断した。

## Phase 131-2: 最小 API 設計

採用方針:

```text
TodaGroupResult
→ existing recursive provenance
→ depth filter
→ group-result proof replay
```

generator-first replay を無理に一般化せず、group-result 専用の薄い API とすることを決定。

## Phase 131-3: core API

追加:

```text
TodaGroupResultProofReplayStep
TodaGroupResultProofReplayResult
build_toda_group_result_proof_replay()
```

保持:

```text
group_result identity
source_entry identity
root ProofStep identity
role
shortest depth
```

focused:

```text
8 passed in 2.73s
```

## Phase 131-4: CLI 接続

追加:

```powershell
python main.py group-proof n k
python main.py group-proof n k --depth N
```

代表:

```powershell
python main.py group-proof 9 7
python main.py group-proof 9 7 --depth 2
python main.py group-proof 2 7
python main.py group-proof 11 -1
```

結果例:

$$
\pi_{16}^{9}=\mathbb Z/16\{\sigma_9\},
$$

$$
\pi_9^2=0,
$$

$$
\pi_{10}^{11}=0.
$$

Phase 130 の connectivity zero が repository-backed result であるため、`Sphere connectivity / Phase 130` として replay 可能であることを再確認。

focused:

```text
14 passed in 7.61s
```

## Phase 131-5: Web 接続

group query result 直下へ

```text
Proof depth: 0 / 1 / 2
Show proof
```

を追加。

Web proof 表示:

```text
Conclusion
Provenance
Proof
Depth
Role
Rule
```

repository-backed result のみ `proof_available=True` とする。

したがって connectivity zero は replay 可能だが、

```text
pi_0 boundary information
negative-dimensional out-of-domain information
```

には proof button を出さない。

focused:

```text
39 passed in 17.21s
```

Web manual check で \(\pi_{16}^{9}\) の depth 2 replay を確認。

## Phase 131-6: completion regression

repository-wide regression:

```powershell
python -m pytest tests -q
```

結果:

```text
9333 passed in 583.64s (0:09:43)
```

Phase 131 完了。

---

# Phase 132 — deterministic proof presentation

Phase 132 は、Phase 131 の machine-traceable group-result proof replay を人間が読みやすい表示へ拡張した。

新しい数学定理、一般 proof search、operation evaluator は追加していない。

## Phase 132-1〜3: narrative / graph semantics audit

既存 `toda_proof_narrative_renderer.py` と \(\pi_{16}^{9}\) の Proposition 5.15 ancestry を監査。

確定した重要事項:

```text
ProofStep.premises edge
→ proof structure の ground truth

flat replay depth/order
→ parent-child relation の ground truth ではない
```

Trace / Outline / Narrative は同じ proof graph を使う方針とした。

## Phase 132-4: `TodaGroupProofPresentation`

追加:

```text
TodaGroupProofPresentation
build_toda_group_proof_presentation()
```

Phase 131 replay の selected node をそのまま保持し、既存 recursive provenance edge を selected node に filter する薄い presentation core とした。

```text
presentation.nodes is replay.steps
```

新しい proof search / depth semantics は追加しない。

focused:

```text
10 passed in 8.73s
```

関連:

```text
35 passed in 10.73s
```

## Phase 132-5: deterministic Outline renderer

追加:

```text
toda_group_proof_outline_renderer.py
render_toda_group_proof_outline_markdown()
```

\(\pi_{16}^{9}\) について actual premise edge と `premise_index` を使って階層表示。

unsupported statement は既存 mathematical renderer、rule name、type name の安全な fallback を利用。

focused:

```text
8 passed in 6.99s
```

関連:

```text
43 passed in 10.05s
```

## Phase 132-6: deterministic Narrative renderer

追加:

```text
toda_group_proof_narrative_renderer.py
render_toda_group_proof_narrative_markdown()
```

固定テンプレート:

```text
〜を用いる。
これらから、〜を得る。
したがって、〜を得る。
```

のみを使い、自由生成による数学的説明は行わない。

sibling premise order と causal narrative order を同一視しないことをテストで確定。

focused:

```text
9 passed in 11.62s
```

関連:

```text
52 passed in 12.71s
```

## Phase 132-7: CLI Trace / Outline / Narrative

`group-proof` に追加:

```powershell
python main.py group-proof 9 7 --mode trace
python main.py group-proof 9 7 --mode outline
python main.py group-proof 9 7 --mode narrative
```

`--mode` 省略時は `trace`。

`--depth` は3 mode で共通。

focused:

```text
9 passed in 16.53s
```

関連:

```text
61 passed in 14.69s
```

## Phase 132-8: Narrative shared-dependency deduplication

同じ `ProofStep` が複数 parent から利用される DAG で、Narrative が同じ subtree を何度も全文再展開しないようにした。

```text
first use
→ subtree expand

later use
→ 既出の ... を用いる。
```

proof graph / Trace / Outline は変更しない。

focused:

```text
8 passed in 25.48s
```

Narrative / CLI 関連:

```text
26 passed in 9.50s
```

Phase 131〜132-8 関連:

```text
69 passed in 16.96s
```

## Phase 132-9: Web Trace / Outline / Narrative

Web group proof に

```text
Proof view:
Trace
Outline
Narrative
```

を追加。

既存 proof depth 0 / 1 / 2 を3 mode で共通利用。

Outline / Narrative は既存 Phase 132 renderer を再利用し、Web adapter は数式 fragment を `data-latex` へ分離して KaTeX 経路を維持。

focused:

```text
15 passed in 15.93s
```

Web 周辺:

```text
60 passed in 20.16s
```

Phase 131〜132-9 関連:

```text
84 passed in 21.58s
```

## Phase 132-10: completion regression / documentation

repository-wide regression:

```powershell
python -m pytest tests -q
```

結果:

```text
9392 passed in 587.98s (0:09:47)
```

Phase 132 完了。

---

# Phase 133 — Narrative readability refinement

Phase 133 は post-Phase-132 capability / workflow pressure audit として開始し、実利用上の具体的 pressure として **Narrative の可読性**を選んだ。

新しい数学定理、proof search、Trace / Outline semantics、operation evaluator は追加していない。

## Phase 133-3: representative statement labels

\(\pi_{16}^{9}\) の Narrative で内部 class / rule 名が見えていた代表 statement に明示的 label を追加。

代表:

```text
Toda48Pi16_9OrderAndE4InjectiveStatement
→ π₁₆⁹ の位数 16 と E⁴ の単射性

TodaLemma514Sigma8Statement
→ Toda Lemma 5.14 の σ₈ に関する結果

TodaSigmaFamilyDefinitionStatement
→ σ-family の定義
```

## Phase 133-4: connectives / shared dependency reuse

表示上の接続語を premise 数に合わせて整理。

```text
1 premise
→ このことから

2 premises 以上
→ これらから
```

shared dependency については nested immediate reuse を抑制し、root-level など必要な再参照では

```text
すでに得た ... を用いる。
```

と表示するようにした。

proof graph / provenance は変更していない。

focused:

```text
32 passed in 12.42s
```

## Phase 133-5: representative five-group audit

代表群

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{16}^9
$$

について depth 1 / 2 の Narrative を横断監査。

低次元、\(\nu\)-family、\(\sigma\)-familyに残る内部 rule 名を抽出した。

## Phase 133-6: low-dimensional / nu-family / sigma-triple-prime labels

追加した代表 label:

```text
E²: π₆³ → π₈⁵ の単射性
π₈⁵ / E²π₆³ が位数 2 であること
Toda (5.6) の ν₄ 分解
π₁₂⁵ の位数 2 の Hopf 像への同型
Toda Lemma 5.13 の σ‴ に関する結果
```

focused:

```text
36 passed
```

## Phase 133-7: remaining depth-2 internal labels

追加した代表 label:

```text
Toda (5.2) の η₂ 合成同型
ν′ に対する Lemma 5.2 の Toda bracket 特殊化
Toda (5.5) の ν-family 有限次元結果
Δ 写像が零写像であること
Hopf 写像の単射性
Toda Proposition 5.1 の有限次元結果
Toda Proposition 5.11 の有限次元結果
```

focused:

```text
39 passed
```

## Phase 133-8: five-group cross audit

代表5群の depth 1 / 2 を再監査。

残存内部 rule 名を5件に限定した。

対象:

```text
Toda Proposition 5.6 finite-dimensional integration
Toda (5.6) nu_4 decomposition isomorphism semantics
Toda Lemma 5.4 integration
Toda Theorem 3.6 Lemma 5.14 sigma double-prime bridge
Toda Lemma 5.14 sigma-prime branch
```

## Phase 133-9: final five statement labels

追加:

```text
Toda Proposition 5.6 の有限次元結果
Toda (5.6) の ν₄ 分解同型
Toda Lemma 5.4 の結果
Theorem 3.6 から Lemma 5.14 への σ″ bridge
Toda Lemma 5.14 の σ′ branch
```

focused:

```text
42 passed
```

## Phase 133-10: sigma wording finalization

最後の2ラベルを Narrative 本文として自然な文面へ調整。

最終:

```text
Theorem 3.6 と Lemma 5.14 を結ぶ σ″ の関係
Toda Lemma 5.14 の σ′ に関する結果
```

Phase 133-9 の旧期待値テストも新文面へ更新。

focused:

```text
43 passed in 15.79s
```

## Phase 133-final: representative audit / full regression

代表5群:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{16}^9
$$

について depth 1 / 2 を最終確認。

監査結果:

```text
Internal wording audit
→ 0件

Old / awkward Narrative wording
→ 0件
```

\(\pi_{16}^{9}\) depth 2 の最終 σ 系表示:

```text
Theorem 3.6 と Lemma 5.14 を結ぶ σ″ の関係
Toda Lemma 5.14 の σ′ に関する結果
Toda Lemma 5.14 の σ₈ に関する結果
σ-family の定義
```

focused regression:

```text
43 passed in 14.16s
```

repository-wide regression:

```powershell
python -m pytest tests -q
```

結果:

```text
9403 passed in 605.52s (0:10:05)
```

Phase 133 完了。

---

# Phase 134 — natural mathematical Narrative refinement

Phase 134 は Phase 133 の human-readable label 改善をさらに進め、代表的な群の Narrative を「証明文として自然に読める」形へ整備した。

新しい数学定理、proof search、Trace / Outline semantics、operation evaluator は追加していない。

## Phase 134-3〜8: \(\pi_6^3\) Narrative

Toda Proposition 5.6 の

$$
\pi_6^3=\mathbb Z/4\{\nu'\}
$$

を代表例として、単なる statement 列ではなく、

```text
まず, ν' の位数を求める.
次に, ν' ∈ π_6^3 であることを確認する.
最後に, EHP 完全列を用いて π_6^3 の群構造を決定する.
```

という数学的 block 構造を導入した。

REFERENCE section では既存の Toda (5.2)、Proposition 5.1 を明示し、本文中の依存関係を `[R1]`, `[R2]` で参照する。

## Phase 134-9〜16: \(\pi_8^5\) への拡張と semantic classification

第2代表例として

$$
\pi_8^5=\mathbb Z/8\{\nu_5\}
$$

を追加。

fact role:

```text
TARGET
REFERENCE
DEFINITION
BOUNDARY
DERIVED
```

block role:

```text
ORDER
MEMBERSHIP
GROUP_STRUCTURE
OTHER
```

を導入し、presentation 層で proof fact の役割を分類した。

この分類は表示専用であり、

```text
fact role
!= new theorem fact
!= new proof edge
!= proof search
```

である。

\(\pi_8^5\) では、

```text
2ν_5 = E^2ν'
π_6^3 = Z/4{ν'}
E^2 の単射性
ν_5 の位数 8
π_8^5 / E^2π_6^3 の位数 2
```

という既存事実を、読みやすい順序で Narrative 化した。

## Phase 134-17〜24: \(\pi_{15}^8\) 2-generator Narrative

第3代表例として Toda Proposition 5.15 の

$$
\pi_{15}^{8}
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}
$$

を採用。

既存 Proposition 4.4 の分解同型

$$
\pi_{14}^{7}\oplus\pi_{15}^{15}
\longrightarrow
\pi_{15}^{8}
$$

を REFERENCE として利用し、

$$
\sigma'\longmapsto E\sigma',
\qquad
\iota_{15}\longmapsto\sigma_8
$$

という generator transport を明示した。

transport 直後の順序

$$
\mathbb Z/8\{E\sigma'\}
\oplus
\mathbb Z\{\sigma_8\}
$$

から、標準表示

$$
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}
$$

への並べ替えも Narrative に保持した。

この実装は Proposition 4.4 固有の theorem-specific renderer として維持し、generic multi-generator synthesis へ一般化していない。

## Phase 134-25〜31: presentation-only 共通化

3例を横断監査し、数学的本文ではなく presentation framing だけを共通化した。

Phase 134-26:

```text
# Group proof narrative
## 証明対象
## 使用する結果
## 証明
```

という外枠を共通化。

Phase 134-28:

```text
[R1], [R2], ...
**[Rn] <title>.**
optional statement lines
reference block spacing
```

という REFERENCE block assembler を共通化。

Phase 134-30:

```text
display math
completed boundary framing
final conclusion framing
```

という proof-body presentation primitive を共通化。

一方、以下は theorem-specific のまま維持した。

```text
block leads
dependency selection
proof ordering
numbered-fact semantics
pi_6^3 proof logic
pi_8^5 proof logic
Proposition 4.4 transport
multi-generator theorem synthesis
map-formula extraction
```

Phase 134-31 の hardcode 再監査では、Phase 134-26 / 28 / 30 で抽出した helper が root-specific / statement-specific ではないことを確認した。

## Phase 134-32: completion audit

最終監査対象:

$$
\pi_6^3,\qquad
\pi_8^5,\qquad
\pi_{15}^8.
$$

確認結果:

```text
renderer boundary: PASS
semantic boundary: PASS
three-example Narrative regression: PASS
scope guard: PASS
```

追加しなかったもの:

```text
root_generators()
generic multi-generator synthesis
generic direct-sum proof synthesis
```

focused regression:

```text
40 passed in 5.78s
```

repository-wide regression:

```text
9495 passed in 282.46s (0:04:42)
```

Phase 134 完了。

---

# Phase 135–136 — Web Narrative / \(\pi_6^3\) Narrative refinement

## Phase 135: Web Narrative math presentation

Phase 135 は Phase 134 で自然化した Narrative を Web 上でも読みやすく表示するため、display math と inline math の presentation adapter を監査・調整した。

主な境界:

```text
Web adapter
!= proof semantics
!= second Narrative renderer
```

実装済み:

```text
display math → data-latex → KaTeX display mode
inline math → data-latex → KaTeX inline mode
multiple inline math segments
REFERENCE emphasis preservation
Narrative reading-width / spacing adjustment
```

## Phase 136-1〜2: \(\pi_6^3\) Narrative の数学的順序監査

代表対象:

$$
\pi_6^3=\mathbb Z/4\{\nu'\}.
$$

Phase 136-2 では証明の数学的依存関係に合わせて Narrative を再構成した。

Toda Lemma 5.2 の適用前に

$$
2\eta_3=0
$$

を確認する。

これにより

$$
\{\eta_3,2\iota_4,\eta_4\}_1
$$

が定義でき、その bracket のある元を \(\nu'\) と定める。

その後 Lemma 5.2 から

$$
\nu'\in\pi_6^3,
\qquad
H(\nu')=\eta_5,
\qquad
2\nu'=\eta_3^3
$$

を得る。

Toda Proposition 2.2 の右合成公式

$$
H(\alpha\circ E\beta)=H(\alpha)\circ E\beta
$$

を明示し、

$$
\eta_6=E\eta_5
$$

と合わせて

$$
H(\nu'\eta_6)
=
H(\nu'\circ E\eta_5)
=
H(\nu')\circ E\eta_5
=
\eta_5\eta_6
=
\eta_5^2
$$

を得る流れを本文に表示した。

位数決定に用いる EHP 完全列:

$$
\pi_7^3
\xrightarrow{H}
\pi_7^5
\xrightarrow{\Delta}
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5.
$$

\(H:\pi_7^3\to\pi_7^5\) の全射性から \(\Delta=0\) を得て、完全性から

$$
E:\pi_5^2\to\pi_6^3
$$

が単射であることを明示した。

最後に

$$
0
\longrightarrow
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5
\longrightarrow
0
$$

を表示し、\(\pi_6^3\) の位数が 4 であることと、\(\nu'\) が位数 4 の元であることから

$$
\pi_6^3=\mathbb Z/4\{\nu'\}
$$

を得る。

Phase 133–135 の旧 Narrative 固定値テストは、Phase 136-2 の確定仕様へ更新した。

focused regression:

```text
65 passed in 15.85s
```

repository-wide regression:

```text
9517 passed in 575.31s (0:09:35)
```

Phase 136-2 完了。

## Phase 136-2 closure Web TeX audit

Phase 136-2 完了後の Web manual check で、Narrative の数学式自体は KaTeX 経路で表示されることを確認した。

一方、静的 template text に次の未整備を確認した。

```text
Group query description:
pi_(n+k)^n
→ plain text

Provenance:
窶・Phase
→ encoding / mojibake
```

`H(nu_prime)`、`E(nu_5)`、`sigma_11` 等は入力 syntax の例なので plain text を維持する方針とした。

---

# Phase 137 — Web presentation cleanup

Phase 137 は数学機能を増やさず、Phase 136-2 の Web manual audit で 確認した presentation-only pressure を処理する。

## Phase 137-2: static math / mojibake cleanup

`templates/index.html` の Group query 説明にある project quantity を

$$
\pi_{n+k}^{n}
$$

として既存 `data-latex` / KaTeX 経路へ接続した。

同じ template 内の `窶・` は6か所すべて正常な em dash `—` へ復元した。

対象:

```text
Group proof provenance
Operation proof Phase
Operation proof repository depth x2
Applicability showing first
Generator execution provenance
```

入力 syntax:

```text
H(nu_prime)
E(nu_5)
sigma_11
```

は plain text のまま維持した。

focused:

```text
3 passed in 6.96s
```

## Phase 137-3: Web focused regression

Phase 117 / 124 / 131 / 132 / 135 / 137 の関連 Web tests を実行。

```text
56 passed in 20.23s
```

## Phase 137-4: Web manual verification

実画面で以下を確認した。

```text
\pi_{n+k}^{n} → KaTeX
H(nu_prime), E(nu_5), sigma_11 → plain text
— showing first → 正常表示
Generator execution provenance → — Phase 68
窶・ → visible output から消失
```

## Phase 137-5: documentation cleanup

README / design / development log / roadmap / proof records を Phase 137 の現状へ更新する。

あわせて GitHub Markdown 上の display math を `$$ ... $$` に統一し、legacy display-math delimiters が生の bracket のように見える presentation 問題を解消する。

```text
documentation math delimiter cleanup
!= mathematical content change
!= proof semantics change
```

# 現在の運用方針

`development_log.md` は索引 + 直近 Phase 記録として維持する。

詳細な古い記録は archive file に保存する。

既存履歴は原則として削除せず、誤りが確定した場合のみ訂正する。

全体回帰:

```powershell
python -m pytest tests -q
```

backup:

```text
repository 外へ保存
```

Phase 137 の repository-wide regression は Phase-final step でのみ実行する。

Phase 137 を閉じた後は Phase 138 capability audit を行い、Narrative の他群への拡張、Web workflow、operation query、stem 8 以降のどれを優先するかを実利用 pressure から選ぶ。
