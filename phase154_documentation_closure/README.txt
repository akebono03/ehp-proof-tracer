Phase 154 Documentation Closure

変更対象
--------
1. README.md
2. docs/design.md
3. docs/development_log.md
4. docs/roadmap.md
5. docs/proof_records.md

production code
---------------
変更なし。

README
------
英語。

Phase 154 proof-prose refinement の:
- semantic prose
- Reference linkage
- punctuation
- 112-group closure
- current regression boundary

を追加する。

design.md
---------
日本語。

Phase 154 の:
- provenance boundary
- semantic duplication
- Reference-to-body linkage
- punctuation policy
- 112-group closure invariant

を追加する。

development_log.md
------------------
日本語・追記。

R2 / R4 / R5 / R6、
punctuation closure audit、
final closure audit の実測を追記する。

roadmap.md
----------
日本語。

旧 Phase 154 planned section を current status に更新する。

documentation closure 時点:
- implementation closure PASS
- 112-group closure PASS
- full regression NOT RUN

次:
- Phase 154 final full regression
- その後 Phase 155

Phase 155:
Reference statement relevance / minimal display
を開始時 audit で scope 確定する。

proof_records.md
----------------
日本語・追記。

Phase 154 の proof-prose presentation provenance を記録する。

全文出力
--------
実行時に5文書を全文で書き戻し、
以下へ全文コピーを出力する。

phase154_documentation_closure/
  updated_full_documents/
    README.md
    docs/design.md
    docs/development_log.md
    docs/roadmap.md
    docs/proof_records.md

テスト
------
この package では pytest を実行しない。

Phase 154 final full regression は次の Phase-final step。
