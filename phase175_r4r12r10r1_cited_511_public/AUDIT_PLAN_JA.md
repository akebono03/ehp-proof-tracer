# Phase 175 R4R12R10R1 — (5.11) 出典付き採用

## 方針

Toda Chapter V の採用 TeX に記録された式 (5.11) は既知の文献結果として使用し、Proposition 2.5 と (5.8) に遡って再証明しない。対象群の結論 $\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}$ は GIVEN にしない。

式 (5.11) は $\Delta(\eta_9)=E\nu'\circ\eta_7$。文献参照 `toda:(5.11)` と、既存の `phase163_r4_r94_output/manifest.json` に対応する掲載順を検証し、`CitedToda511` を `FIXED_STATEMENT` としてリンクする。

## 変更対象

- 新規 `phase175_r4r12r10r1_cited_511_public/source.py`：`CitedToda511`、`canonical_511()`、`verify_cited_511()`、`build_cited_511_source()`。
- 新規 `provider.py`：`expand_cited_511()`、`build_cited_511_provider()`。
- 新規 `installer.py`：`git()`、`update_function()`、`plan()`、`install()`。
- 新規 `audit.py`：`verify_git()`、`inspect()`、`main()`。
- 新規 `tests/test_cited_511.py`：限定テスト6件。
- 既存 `phase165_r52_r9_shared_math.py`：`build_shared_typed_bridge()` 全体と `shared_expansion_provider()` 全体を、各1挿入で更新。モジュール先頭の import は不変更。
- 新規 `run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

## 完了条件・境界

- `build_shared_typed_bridge()` が (5.11) の出典付き GIVEN を正規経路で取り込む。
- `shared_expansion_provider()` が (5.11) の型付き等式を証明義務として展開し、既存 R9 の一般変換につながる。
- 型、出典、掲載順、登録重複を検証。新規数学規則0、最終群 GIVEN 0。
- 既存 `GeneratorImage` の完全証明、$E$ の像、対象群の完成は未主張。
- 全体 pytest は実施しない。Phase 175 終了時のみ実施。

## R4R12R10R1R1 — 限定テスト fixture 修正

対象ファイルは `tests/test_cited_511.py`、対象関数は `test_only_two_entire_functions_are_replaced()` のみ。既存 `installer.BRIDGE_ANCHOR` は本番関数で `if sources is None:` の内側にあり8スペース字下げされる。旧 fixture は関数直下に8スペースで配置し、その直後に4スペースの `return` を置いたため `IndentationError` が発生した。修正版では fixture を有効な `if True:` 内へ配置し、Provider と Bridge の双方を全文単位で更新できること、二重適用で変更しないことを確認する。新規 GIVEN・数学規則・本番コードの変更なし。全体 pytest は実施しない。


## R4R12R10R1R2 — reviewed R9 commit lineage fix（2026-11-18）

GitHub `develop` の現在の HEAD は `bf0d7be3081c61f2feec075a3c82c2004c29bbf2`。
旧 HEAD `3ec001a59044aeb056ec7190c43c6066eaf5abae` から1コミット進み、コミット差分は `phase165_r52_r9_shared_math.py` の共有 Provider 6行と R8/R9 監査ディレクトリの新規ファイルであることを GitHub compare で確認した。

- 既存 `audit.py`: `REVIEWED_R9_HEAD`, `REVIEWED_R9_COMMITTED_PATHS`, `validate_reviewed_lineage()` を追加。`verify_git()` の全文を更新し、旧 HEAD または検証済み R9 HEAD に限定する。R9 HEAD は Git の祖先関係・差分ファイル集合・1コミットを毎回確認。未確認 HEAD を拒否。
- 既存 `installer.py`: `REVIEWED_R9_COMMITTED_BLOB` を追加し、`plan()` 全文を更新。旧コミット blob `81d234c31e1af176457a35556045aed78d30b343` と、レビュー済み R9 コミット blob `83f278ec98512a763cdfba2552c70f972b169eac` のみ許可。
- 新規 `tests/test_lineage.py`: 3件の限定テスト。変更は `run.ps1` の限定 pytest 対象への追加だけ。
- 既存の文献登録 `source.py`、推論 `provider.py`、R9 数学規則は変更しない。GIVEN 追加なし、群完成結論の登録なし。
- 新規修正のテスト: 3 passed。元の6テストと実リポジトリ統合はユーザー環境で実行する。
- 次工程: R10R1R2 DryRun・本実行と出典付き (5.11) 候補を検証する。全体 pytest は Phase 終了時のみ。
