# Phase 170 R2 — R1 コミット後の HEAD ガード修正

## 監査前提

R1 の実測記録は旧 HEAD `790db364a8531693572fc510f969da831f1f9ffb` で作成された。
GitHub の現行 `develop` は `f9e9a9d59970943d967e2cbcb0a98f13b2471407` に進んでいる。
コミット `170-1` の変更は Phase 170 R1 監査パッケージ6ファイルの追加のみ。
本番 Python コード、既存テスト、4種の対象 CSV のコミット間差分はない。

## 今回の修正範囲

新規監査パッケージのみを追加する。既存の R2 パッケージ、本体、既存テスト、Git index、既存監査結果は変更しない。
`EXPECTED_HEADS` に確認済み現行 SHA を追加し、`load_r1` が記録 HEAD と現在 HEAD の差を
無条件に拒否するのではなく、`reviewed_r1_head_transition` により次の条件をすべて検証する。

1. `develop` と、現行本体の blob が事前確認済みであること。
2. 旧 R1 HEAD と現行 HEAD が指定された完全 SHA の組であること。
3. Git の祖先判定が通ること。
4. コミット間差分が R1 監査パッケージ6件の追加に完全一致すること。
5. R1 `audit.json` の12群・AUDIT_ONLY・保全フラグが既存検査に合格すること。

想定外の HEAD、コード変更、CSV 変更、余分な追加ファイルは拒否する。
R1 の Proof Tree と証明探索を再生成しない。R2 の DB/Goal/Reference 診断条件は変更しない。
監査結果には HEAD 移行の受理理由を `r1_source_transition` として残す。

## 完了・次工程

限定 pytest と12件の R2 診断記録生成が正常終了し、既存 tracked/index が不変なら監査実行成功。
未完成群の数学的原因を確定するのは R3 であり、R2 では新規推論規則を実装しない。
全体 pytest は Phase 170 終了時まで実行しない。
