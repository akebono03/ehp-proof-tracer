# Phase 169 R4C3 — 監査出力の復旧

## 現状と原因候補

R4C2 は限定 pytest 24 件 PASS、懸垂同型の証明成功、π₆⁴ の complete（18 ProofStep、未解決 0 件）に到達した。その後、追跡対象の Git status 比較で停止した。GitHub develop では R4C の `output/audit.md` と `output/audit.json` も追跡されており、監査処理はこれらを上書きする。実際にどのパスが変化したかはログに出力されていないため断定しない。

## 対象

- 本番ソース・既存テスト: **変更なし**
- 新規パッケージ: `phase169_r4c3_clean_audit`
- `runner.py`: 監査ファイルの byte-level スナップショット、限定 pytest、既存 R4C 監査、出力コピー、元のバイト列の復旧、前後 Git status 比較
- `verify.py`: R4C2 から無変更で再利用したコミット済み5ファイルの検証
- `run.ps1`: モジュール形式で runner を起動
- `tests/test_r4c3_guard.py`: 新規5件の検証

## 限定テスト

新規5件、R4C2 5件、R4C 6件、R4B 6件、R3O 7件：合計29件。

`python -m pytest -q` を新規と関連テストのファイル指定で実行し、全体 pytest は Phase 169 終了時まで実行しない。

## 完了条件

- 元の tracked audit.md / audit.json をバイト単位で復元
- その他の tracked Git status に変化がない
- R4C source audit: 懸垂同型の導出、3 種の出典祖先、π₆⁴ complete、未解決0
- 本番ソース変更なし

## 次 Phase との境界

R4C3 は監査実行の不具合修正に限定する。Renderer や新しい群の探索は変更しない。π₇⁵の検討は後続作業で扱う。
