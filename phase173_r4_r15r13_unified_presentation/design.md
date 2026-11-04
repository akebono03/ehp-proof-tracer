# Phase 173 R4-R15R13 — 共通表示契約

## 目的

Proof Search → Verified Proof Tree → ProofNarrativeModel → Common Web Layout → Web の責務を整理する。完成と未完成は同じ表示レイアウトを使い、本文と証明状態だけを変える。群・次元別分岐は設けない。

## データと表示

- `ProofNarrativeModel` は証明済み ProofStep、Citation、未解決 Goal、status の事実のみを保持する。
- 既存 `render_model_backed_narrative_markdown` の Markdown 公開 API は変えない（既存試験の `\n証明\n` 契約を維持）。
- `canonicalize_proof_layout` が完成・未完成の Markdown の見出し表記差だけを同じ見出し構造に正規化する。
- Web の外側が「Proof」「Proof target / Conclusion」を所有するため、内側で重複する「証明」「証明対象」は除く。
- 「使用する結果」は見出しとして統一し、Reference/Proof の区切りは1本に統一する。
- 引用本文、証明文、open_goals、数学的結論、探索診断は変更しない。

## 実装境界

既存本番ソースの変更は `web_group_proof_common.py` の `_build_group_proof_rendered_lines` 1関数のみ。新規 module は装飾契約の正規化だけを担当し、証明を生成しない。

全体 pytest は Phase 173 の終了時のみ。追加の意味論的推論、生成元対応、未完成 Goal 数式表示、内部診断文の修正は本作業の対象外。
