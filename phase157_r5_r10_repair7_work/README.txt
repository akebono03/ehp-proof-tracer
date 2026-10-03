Phase157 R5-R10 repair7

原因:
- `使用する結果を先にまとめる.` は proof body ではなく
  `reference_section` 自体の先頭に含まれていた。
- 低レベル Reference renderer の既存 API 契約は維持したい。

修正:
- generic contribution renderer が public output に Reference section を
  組み込む直前だけ legacy intro を除去する。
- `render_toda_group_proof_narrative_reference_entries_markdown()` 自体は変更しない。
- public output で旧 intro を期待していた既存テストだけ、
  新しい `## 使用する結果` / `## 証明` 契約へ更新する。
- 低レベル Reference renderer の既存テストも focused pytest に含め、
  API 契約が維持されることを確認する。

全体 pytest は Phase157 closure の最後だけ実行する。
