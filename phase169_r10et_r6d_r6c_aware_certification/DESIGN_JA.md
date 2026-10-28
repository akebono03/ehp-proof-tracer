# Phase 169 R10ET-R6D 設計と監査範囲

## 目的

R6C 完了後に R6 を再実行すると、`certify_reviewed_production()` が旧 R4 Renderer と
現在の R6C Renderer のバイト差分を検出し、Proof Tree の監査前に停止する。
R6D はこの前提条件だけを更新する。R6C の19ケース PASS は R6 再監査の代わりにはしない。

## 変更対象

- `phase169_r10et_r6_residual_definition_dependency_audit/audit.py`
  - `certify_reviewed_production()` の全文を置換する。
- 新規 `phase169_r10et_r6d_r6c_aware_certification/` の補助プログラム、テスト、説明文書。

変更しないものは、共通 Definition、ProofStep、探索、Model／Renderer の本体、
`summarize_dependency()`（監査の判定条件）、Git index、R5D の7件以内の既存変更である。

## 検証方法

Git R4 の元コードと Git blob SHA-1 を照合し、R6C patch.py 自体の SHA-256 を
固定値と照合してから、Model・Renderer に R6C の変換関数を適用する。
実ファイルが変換後の期待バイト列と一致することが必須。
R10A Projection は従来どおり R4 本体と完全一致が必要。
R5D の provider と関連テストは R4 ベースの R5D 変換結果と完全一致が必要。

これらの安全条件を満たした場合だけ、R6 の既存19ケース監査と限定 pytest を再実行する。
監査失敗時は R6 の監査ファイルだけ復元し、既存の実装・変更を保持する。

## 完了条件・境界

R6 の `REQUIRED_PASS`、`PROBES_PASS`、`AUDIT_ONLY_COMPLETE` に加えて、
R6D の `TRACKED_INDEX_PRESERVED`、`COMPLETE` がすべて PASS。

R6D では新たな数学的規則、任意 stem への一般化、将来 Phase の機能を追加しない。
全体 pytest は Phase 最終段階まで実行しない。
