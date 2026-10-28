# Phase 169 R10EC-R1 — 巡回群の負例テスト修正

## 原因

元の `test_r10ec_cyclic_non_direct_sum_is_not_compressed` は、`(n,k)=(4,1)` の探索が `ProofSearchStatus.COMPLETE` であることを前提としていた。しかし実際の R10EC 実行では `PARTIAL` となり、未完成探索に対する不適切な事前条件で失敗した。現行の推論の変更を正当化するものではない。

## 変更対象

既存ファイル `phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py` の import 部分全体（`FiniteCyclicGroup` の追加）と、テスト関数 `test_r10ec_cyclic_non_direct_sum_is_not_compressed` の全文のみ。

新規 `phase169_r10ecr1_cyclic_test_alignment/patch.py` の `transform_test` と `main` は元のテストファイル SHA-256 に厳密一致する場合だけ置換する。追加位置は `pytest` import の直後と、元の同名テスト関数位置。改変後の import 全文、関数全文、ファイル全文を `output/` に出力する。

## 数学・信頼境界

巡回群に対し直和群専用の Projection が `None` を返すという負例の意味は不変。対象を既存 R10A が `COMPLETE` として検証済みの `(n,k)=(8,2)`、すなわち $\pi_{10}^{8}$ に置換し、結論の右辺が `FiniteCyclicGroup` であることも明示的に確認する。

Proof Tree、推論規則、Reference、Trust Boundary、データベース、既存の本番ファイルは、この R1 パッチでは変更しない。元 R10EC の `run.ps1` が本番 Renderer 変更・限定 pytest・監査を担当する。

## 実行・完了条件・次段階

R1 のガード用 pytest 5件を実行し、続いて元の R10EC `run.ps1` をそのまま呼び出す。全て PASS の場合に完了。失敗時は元の R10EC が本番ファイルを復元し、R1 はテストを元のバイト列に戻す。全体 pytest は Phase 169 終了時のみ。次の機能には着手しない。
