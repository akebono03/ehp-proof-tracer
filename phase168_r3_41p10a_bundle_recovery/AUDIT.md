# Phase 168 R3-41P10A — 一時 ZIP 占有エラーの修正

## 対象

- 修正するファイル：`phase168_r3_41p10_generic_replay_audit/run.ps1` の全文。
- 追加ファイル：`phase168_r3_41p10a_bundle_recovery/run.ps1`、`run_FIXED.ps1`、`README.md`、`AUDIT.md`、`tests/test_package.py`。
- アプリケーション本体、既存のテスト、Proof Tree、Renderer は変更しない。

## 原因

旧ランナーは監査資料 ZIP を `output/review_bundle.zip` へコピーした後、Dropbox 配下の `review_bundle.tmp.zip` を `Remove-Item` で削除していた。監査および限定テストの成功後、一時 ZIP のファイル占有により処理が異常終了した。

## 変更

- 一時 ZIP を作成しない。
- 圧縮対象を `output` 直下の通常ファイルだけに限定し、過去の `review_bundle*.zip` を除外する。
- 固定名 ZIP が占有されている場合は一意名の ZIP に保存する。
- `-BundleOnly` で既存の監査ログを再圧縮する。監査も pytest も再実行しない。
- 旧 `run.ps1` の SHA-256 を照合し、バックアップ後に置換する。未知の版は拒否する。

## R3-41P10 の結果

ユーザー環境のログでは推論39/39件再検証成功、偽推論2件拒否、限定 pytest 32件 PASS。P10A は検証方式の採用を決定しない。既存 GIVEN の真正性と文献順は、この監査の再検証対象外。

## 次工程との境界

R3-41P10A はレポート出力だけの修正。既存 matcher による一括再検証と、探索時に検証済みという provenance（由来）の引き継ぎの設計比較は、別の作業として扱う。全体 pytest は Phase 168 の最後にのみ実行する。
