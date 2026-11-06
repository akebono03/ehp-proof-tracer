# Phase 174 R3-R7-R14 — 一般消滅関係の公開証明探索への接続

## 実装前監査

GitHub `akebono03/ehp-proof-tracer` の `develop`（`9a8a3e953fe7d3bc7d8d989188aef15525b3a414`）で、`phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` と `shared_expansion_provider()`、R12 の `source.py`・`rule.py` とそのテスト、R13 の提出 ZIP の文献 Bridge・関連テスト、既存の `source_first.py` と `unified_statement_registry.py` を監査した。R13 は実行ログで 347 件の限定 pytest PASS、隔離一般命題の GIVEN 1件と出典付き特殊化 INFERENCE 1件、公開の一般命題 GIVEN 0件を確認した。

## 変更対象

- 既存 `phase165_r52_r9_shared_math.py`：`build_shared_typed_bridge()` の既定 source 群に、R13 の出典付き一般命題 Bridge 1件を追加する。`shared_expansion_provider()` は、R12 の `expand_cited_annihilator_specialization()` を既存の `available` に対して呼ぶ。いずれも関数内部の import と追加呼び出しだけで、既存 API と既存分岐を変更しない。完全な置換後関数2本は DryRun により `MODIFIED_FUNCTIONS_FULL_JA.md` に全文を出力する。
- 新規 `phase174_r3_r7_r14_public_annihilator_connection/patch.py`：上記1ファイルの2か所だけを検証付きで編集し、バックアップと全文抽出を行う。
- 新規 `audit.py`：厳格な HEAD・Git Blob・R13 JSON・出典付き ProofStep 祖先を検査する。
- 新規 `tests/test_patch.py`、`tests/test_audit.py`、`tests/test_public.py`：差分アンカー、出典・報告の偽装拒否、公開側の型付き推論を検証する。
- 新規 `run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md` を追加する。

## 数学的境界

Toda (5.9) の一般命題「n >= 6 で ν_n ∘ η_{n+3} = 0」だけを FIXED_STATEMENT の出典付き GIVEN に登録する。具体的な `ν₆ ∘ η₉ = 0` は R12 の一般特殊化規則による INFERENCE であり、親 ProofStep が存在することを検査する。`π₁₂⁷ = 0` や具体的な零関係を GIVEN として登録しない。Proof Search は First Successful Proof Search を維持し、唯一性検査や群専用 Narrative を追加しない。

## 検証・完了条件・次段階との境界

DryRun は何も本番ソースに書き込まない。通常実行は元ソースの Git Blob SHA と挿入アンカーを検査してから更新し、直後の結合テストと監査が失敗すれば復元する。R14 の完了条件は、Source Guard・限定 pytest・一般文献 GIVEN 1件・型付き `n=6` 特殊化候補 1件・出典付き祖先関係の PASS である。これは `π₁₂⁷=0` の完成証明を意味しない。R15 以降で残る一般推論連鎖を別途検査し、全体 pytest は Phase 174 終了時のみに実行する。
