# Phase 173 R4-R1 — 対角群の出典付き推論修正

## 監査結果

最新 Root Match 監査では `ROOT_DIAGNOSIS=WRONG_PROOF_RULE`。4前提のうち第3前提 $\pi_7^7=\mathbb{Z}\{\iota_7\}$ のみ、既存規則の `INFERENCE` 要件に対し、直接採用された `GIVEN` だった。$H(\nu_4)=\iota_7$ は `INFERENCE` として成立している。

## 変更対象・追加位置

1. **既存ファイル** `phase173_r4_r1_source_bound_56/rule.py`：変更後の import 部分全文を含めて、既存 `expand_source_bound_toda56` 関数全体を置換。`source_bound_toda56_rule` など他の関数は変更しない。
2. **新規パッケージ** `phase173_r4_r1_diagonal_inference_fix/`：`replacement_rule.py`（既存ファイルの完全な置換内容）、`install.py`（`git`、`blob_hash`、`normalize_line_endings`、`proposed_bytes`、`preflight`、`install`、`main`）、`verify.py`（`run_verification`、`main`）、`run.ps1`、`tests/test_install.py`、`tests/test_scoped_diagonal.py`、文書を追加。

## 修正の論理

既存の `expand_cited_general_specialization(diagonal, available)` が提供する Toda (5.1) の一般形とその子目標を、出典 `locator=(5.1)` のスクリーン済み固定文献 `GIVEN` で照合する。その引用命題を `SourceBoundGoal(diagonal, diagonal_source)` に渡す。このラッパーは `reconstruct_registered_goal` にある既存仕様であり、DB 由来の直接 `GIVEN` や別の証明経路を採用せず、指定の一般形からの推論のみを受理する。

Root の `premise_patterns` と `match_guard` は変更しない。先行結果 $\pi_6^3$、Proposition 4.4、Lemma 5.4 の推論は変更しない。一般形が一意でない場合、出典照合が失敗した場合は候補を生成しない。

## 実行テスト

DryRun: `python -m pytest -q -p no:cacheprovider phase173_r4_r1_diagonal_inference_fix/tests/test_install.py`

本実行: `python -m pytest -q -p no:cacheprovider phase173_r4_r1_diagonal_inference_fix/tests/test_scoped_diagonal.py phase173_r4_r1_source_bound_56/tests/test_rule.py phase173_r4_r1_lemma54_source_bridge/tests/test_source.py`

インストール後に `python -m phase173_r4_r1_diagonal_inference_fix.verify` で一時的な公開相当の引用条件における Proof Search を実行する。全体テストは Phase 173 終了時だけ。

## 完了条件

- ソースおよび Git blob のガード PASS。
- 対角群を `INFERENCE` で導出し、その前提が Toda (5.1) の引用済み一般形である。
- Toda (5.6) の最終 Root が `INFERENCE` になり、`COMPLETE=True`・`DIAGONAL_INFERENCE_CERTIFIED=True` になる。
- まだ Web 表示経路には常設接続していない。これを R4-R1 の次段階とする。
- $\pi_8^5$ の群構造と位数8は R4-R2 の範囲。
