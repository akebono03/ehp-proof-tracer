Phase156 closure

目的
====
Phase156-R6 完了後の Phase-final closure。

実行順:
1. README.md / design.md / development_log.md / roadmap.md / proof_records.md を全文再生成
2. 5文書の closure marker を検証
3. repository-wide pytest を実行
4. Phase155 で audit-only に分離された2 nodeid を exact 実行

Production code changes
=======================
なし。

文書方針
========
- README.md: 英語
- docs/design.md: 日本語
- docs/development_log.md: 日本語、追記
- docs/roadmap.md: 日本語
- docs/proof_records.md: 日本語、追記

build_phase156_closure_documents.py は current repository の各文書を読み、
Phase156 closure section を追加した全文を

phase156_closure_output/documents/

以下へ出力してから repository の各文書を全文置換する。

同一 marker が既に存在する場合は二重追記しない。

Phase156 closure 内容
=====================
- R1 duplicate inventory
- R2 consumer usage audit
- R3 minimal statement selection
- R4 proof-body duplicate suppression
- R5 112-group final audit
- R6 4-shard regression
- Reference minimal-display final contract
- Phase157 boundary

Phase-final test
================
通常 repository-wide pytest はこの closure で1回だけ実行する。

その後 audit-only exact node:
- Phase153 public Reference population invariant
- Phase97 cross-layer provenance invariant

も確認する。

Failure behavior
================
文書更新後に validation / pytest / audit-only test のいずれかが失敗した場合、
runner は5文書を自動的に元へ復元する。

Phase157 の production 機能は含めない。


Fixed1
======
初版 closure runner は PowerShell の `throw (...)` 内で
文字列連結を複数行に書いたため parser error で停止した。

そのため document build / validation / pytest は未実行であり、
repository content は変更されていない。

Fixed1:
- run_phase156_closure.ps1 の multiline throw を
  単一の interpolated string に変更。
- expected HEAD を Phase156-R6 commit
  `baab9402c9ca8c5051268d5d334591ea44b5b273`
  に更新。

その他の closure 内容は変更しない。


Fixed2
======
Fixed1 は5文書の生成自体には成功したが、
proof_records.md の validation marker が実際の文書表現と不一致だった。

validator expected:
- `112 unique groups`

actual closure text:
- `unique groups: 112`

Fixed2:
- validate_phase156_closure_documents.py の proof_records marker を
  `unique groups: 112` に修正。

Production changes:
- なし

Document content:
- 変更なし

pytest / audit-only execution:
- 変更なし
