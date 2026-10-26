# Phase 169 R3J — 監査実装記録

## 変更対象

既存の本番コード・関数・import・テストは変更しない。

新規ファイル（リポジトリ直下へ展開）:

- `phase169_r3j_narrative_boundary_audit/audit.py`: `capture_actual_narrative()`, `split_narrative()`, `_inline_math_counts()`, `_step_report()`, `build_audit()`, `main()` を追加。
- `phase169_r3j_narrative_boundary_audit/tests/test_r3j_narrative_boundary_audit.py`: 監査用の新規テスト4件。
- `phase169_r3j_narrative_boundary_audit/run.ps1`: 事前検査・限定 pytest・監査を実行。
- `README.md`, `IMPLEMENTATION_NOTES.md`: 実行方法と境界。

関数全文と必要な import は `audit.py` とテストファイルに含む。`...` によるコード省略はない。

## 判断対象

- 完成した Proof Tree と Model、標準 Web Renderer の一致。
- Reference 各項目と実際に使われた ProofStep の対応。
- `π_4^2` 群構造の重複表示（証明経路の重複と表示の重複は区別）。
- 英語の `is surjective`, `is injective`, `is the zero map` の残存。
- `Chapter V, i)` の引用欄表示。文献を隠す変更ではなく、文体上の要望との差異として記録。
- `$E(\eta_2^2)=\eta_3^2$` が証明済みの型付き祖先に存在するか、表示が欠けているだけか。まだ追加しない。

## pytest と完了条件

`python -B -m pytest -q .\phase169_r3j_narrative_boundary_audit\tests\test_r3j_narrative_boundary_audit.py .\phase165_r14_r5_ehp_connection\test_phase165_r14_r5_ehp_connection.py`

完了条件: `R3J_FOCUSED_PYTEST_EXIT_CODE=0`, `R3J_AUDIT_EXIT_CODE=0`, `R3J_COMPLETE` が表示され、2つの出力ファイルが生成される。

次の R3K は、監査の結果に応じて本番 Renderer の文章規則と既存の限定テストだけを変更する。全体 pytest は Phase 169 の最後に実施する。
