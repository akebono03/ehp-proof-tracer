# Phase 166 R3-Q 参照命題監査

## 変更対象

本番ファイル、クラス、メソッド、既存テストの変更はありません。

- 新規 `phase166_r3q_reference_audit/audit.py`：`contains_relation()` と `main()` を新規ファイルに全文追加。
- 新規 `phase166_r3q_reference_audit/run.ps1`：読み取り専用の監査コマンド。
- 新規 `README.md`、`CHANGED_CODE.md`。

## 確認事項

- 登録済みの $\pi_3^2$ に対応する主張 ID と文献位置。
- 以前の参照審査で残った前提と、掲載順審査で除外された前提。
- `component_position=None` の分解済み主張数。
- 通常の $\pi_3^2$ 証明の状態。

## テストと完了条件

コード変更は行わず、読み取り専用監査の終了コード0と `audit.json` 作成を完了条件にします。全体 pytest は Phase 166 終了時のみ。次工程では監査によって確認された原因だけを修正し、他の機能追加はしません。
