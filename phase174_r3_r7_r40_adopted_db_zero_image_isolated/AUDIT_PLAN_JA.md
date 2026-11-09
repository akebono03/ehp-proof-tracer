# Phase 174 R3-R7-R40 監査設計

## 結論

R39 の `E(ν₅η₈²)=0` は Toda (5.9) を親に持つ `INFERENCE` で導出済み。一方、`π₁₀⁵=Z/2{ν₅η₈²}` の DB prior は `GIVEN` としてのみ採用され、R6 の「両方 INFERENCE」条件では全体零像へ進めなかった。

R40 では **既存の R6 を変更しない**。次の別規則のみを隔離追加する。

$$
\begin{gathered}
\pi_q^n=\mathbb Z/m\{g\}\quad\text{（独立に検証された採用済み DB prior）},\\
E(g)=0\quad\text{（検証済み INFERENCE）}\\
\Longrightarrow\operatorname{im}(E:\pi_q^n\to\pi_{q+1}^{n+1})=0.
\end{gathered}
$$

DB prior を Toda の出典に偽装せず、`ProofRule.GIVEN` と `ADOPTED_DATABASE_PRIOR` の note をそのまま祖先に残す。

## 新規変更対象（既存ファイルは変更なし）

- `phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py`: `verified_prior_zero_image_inputs`, `adopted_prior_zero_image_rule`, `expand_adopted_prior_zero_image`（全て新規）。
- `source_guard.py`: SHA と develop 履歴の検証。R39 統合のみ許可。
- `audit.py`: R39 の実際の Toda (5.9) → 生成元零像の推論連鎖を再生し、採用済み DB prior との一般推論結果を構成。`GIVEN` の昇格は禁止。
- `tests/test_rule.py`, `tests/test_audit.py`, `tests/test_guard.py`, `tests/test_static.py`: 限定回帰テスト。
- `run.ps1`: DryRun、実行、限定 pytest。

## 完了条件

Source Guard PASS、実際の R39 先行出典検証 PASS、DB prior の先行順序・真正性 PASS、DB 親を `GIVEN` のまま保持する `ImageZeroStatement` の `INFERENCE` 成立、限定 pytest PASS。全体 pytest は Phase 終了時のみ。

## R41 との境界

R40 では共通 Provider に接続しない。最終目標 $\pi_{12}^{7}=0$ と上側 $\Delta$ 全射性もまだ未証明。R41 は source-first screening（出典の適格性確認）と DB adoption（先行データの採用）を経由する共通 Provider 接続を対象とする。
