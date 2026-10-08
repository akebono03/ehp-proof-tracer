## Phase 161 — Concrete Backward-Driven Reconstruction（完了：focused 検証のみ）

当初の unstable proof audit を具体的な不足能力の監査へ絞り、$E:\pi_4^2\to\pi_5^3$ の同型性を目標とする Backward Goal Schema（逆向き目標スキーマ）と証明再構築の縦断経路を実装した。

- R1：既存7規則の入力・結論・guard 実体監査。
- R2：同型性から単射性・全射性への分解。
- R3：EHP 完全性の4つの窓を保持した逆向き展開。
- R4：文献由来の既存 `ProofStep` の構造的照合。
- R5：7規則を前向きに適用する、目標依存の証明再構築。
- R6：前提除去・依存関係・祖先未検証の制限監査。
- R7：推論祖先と承認済み `GIVEN` を検証する別入口。

局所テスト報告：R2 3 PASS、R2–R3 7 PASS、R2–R4 11 PASS、R2–R5 17 PASS、R6 4 PASS、R7 と R6 回帰10 PASS。全体 pytest は利用者指定により **Phase 161 でも実行しない**。Phase 161 の終了は full-suite all-pass の主張を伴わない。

### Phase 162 — Reconstructed Proof Narrative Connection（次の作業）

R7 の検証済み `ProofStep` を既存の共通証明表示経路へ接続できるか監査し、$E:\pi_4^2\to\pi_5^3$ の文章表示を確認する。Reference（一般形の文献命題）と Proof（具体的適用）を分離し、証明末尾の $\square$ 等、既存の表示規則を保持する。まず実出力の数学的順序と重複を確認し、必要最小限の修正だけを行う。新しい renderer や未確認の一般規則は先取りしない。

### その後の一般化

任意の非安定目標への規則選択、文献検索、一般的な EHP Goal Schema、より広い provenance trust policy は後続の設計監査対象とする。Phase 161 の具体的目標が成功したことを、任意目標での自律探索の完成とは扱わない。

