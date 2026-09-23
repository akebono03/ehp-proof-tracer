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

\[
E(\nu_5)=\nu_6
\]

を exact handoff として operation query へ接続。

```text
9097 passed in 449.47s
```

## Phase 115

\[
E(\sigma_{11})=\sigma_{12}
\]

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

\[
E(\nu_5\eta_8)=0
\]

を exact theorem-specific handoff として実装。

final:

```text
9256 passed in 570.10s (0:09:30)
```

## Phase 129

既存 Proposition 5.6:

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}
\]

を再利用し、

\[
E\nu' \in \pi_7^4
\]

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

\[
\pi_3^2,\quad
\pi_4^3,\quad
\pi_4^2,\quad
\pi_5^3.
\]

focused:

```text
6 passed in 5.30s
```

## Phase 130-5〜6: stem 1–3 stable specialization

\[
\pi_{n+1}^n=\mathbb Z/2\{\eta_n\},
\]

\[
\pi_{n+2}^n=\mathbb Z/2\{\eta_n\eta_{n+1}\},
\]

\[
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\}.
\]

focused:

```text
14 passed in 3.47s
```

## Phase 130-7〜8: stem 4–6

\[
\pi_{n+4}^n=0
\qquad (n\ge6),
\]

\[
\pi_{n+5}^n=0
\qquad (n\ge7),
\]

\[
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\}.
\]

focused:

```text
24 passed in 9.23s
```

## Phase 130-9: foundational semantics audit

確定 semantics:

\[
k=0
\Rightarrow
\pi_n^n\cong\mathbb Z\{\iota_n\},
\]

\[
n=1,\ k\ge1
\Rightarrow
\pi_{1+k}^1=0,
\]

\[
1\le n+k<n
\Rightarrow
\pi_{n+k}^n=0.
\]

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

\[
\pi_{16}^{9}
=
\mathbb Z/16\{\sigma_9\}
\]

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

次 Phase 131 は capability / usage-pressure audit から開始する。
