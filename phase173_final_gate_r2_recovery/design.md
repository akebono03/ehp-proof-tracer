# Phase 173 最終 Gate R2 — 失敗記録を保持した再検証

## 目的と背景

Phase 173 の第1回終了 Gate は、現行 `tests/` において `3541 passed, 5 failed`、終了コード1となった。失敗は Phase 167 の3テストファイル内の5テストであり、旧 Reference / 証明の見出し区切りを前提として `StopIteration` が発生した。

R1 は、本体の数学的推論や Renderer（表示器）を変えずに3テストファイルの区切り判定だけを修正した。ユーザーのローカル実行では R1 のパッチ契約 9 PASS、対象の限定 pytest 6 PASS、Git index 保持 PASS を確認した。

R2 は、その修正後のアクティブ全体 pytest を**訂正実行として一度だけ**実施し、第1回の失敗を改竄せず独立した証拠として記録する。

## 変更対象・処理の境界

新規の `phase173_final_gate_r2_recovery/` ディレクトリのみを追加する。既存のコード、Reference ルール、Proof Tree（証明木）、Narrative Renderer（文章表示器）、テスト本文は変更しない。

- `gate.py`：Git/SHA 検査、旧失敗ログの検査、実行回数の排他制御、成功／失敗レポートの保存。
- `run.ps1`：DryRun と通常実行を分岐し、通常実行時だけ現行 `tests/` の全体 pytest を起動。
- `reviewed_test_replacements/`：R1 の3テストファイルの審査済み全文を保存し、改行形式を除く SHA-256 を固定。
- `tests/test_gate_contract.py`：この監査 Gate 自体の限定テスト。
- `README.md`、`design.md`、`FULL_CHANGED_UNITS.md`：操作・設計・新規コードの全文。

## 実行前の必須条件

1. `develop` のローカル HEAD と `origin/develop` が一致し、審査済み HEAD `ac9149beaf91eeef382bc816234bd2d895398667` の子孫である。
2. その HEAD からの追跡差分は、3つの審査済み Phase 167 テストか終了 Gate の補助ディレクトリに限定する。
3. 既存の15個のソース／文書 Git Blob が変わっていない。
4. 作業ツリー上の3つの修正済みテストは、R1 でレビューした内容と一致する。それ以外の追跡変更やステージ済み変更はない。
5. 第1回終了 Gate の JSON と stdout／stderr／attempt はすべて存在し、HEAD、終了コード1、5件のテスト名、`5 failed, 3541 passed` が一致する。

第1回 Gate のファイルは読み取り専用として参照し、上書きも削除もしない。

## Gate の実行と判定

DryRun は上の条件と Gate の限定 pytest だけを確認し、全体 pytest を起動しない。通常実行では R2 専用の `attempt.json` を排他的に新規作成した後、以下のコマンドを一度実行する。

```powershell
python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests
```

終了コード0、pytest の最終集計 `3546 passed`、実行前後の Git index 同一性が必要である。結果は `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_final_gate_r2\` に新規保存し、成功済みなら再実行しない。新しい失敗を記録した場合も独立した R2 レポートを保存して停止する。

## 認定範囲と次工程

PASS は Phase 173 終了時の**アクティブ `tests/`** の合格であり、退避した歴史的テストすべて、未登録のホモトピー群、未証明の記名生成元の一般解決を意味しない。

特に $\pi_{12}^{4}\cong\mathbb{Z}/2$ の抽象群構造の証明は $\pi_{12}^{4}=\mathbb{Z}/2\{\varepsilon_4\}$ という記名生成元の証明ではない。$\pi_{13}^{4}$、$\pi_8^5$ の未完成も維持する。

成功後に主要5文書へ第1回の失敗、R1 修正、R2 全体テスト結果と認定境界を記録し、最終レビューを経て Phase 173 を正式終了する。今回の ZIP は文書を書き換えたり正式終了を宣言したりしない。
