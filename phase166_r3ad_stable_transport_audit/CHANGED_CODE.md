# Phase 166 R3-AD 変更一覧

- 本体コード・既存テスト・文書5種は変更なし。
- 新規 `phase166_r3ad_stable_transport_audit/audit.py`：`audit_structural_transport()`、`audit_real_eta()`、`main()` の全文を同梱。
- 新規 `phase166_r3ad_stable_transport_audit/test_r3ad.py`：限定テスト関数全文と import を同梱。
- 新規 `run.ps1`：読み取り専用監査と限定 pytest を実行する。
- 合成前提による構造テストは「任意 stem の文献上の証明が完成」を意味しない。
- Phase 166 終了時まで全体 pytest を実行しない。
