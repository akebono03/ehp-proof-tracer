Phase 146 Documentation Closure

更新対象:
- docs/design.md
- docs/development_log.md
- docs/roadmap.md
- docs/proof_records.md

README.md:
- 変更なし。Phase 146 の最終内容は内部 Narrative architecture / audit が中心で、
  user-facing API / CLI / Web usage の新変更はないため。

方針:
- design.md: Phase 146 の current architecture / root-cause boundary を追加。
- development_log.md: Phase 146-1〜146-9 を追記。
- roadmap.md: Phase 146 planned section を完了節へ置換し、Phase 147〜152 を RC1〜RC6 に対応。
- proof_records.md: historical/current comparison と provenance boundary を追記。
- Phase 146-7 の production change と Phase 146-8/9 audit-only を区別。
- order argument に primary exactness component が存在するという Phase 146-9 実測を反映。
- pi_6^3 public route gate はまだ削除しない。
- future Phase の機能は実装しない。

全文出力:
実行後、更新済み4文書の全文コピーを
phase146_documentation_closure/updated_full_documents/
へ出力する。

テスト:
この documentation package 自体は pytest を実行しない。
Phase-final repository-wide test は次を使用する:
python -m pytest tests -q
