# Phase 169 R10E4R4 設計・実行記録

## 対象

- 本番 `phase169_r10e4_ordered_db_prior/db_prior.py` の `_has_explicit_row()` だけを R10E4R2 の保護付きパッチで更新する。
- 既存テスト `phase169_r10e1_general_group_transport/tests/test_r10e1_general_transport.py` の3関数を更新する。
- 既存テスト `phase169_r10e2_unpositioned_citation/tests/test_r10e2_unpositioned_citation.py` の1関数を更新する。
- 新規限定テスト `tests/test_r10e4r4_explicit_rows.py` を追加する。

## 理由

CSV に `n` が空欄の区切り行があり、早期例外で後続の実在 DB 行が隠れていた。R10E4R2 はこの点を修正したが、最初の一致後に早期 return すると、後方に存在する不正な非空次元値を検出できない。全行を検査したうえで一致可否を返す。

R10E1/R10E2 の失敗4件は R10E4 の「文献登録がなくても、先行 DB を明示的に採用できる」仕様に対し、旧テストが「引用がなければ候補0件」を一律に期待していたために発生した。登録されていない文献は引き続き `GIVEN` と認めず、実在する先行 DB の存在と一致する候補のみ許可する。DB を返さないモックでは候補0件も確認する。

## 信頼境界

DB 前提は `admitted_db_step()` と `verified_db_step()` により、型、内容、先行順序、実在行を照合する。旧テストの期待値を更新しても、この検証条件は緩和しない。

## Phase 境界

(4.5) と生成元の写像を実際にすべて証明できたかは別問題。未完成群が残っても、本修正で完成と偽装しない。全体 pytest は Phase 169 の最後にのみ実行する。
