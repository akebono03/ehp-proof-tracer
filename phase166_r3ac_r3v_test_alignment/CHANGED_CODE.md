# Phase 166 R3-AC 回帰テスト修正

- 変更ファイル: `phase166_r3v_test_repair/test_r3v.py`
- 変更関数: `test_r3v_registered_prior_and_shared_search_connection()`。関数全文は `install.py` が `modified_test_function.txt` に出力。
- import: 既存 import を変更しない。
- 本体コードは変更しない。
- 従来の型付き登録命題を実際に使用し、推論候補の source generator と inference guard を検査する。
- 限定 pytest: `phase166_r3v_test_repair/test_r3v.py` と `phase166_r3ac_stable_notation/test_r3ac.py`。
- `phase166_r3ab_pi65_audit.audit` を再実行して pi6^5 の状態を確認する。COMPLETE は現時点では未確認。
- 全体 pytest は Phase 166 の最後にのみ実行する。
