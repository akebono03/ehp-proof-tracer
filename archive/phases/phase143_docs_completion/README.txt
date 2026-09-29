Phase 143 documentation completion package

変更対象
========
- README.md
- docs/design.md
- docs/development_log.md
- docs/roadmap.md
- docs/proof_records.md

コード変更
==========
なし。

テスト変更
==========
なし。

更新方針
========
README.md:
- English.
- Phase 143 semantic Narrative closure を追加。
- rule-name fallback を通常経路として残す古い説明を、Phase 143 完了状態へ訂正。
- latest regression を 9980 passed へ更新。

docs/design.md:
- 日本語。
- semantic statement rendering の現在設計を追加。
- direct premise suppression / relocation / preservation の境界を記録。

docs/development_log.md:
- 日本語。
- 追記方式で Phase 143 完了記録を追加。

docs/roadmap.md:
- 日本語。
- Phase 143 完了後の現在地と Phase 144 開始方針を追加。

docs/proof_records.md:
- 日本語。
- 追記方式で Phase 143 semantic Narrative provenance record を追加。

全文出力
========
実行後、更新済み5文書の全文を次へコピーする。

phase143_docs_completion/updated_full_documents/

実行テスト
==========
なし。

理由:
Phase 143 の最終全体回帰は既に

9980 passed in 807.31s (0:13:27)

で完了しており、今回の変更は Markdown 文書のみ。

完了条件
========
- 5文書が現行 Phase 143 完了状態を記録する。
- README は英語。
- その他4文書は日本語。
- development_log / proof_records は既存記録を削除せず追記。
- Phase 143 completion audit の fallback=0 / render errors=0 を記録。
- Phase 144 の機能を実装しない。

次 Phase との境界
=================
Phase 144 は別 Phase。
まず semantic Narrative を証明全体として横断監査し、
一般的な presentation pressure が確認できた場合だけ最小実装する。
