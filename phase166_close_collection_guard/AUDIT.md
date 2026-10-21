# Phase 166 全体テスト収集対策

## 変更対象
- 新規 `phase166_close_collection_guard/close.py`: `main()` 全文を収録。
- 新規 `phase166_close_collection_guard/run.ps1`。
- 新規 `README.md` (英語)、`AUDIT.md` (日本語)。

## 範囲
現行 GitHub `develop` の `phase165_r6_8_eta_name_fix/install_and_test.py` を確認。pytest の標準パターン `*_test.py` に一致するが、モジュール先頭レベルで本番ファイル書き換えを含むため通常のテストではない。収集からこのファイルのみ除外する。一般のテストを追加で無効化しない。実行後 `summary.json`, `pytest_full.log`, `git_before.txt`, `git_after.txt` を保存する。

## 終了条件
除外した1ファイルを明記した全体 pytest の終了コードが 0。その他の障害があれば Phase 166 完了は保留。

## Phase 167 との境界
証明文章や探索規則は変更しない。Phase 167 では π₄³、次に π₅³ の証明を調べる。
