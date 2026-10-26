# Phase 169 R3X — 監査の範囲

変更対象の本番ファイル・クラス・関数・メソッド：**なし**。

新規ファイル・関数：

- `phase169_r3x_source_bound_eta_probe/audit.py`：`examine()`、`main()`（全文収録）。
- `phase169_r3x_source_bound_eta_probe/tests/test_phase169_r3x_source_bound_eta_probe.py`：3つのテスト関数と fixture（import を含め全文収録）。
- `phase169_r3x_source_bound_eta_probe/run.ps1`：読み取り専用監査・限定 pytest。

R3W が確認した2つの正当な証明経路（(4.5) による安定輸送、Proposition 5.1 の一般命題特殊化）はいずれも保存する。R3X は `expand_registered_eta_specialization()` と公開済み `reconstruct_registered_goal()` を組み合わせ、指定された出典に限った下位目標の証明が一意かを監査するだけである。新規 GIVEN は生成しない。

## 完了条件

1. 出典限定で $\pi_6^5=\mathbb Z/2\{\eta_5\}$ の実際の INFERENCE が1件生成され、引用済み Proposition 5.1 の GIVEN のみを前提にする。
2. 引用を除外すると監査用 Provider は fail closed（未解決）となる。
3. 公開の Provider には2つの独立経路が残り、$\pi_5^3$ の完成証明は維持される。

次工程との境界：この監査は Hopf 全射性に新しい ProofStep を追加しない。追加は出典限定解決の仕組みと併せて後続工程とする。全体 pytest は Phase 169 の最後のみ。
