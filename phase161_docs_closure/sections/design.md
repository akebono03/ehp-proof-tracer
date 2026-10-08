## Phase 161 — Concrete Backward Goal Schema と provenance 境界

Phase 161 は、非安定 EHP の具体的目標

$$
E:\pi_4^2\xrightarrow{\cong}\pi_5^3
$$

に対する Backward Chaining（後向き推論）の最小縦断実装を導入した。現行の Production Rule（前向き推論規則）を変更せず、逆向きの目標分解と前向きの証明構築を別の責務として扱う。

### 目標展開

```text
E isomorphism
├── E injective
│   └── Delta_6 zero
│       └── H_6 surjective
└── E surjective
    └── H_5 zero
        └── Delta_5 injective
```

EHP 完全性は4箇所で別々の部分目標・証拠として保持する。

$$
\pi_5^3\xrightarrow{H}\pi_5^5\xrightarrow{\Delta}\pi_3^2,
$$
$$
\pi_4^2\xrightarrow{E}\pi_5^3\xrightarrow{H}\pi_5^5,
$$
$$
\pi_6^3\xrightarrow{H}\pi_6^5\xrightarrow{\Delta}\pi_4^2,
$$
$$
\pi_6^5\xrightarrow{\Delta}\pi_4^2\xrightarrow{E}\pi_5^3.
$$

末端規則には既存の `TodaProp51FiniteDimensionalStatement` と $H(\nu')=\eta_5$ の `Relation` など、既存の推論済み前提を照合する。`conclusion_builder` と `match_guard` は既存規則のものを再利用し、文字列による数学命題判定には置き換えない。

### 証明再構築と信頼境界

R5 は完成済み同型の `ProofStep` を入力せず、承認された前提証拠から7規則を適用し、新たな `ProofRule.INFERENCE` の導出を構築する。ただし、元となる文献前提の `ProofStep` の祖先の正しさは R5 だけでは保証されない。

R6 でこの限界を明示した。R7 の検証付き入口では、`INFERENCE` の依存関係を再帰的にたどり、既存規則から結論を再計算する。未承認の `GIVEN`、根拠のない `INFERENCE`、改変された結論、循環する祖先は拒否する。`GIVEN` の出所承認は外部に残る Trust Boundary（信頼境界）であり、文献事実の数学的妥当性を形式証明したことにはならない。R7 は R5 の従来 API を変更せず、検証済み経路を追加する。

### 制限と次 Phase

本実装は $E:\pi_4^2\to\pi_5^3$ に特化した7規則の再構築である。任意群の規則選択、文献命題の自律探索、無制限な AND/OR 探索、public Narrative との統合は実装していない。次の Phase 162 では、R7 で検証した導出結果と既存の共通 Narrative Renderer の接続を先に監査する。新しい別系統の renderer を作らない。

### 検証方針

利用者指定により Phase 161 終了時にも repository-wide full pytest を行わない。局所検証は R2–R5 合計17件、R6 4件、R7+R6 回帰10件の PASS 報告がある（R6 は重複して実行されている）。全体テスト成功は主張しない。

