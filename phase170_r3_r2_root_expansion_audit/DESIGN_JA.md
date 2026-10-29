# Phase 170 R3-R2 — 根元 Goal 推論候補監査

## 変更対象と追加位置

変更対象は新規 `phase170_r3_r2_root_expansion_audit/` のみ。
既存コード、命題台帳、CSV、テスト、文書を変更しない。

- `audit.py`：新規ファイル。全 import と定数の後に `clipped`、`load_reviewed_r3_code`、`check_reports`、`evaluate_root_proposals`、`classify_root_evidence`、`inspect_case`、`render_markdown`、`run`、`main` をこの順に定義する。
- `run.ps1`：新規実行入口。
- `tests/test_audit_contract.py`：新規テスト関数を追加する。
- `README.md`：英語で操作説明。
- `DESIGN_JA.md`：日本語で安全境界の明記。
- `__init__.py`：新規パッケージ定義。

新規関数の全文と import 全文は、それぞれ上記の新規ファイルに収録する。

## 調査する内容

1. R1/R2/R3-R1 の完了済み記録・HEAD・入力同一性。
2. 位置付き Citation ID のある3-stem と独立出典審査経路の4-stem の差。
3. R3-R1 と同じ Goal を現行の本番 Goal selector から再取得。
4. 出典のスクリーニングと `prefer_universal_prop42_derivation` を通した共通 provider の根元 Goal に対する提案。
5. 提案された推論規則と下位 Goal（型・表現・直接 GIVEN としての利用可否）。

分類は `NO_ROOT_EXPANSION_PROPOSED`、`ROOT_EXPANSIONS_WITH_UNPROVED_SUBGOALS`、`ROOT_EXPANSIONS_PRESENT_REPLAY_UNRESOLVED` に限定する。
前者は推論接続が見つからないこと、後二者は推論候補はあることを示すだけである。
いずれも数学的な命題不存在・証明不能・Trust PASS を意味しない。

## 安全性と完了条件

- R3-R1 の監査コード SHA-256 とレビュー済み本体ソース blob を再確認する。
- `develop` と R1/R2/R3 の記録を照合し、未知の本体変更を拒否する。
- Python `-B` と pytest `-p no:cacheprovider` を用いる。
- R1/R2/R3 の既存報告を変更せず、出力はリポジトリ外に新規作成する。
- 5群の根元 Goal 推論候補がすべて採録され、既存 Git tracked/index が不変なら R3-R2 の監査実行 PASS。
- full pytest は実行しない。新規推論規則・新規数学的機能・Renderer 修正は Phase 170 R3-R2 の対象外。
