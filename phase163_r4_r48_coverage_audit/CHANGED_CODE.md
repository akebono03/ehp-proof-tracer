# Phase 163 R4-R48 変更一覧

## 追加ファイル

- `phase163_r4_r48_coverage_audit.py`：新規、既存108環境を変えずに TeX 内の未登録候補を調べる。関数 `clean_source`, `span_end`, `containing`, `classify_chapter`, `audit`, `write_report`, `main` はすべて新規で、ファイル先頭から末尾まで省略なく収録。
- `tests/test_phase163_r4_r48_coverage_audit.py`：新規、8件の限定テスト。全 import と全テスト関数を省略なく収録。
- `run.ps1`：新規、解凍後の実行用。
- `README.md`：新規、英語の実行説明。
- `CHANGED_CODE.md`：新規、日本語の変更説明。

既存のクラス・関数・import・ファイルは変更しない。既存 Registry と公開 API を変更しない。全体 pytest は Phase 終了時まで実施しない。

## 完了条件

108件の TeX カタログと source hash を再検証し、候補の位置・分類を出力すること。候補を確定済み命題として扱わないこと。元の ID とカタログを変更しないこと。

## 次 Phase との境界

R4-R49 は候補の人手審査・登録単位確定。R4-R48 は source 登録・新 ID 発行・証明探索接続を行わない。
