# Phase 173 R4-R15R16R3R1 設計

## 原因

`test_install_and_restore_preserve_staged_index` が追加行の期待値を `b"# tested patch\n"` に固定していた. Windows では Installer が適切に CRLF を維持するため、テストの期待値だけが不一致になった.

## 対象

変更は `phase173_r4_r15r16r3_staged_guard_fix/tests/test_staged_guard.py` の関数 `test_install_and_restore_preserve_staged_index` 内の比較式だけ.

## 方針

編集前バイト列に CRLF があれば CRLF を期待し、それ以外は LF を期待する. 本番 Installer や Verified Proof Tree / Common Narrative Renderer は変更しない.

## 安全条件

- Source Guard で `develop` の HEAD と系譜、テスト全文 SHA256 を検査.
- 既存のステージ済み内容は `git add`, `git reset`, `git commit` により変更しない.
- 修正対象テストのステージ内容と作業ツリーが不一致であれば中止.
- DryRun はリポジトリの既存テストファイルを変更しない.
- 失敗時にテストファイルを元の内容へ復元.

## 実施するテスト

- CRLF 対応テスト6件と追加契約テスト5件（計11件）.
- 元の R15R16R3 スクリプトの DryRun と限定 pytest.
- 全体 pytest は Phase 終了時のみ.

## 次の作業との境界

この修正は改行を原因とする偽陰性の除去だけ. 証明木と共通 Renderer の実運用・Reference 接続・Web 表示は R15R16R3 の限定テストとその後の表示監査で判断する.
