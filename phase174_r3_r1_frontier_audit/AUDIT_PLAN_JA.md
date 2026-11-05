# Phase 174 R3-R1 — 公開証明探索の Subgoal 監査

## 変更対象と追加位置

今回、既存のソースファイル・クラス・関数・メソッド・import・テストは変更しない。
次のファイルをリポジトリ直下の新規ディレクトリ `phase174_r3_r1_frontier_audit/` に追加する。

- `__init__.py` — 監査パッケージ。
- `audit.py` — 監査用関数を新規追加。`validate_r2_record`, `describe_first_two_hops`, `inspect_live_frontier`, `verify_against_r2`, `main` などは全文収録。
- `tests/__init__.py` — テストパッケージ。
- `tests/test_audit.py` — 新規テスト５件を全文収録。
- `run.ps1` — 既知 HEAD、原文・実装・関連テストの Git Blob SHA、既存 R2 レポートを検査し DryRun／通常実行を行う。
- `README.md`（英語）と本ファイル（日本語）。

## 背景

R2 実測では、公開 `pi_8^5` の Citation Gate 通過前提27件、
Root Proposal３件（有限巡回構造２件、等式対称性１件）、Subgoal 各１件、
新規 ProofStep は０件だった。

## 実行内容

1. R2 JSON が、旧コミット `3558d713` で生成された原本であると確認する。
2. 現行の `shared_expansion_provider` と同じ Citation Gate で Root Proposal を再構成する。
3. R2 レポートと候補の順序、Rule 名、Subgoal の型と `repr`、GIVEN の有無を照合する。
4. 各 Subgoal について２段目の探索候補、循環依存、直接引用可否を記録する。
5. JSON を `%LOCALAPPDATA%` に保存する。本番コードや主要５文書は変更しない。

`SourceBoundGoal` は情報表示のために一時的に内部目標を取り出すが、
本番の `source-bound` 証明義務を解除しない。
`GIVEN=True` は対象と文字列・型が一致する引用を示すだけであり、
`SourceBoundGoal` に対して推論が完了したことを意味しない。

## 実行する限定 pytest

```powershell
python -B -m pytest -q -p no:cacheprovider `
    phase174_r3_r1_frontier_audit/tests/test_audit.py `
    phase174_r2_source_math_audit/tests/test_audit.py `
    test_phase165_r55_nk_only_goal.py
```

## 完了条件と次 Phase との境界

- Source Guard、R2 Provenance Guard、R2 との Root Match、限定 pytest が全 PASS。
- 既存 Git index・作業ツリーが不変。
- 原文で既知の `2\nu_5=E^2\nu'`、(4.8) の条件、先行群の
  再利用可能性について、欠落している具体的な Goal を読めること。
- ここでは型付き推論規則を追加せず、`GIVEN` と完全証明を捏造しない。
- 根拠が得られた後の R3-R2 で、汎用規則の最小修正を検討する。
- 全体 pytest は Phase 174 完了時のみ実行する。
