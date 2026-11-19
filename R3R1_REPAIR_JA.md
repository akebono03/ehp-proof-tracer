# Phase 176 R3R1 — 出典アンカー引用符修正

対象: `phase176_r3_n3_rule_sufficiency_audit/audit.py` の `SOURCE_ANCHORS` 2エントリ、`tests/test_audit.py` の追加回帰テスト2件。既存 Proof Search、数学的規則、Provider、資料本体、主要5文書は変更しない。

原因: 原文の `\nu'` を、単一引用符で囲んだ raw string の中で `\nu\'` と誤記した。これは引用符をデータとしてエスケープしてしまうため、原文アンカーと一致しない。

修正: raw string の外側を二重引用符に変更し、原文の `\nu'` と厳密に一致するようにした。出典の許容条件は緩めない。

注意: R3 DryRun 失敗前の監査レポートは修正完了の証拠ではない。本 ZIP を上書き展開して DryRun と限定 pytest、本監査を再実行し、結果を確認する。全体 pytest は Phase 終了時のみ。
