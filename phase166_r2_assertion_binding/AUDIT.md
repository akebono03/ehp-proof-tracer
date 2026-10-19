# Phase 166 R2 — 命題構成要素と型付き関係式の候補対応監査

## 目的

Toda (5.3) の `boundary:(5.3):nu_prime_double_relation` と、前工程で構築した `Relation` との候補対応を、**本番コードを変更せず**記録する。

## 事前確認

GitHub の `expression.py`、`proof.py`、`unified_statement_registry.py`、`toda_literature_statement_boundary.py`、`phase163_r4_registry_bridge.py`、関連する `tests/test_expression.py`、`tests/test_repository.py`、`tests/test_phase165_r2_registry_lookup.py` と、直前の `phase166_r2_typed53/audit.py` を確認した。

## 変更対象と追加位置

新規ディレクトリ `phase166_r2_assertion_binding/` に `audit.py`、`test_audit.py`、`run.ps1`、`README.md`、`AUDIT.md` を追加。既存ファイル・クラス・関数・import は変更しない。

新規関数 `candidate_binding()`、`inspect()`、`main()` は新規 `audit.py` 内に配置。テスト関数は新規 `test_audit.py` に配置。いずれもファイル全文を配布している。

## 判定境界

- `AssertionInstantiation` は「識別子と候補内容の対応」を表すだけで、登録命題の元の `content` を変更しない。
- `TodaFixedStatementComponent` は主張を識別するメタデータで、`Relation` 自体ではない。
- `composition` と `rep_linear` の表示一致だけでは数学的同一性の証明とはならない。
- `ProofStep` と `ProofStepLink` は作成しない。引用資格の審査は R3 に留保する。
- CSV と前工程の予想件数が変化した場合は停止する。

## 限定 pytest

`python -m pytest -q phase166_r2_assertion_binding/test_audit.py`

## 完了条件

2件の表示一致候補を正しい個別主張 ID に関連付けて記録すること。数学的内容一致・証明資格付与は0件のままであること。本番コード不変更、全体 pytest 未実施。

## R3 との境界

この工程は候補対応の監査のみ。引用可否の判定、Proof Tree への挿入、一般規則の逆向き適用は実施しない。
