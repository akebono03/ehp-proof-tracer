# Phase 169 R3S — 実装・監査記録

## 変更対象

- `phase168_r3_37c_reference_projection.py` — `project_reference_bodies()` の関数全体のみ。
- 新規 `phase169_r3s_composite_reference_projection/tests/test_r3s_composite_reference.py` — テスト関数4件。

## 出典を越えない制約

- 登録済み `AssertionEntry.scope` に `typed_composite_fields` がある場合だけ、列挙された dataclass フィールドを独立した Reference 文として表示。
- スキーマと実体のフィールド一覧が一致しない場合は閉じて失敗。
- Proposition 5.1 の高次 η 群構造は型付き一般関係式の認識が通った場合だけ、既存命題の n>=4 の範囲で表示。
- 新しい ProofStep、命題、GIVEN、文献引用は作成しない。
- π₅⁵=(5.1) は引用経路未接続なので次の Phase に残す。

## テストと完了条件

限定テスト: 新規4件＋既存Reference3件＋1-stem10件。R3S実行時の Web π₅³ が complete を維持し、Proposition 5.1 の Reference 本文に4成分が表示されること。

全体 pytest は Phase 169 終了まで実行しない。
