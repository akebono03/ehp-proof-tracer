# Phase 174 R3-R7-R29：共通逆向き探索 Provider の接続

## 実装前に確認した既存コード

- GitHub `akebono03/ehp-proof-tracer` の `phase165_r3_recursive_search.py`：`GoalExpansion`、`reconstruct_registered_goal`、`SourceBoundGoal`。
- `phase165_r52_r9_shared_math.py`：`build_shared_typed_bridge` と `shared_expansion_provider`。
- `phase165_r6_2_unified_registry_r3_r3/provider_registry.py`：`UnifiedExpansionProviderRegistry`。
- R25 `rule.py`、R26 `bridge.py`、R28 `registration.py`、関連した R28 のテスト。

## 変更対象と追加位置

新規ディレクトリ `phase174_r3_r7_r29_prop27_canonical_provider` のみ追加。

- `provider.py` 新規：`expand_cited_prop27_goal`、`build_canonical_prop27_context`、`search_canonical_prop27_instance` をモジュール末尾へ順に追加。
- `audit.py` 新規：Source Guard と正規の逆向き探索の実測検査。
- `tests/test_provider.py` 新規：型・出典・親 ProofStep・不正な次元・推論候補を監査。
- `run.ps1` 新規：DryRun と限定 pytest。import mode は `importlib`。
- `README.md` 英語、`AUDIT_PLAN_JA.md`・`CODE_FULL_JA.md` 日本語。

既存のクラス、関数、import、公開 Web ルートは変更しない。新規 GIVEN・個別の GIVEN なし。

## 完了条件

1. Git develop 履歴と重要ファイルの改変検査 PASS。
2. 出典認証済み一般定理が共通 Registry に一意に入る。
3. 共通検索 API `reconstruct_registered_goal` が R25 と R28 の `InferenceRule` を逆向きに適用し、n=6 の出典付き ProofStep（GIVEN → INFERENCE → INFERENCE）を返す。
4. 限定 pytest PASS。全体 pytest は Phase の最後のみ。

## 次の Phase 境界

R29 は**正規の証明探索 API を用いる独立 Provider** まで。Web の既定 Provider の登録や根の全射性の証明は対象外。後工程で Web 接続と実際の根の推論候補を確認する。
