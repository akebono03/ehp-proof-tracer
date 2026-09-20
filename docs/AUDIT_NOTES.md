# 文書監査概要 — 2026-08-25

## 主な訂正

1. 当時の長文文書は詳細な現行履歴が概ね Phase 5-36 までしかなく、コードとテストは Phase 5-65 まで進んでいた。

2. 次のような過去の記述は当時は正しかったが、現在の制約ではなくなっていた。

   - greedy premise matching
   - pattern variable なし
   - shared binding なし
   - substitution なし
   - 型だけに基づく premise combination

3. 当時の実装には次が既に含まれていた。

   - exhaustive deterministic backtracking
   - `PatternVariable` / `VariableBinding`
   - relation-pattern matching
   - repeated-variable consistency
   - premise 間の shared binding
   - `InferenceMatch` に保存される bindings
   - `conclusion_pattern` substitution
   - 異なる binding assignment からの異なる conclusion
   - multiple-rule multi-round propagation
   - branch / merge fixed-point inference

4. Phase 5-65 は明示的に

   ```text
   generic inference engine foundation completed
   ```

   と扱うことにした。

5. Phase 6 は

   ```text
   EHP domain inference rules
   ```

   と定義した。

6. 当時の制約一覧は、Phase 5-65 時点でも実際に残っているものだけへ書き換えた。

   - 通常の Python conclusion equality
   - knowledge state における alternative proof collection の first-class 表現なし
   - 完全に一般的な recursive unification language なし
   - unbound conclusion variable は `None` に置換
   - indexing / pruning のない combinatorial exhaustive search
   - `max_rounds` は semantic cycle detection ではない

7. 当時アップロードされた inference-rule suite を再実行し、

   ```text
   423 passed
   ```

   を確認した。

   これはプロジェクト全体の test-suite 件数としては扱わない。

## 文書改訂後の役割

- `README.md`: 現在の capability と状態
- `docs/design.md`: 現在の architecture と設計規則
- `docs/development_log.md`: 時系列の開発履歴
- `docs/roadmap.md`: 今後の計画
- `docs/proof_records.md`: 数学的証明と証明基盤の記録索引

## 2026-09-21 追記

Phase 106 完了後、主要文書の言語も再監査した。

日本語文書では、API名、クラス名、関数名、状態名、数学用語、一般に定着した技術語を除き、説明文と見出しを日本語へ統一する。

`README.md` はプロジェクト規約により英語を維持する。
