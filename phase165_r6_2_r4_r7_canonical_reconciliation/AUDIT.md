# 正規探索照合の範囲

- 本番コード変更なし。
- 前回の 3 Root Candidate について、全候補と各候補単独の正規探索を比較する。
- 正規の `reconstruct_registered_goal` と `typed_reference` を使用する。
- `FORWARD_PASS` と `CANONICAL_COMPLETE` を明確に区別する。
- `UNRESOLVED_OR_AMBIGUOUS` は例外本文の `found N` で識別する。
- 公開 Renderer の原因調査は、正規探索結果の確認後に実施する。
- 全体 pytest は Phase 165 の最後に実施する。
