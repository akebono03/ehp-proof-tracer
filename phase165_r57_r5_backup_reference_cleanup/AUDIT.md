# Phase 165-R57-R5 本番参照とバックアップ参照の分離

## 確認対象

GitHub の `toda_group_proof_narrative_renderer.py` と `test_phase165_r52_r11_common_renderer.py` などの関連テストを確認した。R57-R4 実行ログでは旧 `_phase159_render_pi_n_plus_1_n_stable_transport_narrative()` の削除がバックアップ3ファイルにある文字列参照で止まった。R57-R4 により、その補助関数を呼ぶ最初の公開 Renderer 定義はすでに削除済み。

## 変更対象（最初に確認する場所）

- `toda_group_proof_narrative_renderer.py`: 旧 `_phase159_render_pi_n_plus_1_n_stable_transport_narrative()` の**関数全体を削除**。import 変更なし、他の関数は変更しない。
- 新規 `phase165_r57_r5_backup_reference_cleanup/install.py`: 対象の AST 参照を検証し、ガード付き削除を行う。
- 新規 `test_phase165_r57_r5_backup_reference_cleanup.py`: 5件の対象テストを追加。

## 削除条件

1. 同じモジュールの残存 AST から対象関数への参照がない。
2. リポジトリ直下の本番 `.py` と `tests/` 内 `.py` に対象名への参照がない。
3. 該当する参照がバックアップ由来だけなら、バックアップを削除せず本番定義を削除する。
4. 最後の公開 Renderer 2定義（現在の公開入口と捕捉済み共通処理）は残す。

テスト・本番の参照が1件でもある場合はインストールを失敗させる。その他のサブフォルダーや動的 import は監査しきれないため、本番利用の完全な不存在を証明するものではない。

## 完了条件・次との境界

対象テストがすべて成功し、JSON 監査で対象関数が削除されたことを確認する。安定輸送の実際に稼働する専用分岐、旧互換 API の削除は行わない。全体 pytest は Phase 165 終了時だけ実行する。
