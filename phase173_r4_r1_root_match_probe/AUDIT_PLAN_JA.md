# Phase 173 R4-R1 — Root Match 詳細監査

## 現状

- 直前の限定 pytest は21 PASS、Source Guard は PASS。
- Lemma 5.4 の citation-screened typed source は1件。
- $H(\nu_4)=\iota_7$ の候補、Toda (5.6) の Root Candidate が生成済み。
- $\pi_7^4$ は `partial` のまま。`OPEN_GOALS` は最上位結論とその対称性を記録している。
- 最終規則の照合失敗か、4前提のうち実際に採用されないものがあるか、ログだけでは判定不能。

## 変更対象

新規ディレクトリ `phase173_r4_r1_root_match_probe/` のみ。

- `audit.py`：`_git`、`only_audit_additions`、`guard_sources`、`summarize_premise_states`、`inspect_runtime`、`main`（すべて新規関数）。
- `tests/test_audit.py`：診断分類・ソース差分保護の限定テスト14件。
- `run.ps1`：テスト・DryRun・本実行コマンド。
- `__init__.py`、`tests/__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`：新規ファイル。

既存関数・クラス・import・API・本体ファイルは変更しない。

## 実装内容

1. Git の開発ブランチ、現在のソース Git blob、作業ツリー、および直前パッケージの `source.py` / `audit.py` の SHA-256 を確認する。
2. 直前と同一の citation screen（引用選別）および追加 Provider を組み立て、公開の `search_shared_group_goal()` を実行する。
3. `result.proven_steps` から4前提と同一の結論を持つ実際に採用された ProofStep を検索する。
4. 各前提について採用件数・`ProofRule`・既存 `PremisePattern` の一致を記録する。
5. 4件揃った場合に限り、既存 `match_guard` と `find_inference_matches_for_rule` を呼び出す。推論結果の結論も一致検査する。
6. 出力を `$LOCALAPPDATA/EHPProofTracerRecovery/phase173_r4_r1_root_match_probe/audit.json` に保存する。

## 成功条件と境界

- DryRun で `PHASE173_R4_R1_ROOT_MATCH_DRY_RUN=PASS`。
- 本実行で `PHASE173_R4_R1_ROOT_MATCH_AUDIT=PASS`。
- `PREMISE_1..4_STATE`、`ROOT_GUARD_ACCEPTS`、`ROOT_MATCH_COUNT`、`ROOT_DIAGNOSIS` を出力。
- 既存 ProofStep からの照合を観測するだけで、完成証明・出典文献・DB を書き換えない。
- 原因が判明してから最小限の規則修正または前提接続を行い、Phase 173 R4-R1 の公開完成証明を目指す。
- $\pi_8^5$（R4-R2）は対象外。全体 pytest は Phase 173 の最後のみ。
