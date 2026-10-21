# Phase 166 R3-AH 変更内容

変更対象：新規 `phase166_r3ah_provenance_audit/audit.py` の `contained_relations`, `assertion_matches`, `inspect_case`, `audit`, `main`、新規 `test_r3ah.py` の2テスト、および `run.ps1`。

既存コード・既存テスト・本体ドキュメントは変更しない。命題台帳にない出典や掲載順を作らない。目標の完全一致、CSV候補、登録命題、Toda (4.5)、基点、未解決 Goal と診断を記録する。2件の限定 pytest のみ実施する。全体 pytest は Phase 166 最後に実施する。
