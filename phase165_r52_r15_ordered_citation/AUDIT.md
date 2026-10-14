# Phase 165 R52-R15 監査

現行 GitHub で `phase164_r2_citation_eligibility.py`、`phase165_r2_registry_lookup.py`、`phase165_r3_recursive_search.py`、`phase165_r52_r9_shared_math.py`、関連テストを確認した。

既存 Phase 164 R2 の判定は、自己引用、出典、migration status、依存関係、独立確認済み ID、文献掲載順を検査する。一方で Phase 165 `typed_reference` はその判定を迂回する。今回新設する厳格モードだけをこの既存判定へ接続した。

現行登録の掲載順が未確定な場合、厳格モードで利用不可となる。採用済み TeX からの R38 証明と既存 Web 動作は変更しない。確認済み ID を自動生成しない。今後の課題は Web 共通探索への安全な接続と、文献内の順序確定、および部分証明/Narrative 表示の整合。

全体 pytest は Phase 最後に限る。
