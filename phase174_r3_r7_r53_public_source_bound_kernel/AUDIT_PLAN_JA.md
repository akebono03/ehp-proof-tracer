# Phase 174 R3-R7-R53 実装・監査計画

## 実装前に確認した現行 GitHub

- `develop` HEAD: `1151d6a3044fd7fae2ff1fb864a83afdaefc285d` （R52・R52R1・R52R2 を収録）。
- `phase165_r55_nk_only_goal.py`: 零群の標準公開探索を `search_registered_partial_proof` に接続。
- `phase165_r52_r9_shared_math.py`: 一般の R35 KernelMultipleStatement 候補を共有供給。
- `phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py`: 3前提のうち始域 `Relation` が INFERENCE であることを要求。
- `phase174_r3_r7_r52_public_kernel_source_bound_probe/probe.py`: 出典付き `SourceBoundGoal` の候補を優先すると根零群が complete（ユーザー実測28 ProofStep）になることを確認。
- `phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py`、`phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py`、R35/R36/R50 の関連 pytest を確認。

## 変更対象

既存ファイル **1件**:

- `phase165_r55_nk_only_goal.py` の関数 `search_group_from_registered_goal()` **全体**（変更後全文は `CHANGED_FUNCTIONS_FULL.py`、本書 `CODE_FULL_JA.md` に収録）。
- 変更する top-level import はなし。関数内 import は変更後関数に全文収録。

新規ファイル（**追加位置はリポジトリ直下** `phase174_r3_r7_r53_public_source_bound_kernel/`）:

- `provider.py`: `cited_inferred_domain_sources()`、`build_public_source_bound_kernel_provider()`。
- `source_guard.py`: `git()`、`git_bytes()`、`git_blob()`、`normalized()`、`verify_checkout()`。
- `install.py`: `function_source()`、`patched_source()`、`prepare()`、`apply()`、`main()`。
- `audit.py`: `inspect_public_root_completion()`、`main()`。
- `tests/test_static.py`、`tests/test_guard.py`、`tests/test_public.py`：新規テスト関数一式。
- `__init__.py`、`run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、`CODE_FULL_JA.md`、`CHANGED_FUNCTIONS_FULL.py`。

## 数学的信頼境界

1. Source-first（出典優先）: `FIXED_STATEMENT`、引用元の真正な `ProofStepLink`、出版位置、既存推論規則の実照合を全て検証。
2. R35 `InferenceRule` は変更しない。Domain の直接 GIVEN による不正解決を禁止し、出典付き `SourceBoundGoal` を優先候補にする。
3. First Successful Proof Search（最初の成功で終了）を維持。元の候補は fallback として保持。唯一性検査は行わない。
4. n/k ごとの専用分岐なし。一般の `KernelMultipleStatement` の型だけで追加候補を判定。
5. 共通 Narrative Renderer・ProofNarrativeModel は変更しない。完成判定は既存の Web trust boundary（証明木検証）を通す。

## 限定 pytest・完了条件

- 8 グループの限定 pytest: R53 STATIC/GUARD/PUBLIC、R52 PROBE、R51 PUBLIC、R50 FRONTIER、R36 KERNEL、R35 RULE。
- Source Guard・DryRun・実行監査 PASS。ユーザー実行で `PUBLIC_STATUS=complete`、`PUBLIC_ROOT_COMPLETE=True`、`PUBLIC_WEB_KEY=generic-complete-proof`、`PUBLIC_ROOT_SIX_CITED_ANCESTORS=True`、`PUBLIC_OPEN_GOAL_TYPES={}` を確認。
- R53 はブラウザ HTTP の実通信を認証しない。R54 に公開 HTTP Gate を分離する。
- 全体 pytest は Phase 174 最終工程のみに実施。
