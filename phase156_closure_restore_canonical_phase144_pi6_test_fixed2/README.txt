Phase156 closure — canonical Phase144 pi6 test restore

対象
====
tests/test_phase144_6_pi6_generic_production_route.py

Production changes
==================
なし。

原因
====
ローカル対象 test file が現行 HEAD より古かった。

全体 pytest のログでは4 tests が収集され、そのうち

- actual == expected の旧完全一致 test
- Japanese punctuation `、` を固定する旧 CLI expectation
- stale static route source-inspection test

が失敗した。

GitHub develop HEAD
===================
baab9402c9ca8c5051268d5d334591ea44b5b273

現行 HEAD の対象 file は3 tests。

Phase155 では stale static route test は削除済みであり、
残る古い表示期待値も stale expectation repair の対象として整理済み。

変更
====
対象 test file を

git show HEAD:tests/test_phase144_6_pi6_generic_production_route.py

の全文で置き換える。

置換前 file は

phase156_closure_test_restore_backup/
test_phase144_6_pi6_generic_production_route.py

へバックアップする。

完了条件
========
- restore 後の git status が clean
- restore 後の git diff が空
- 対象 focused pytest が PASS

次
==
Phase156 closure fixed4 を再実行し、
canonical `python -m pytest tests` を Phase-final gate とする。


Fixed1
======
初版 restore script は subprocess の text decoding を
Windows locale の既定値に任せていたため、git show の UTF-8 日本語を
cp932 として読み、UnicodeDecodeError になった。

Fixed1:
- `_run_git()` に
  `encoding="utf-8"`
  `errors="strict"`
  を明示。

Production changes:
- なし

対象 test file:
- 初版失敗時には write 前で停止したため未変更。
- Fixed1 で HEAD の canonical full file に置換する。


Fixed2
======
Fixed1 は canonical file の内容自体は取得できたが、
Python の `Path.write_text(..., newline="\n")` で LF 固定にしたため、
Windows working tree の CRLF と差が生じた。

git diff では全117行が内容同一の remove/add として表示された。

Fixed2:
- `git show` + Python write を廃止。
- Git 自身の

  git restore --source=HEAD --worktree -- tests/test_phase144_6_pi6_generic_production_route.py

  を使用。

これにより `.gitattributes` / `core.autocrlf` を含む
Git の working-tree 改行規則に従って復元する。

Production changes:
- なし

Test semantic changes:
- なし

対象 file は HEAD の canonical working-tree representation に戻すだけ。
