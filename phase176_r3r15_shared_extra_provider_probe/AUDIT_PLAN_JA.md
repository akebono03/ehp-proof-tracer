# Phase 176 R3R15 監査計画

## 目的

既存の `shared_expansion_provider(extra_providers=...)` に独立監査済みの2規則を明示的に渡し、共有候補生成 API を経由して候補が現れるか確認する。公開の共有 Provider の恒久登録や群構造の完成は、この工程の対象外。

## 変更対象

新規 `phase176_r3r15_shared_extra_provider_probe/` 以下のみ。

- `provider.py`: `build_screened_extra_provider`（新規関数）。出典審査済みの Lemma 5.7 と一般的右合成零像規則を候補として提案する。ProofStep や GIVEN を作らない。
- `audit.py`: `git`, `preflight`, `observe`, `report_path`, `execute`, `main`（すべて新規）。
- `tests/test_provider.py`: 新規の型・出典境界の限定テスト。
- `run.ps1`: DryRun、本実行、限定 pytest。pytest cache は無効。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`（日本語）。

## 監査条件

- develop が検査済み HEAD `dc67a7c79ac483b3c9dbf014fcd26171dfa2b6b2` の子孫である。
- 追跡ファイルに未コミット変更がなく、参照コードと Toda 原典の anchor が存在する。
- 出典付き GIVEN は `screen_independent_sources_for_derived_goal` の採用結果1件に限る。
- 基礎の零像目標と右合成後の零像目標に、それぞれ適切な GoalExpansion が1件できる。
- 無関係な根 Goal の候補列は変化しない。
- 本番共有 Provider を変更しない。新規 GIVEN 0、公開数学規則追加 0。

## 検証と次 Phase 境界

DryRun、本実行、限定 pytest がすべて PASS した場合、共有 API の候補受理までを確認する。実際の公開探索の登録と残る群構造の Goal 監査は次工程に分離し、全体 pytest は Phase の最後まで実施しない。
