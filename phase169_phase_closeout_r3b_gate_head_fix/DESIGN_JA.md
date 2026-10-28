# Phase 169 Closeout R3B — 最終テスト報告 HEAD 互換修正

## 変更対象

新規パッケージ `phase169_phase_closeout_r3b_gate_head_fix/` 内の `run.py::inspect_report()` と、`tests/test_gate_head.py` を追加・更新対象とする。旧 R3 パッケージ・本番実装・既存 tests・主要文書の変換方針は変更しない。変更前後の `run.py` は `reviewed_sources/` に全文収録した。

## 原因と対策

旧 R3 は有効な R1 Gate 報告の Git HEAD を R10ET 基準コミットか現在の GitHub HEAD の二者に固定していた。監査専用パッケージの追加コミットを挟むと、レビュー済みの中間 HEAD で実行した R1 終了時 Gate が拒否される。`git merge-base` によって報告 HEAD が「基準コミット→レビュー済み HEAD」の祖先経路上にあることを検査し、合格の場合だけ受け入れる。Gate 成績・終了コード・対象件数・ログファイル・Git index 保全などの条件は緩めない。

報告書が見つからない場合、あるいは項目が不整合の場合には具体的な理由を表示して終了する。全体 pytest を再実行しない。報告の JSON を新規生成したり、値を捏造したりしない。

## 動作と安全性

実行前に GitHub とローカルの HEAD、tracked ファイルと R6 証拠の Git blob を照合し、最終 Gate の既存報告を確認する。成功した場合のみ主要文書5件を全文更新し、変更前後の全文をリポジトリ外へバックアップする。既存 API、Trust Boundary、Proof Tree、Reference の根拠を変えない。Git 操作の破壊的コマンドは使用しない。

## 検証と完了条件

R3B 限定テストは元の R3 の10件と、レビュー範囲内の中間 HEAD・両端・範囲外・テスト失敗・ログ欠損・報告欠損の追加7件を対象とする。Windows 実行で主要文書5件更新・Git index 不変を確認したとき、Phase 169 の検証済み範囲について文書上の終了記録を完成する。次 Phase の数学的未達事項は別途監査する。
