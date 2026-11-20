# Phase 176 R3R14 監査計画

## 目的

R3R13で確認された二つの共有探索未接続境界について、出典優先・型検査を維持した独立の二段階候補生成器で接続を検証する。既存公開コードは変更しない。

## 監査対象

1. Toda Lemma 5.7 の出典付き `E(\eta_2\circ\nu')=0` を通常の GIVEN と区別して、推論ステップとして導出する。
2. 合成の前半部分を型から取得し、`E(a)=0` から `E(a\circ b)=0` を推論する。
3. 両者を一本の証明木に接続し、最終 ProofStep の根拠関係を検査する。
4. 通常の公開候補が未変更で、対象群の証明が依然未完成であることを記録する。

## 変更対象と追加位置

リポジトリ直下に新規ディレクトリ `phase176_r3r14_isolated_two_stage_provider/` を追加する。

- `provider.py`: 新規関数 `preceding_zero_image`、`build_isolated_two_stage_provider`。
- `audit.py`: 新規関数 `git`、`preflight`、`observe`、`report_path`、`execute`、`main`。
- `tests/test_provider.py`: 新規テスト4件。
- `tests/test_audit.py`: 新規テスト2件。
- `run.ps1`: DryRun、本監査、限定pytest用。
- `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`: 全文収録。

既存ファイル・既存クラス・既存関数の変更はない。

## 判定条件

DryRun、本監査、限定pytestが成功し、出典付きの基礎零像ステップと右合成零像ステップの双方が `ProofRule.INFERENCE` であること。公開 Group Query の証明完成は要求しない。

## Phase 境界

R3R14では公開共有探索への登録をしない。公開接続と残余Goal監査は後続工程に限定する。全体pytestはPhase末尾にのみ実施する。
