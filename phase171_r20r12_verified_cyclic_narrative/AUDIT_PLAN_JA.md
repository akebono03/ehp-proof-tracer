# Phase 171 R20R12 — 実装・監査仕様

## 変更対象

- `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown` 全体（関数の内部だけを変更）
- 新規 `phase171_r20r12_verified_cyclic_narrative/projection.py` の `verified_order_four_summary` / `suppress_exact_duplicate_body_lines`
- 新規限定テストと監査、インストーラ

既存の探索器、InferenceRule、登録済み文献・データベース・数学的定義は変更しない。

## 証明上の条件

- 公開探索の root `ProofStep` が `INFERENCE` であること
- root の直下に `FiniteGroupCardinality` / `FiniteElementOrder` の検証済み推論があること
- 位数4の導出に実際の `EHPShortExactSequence` と両端の群が使われていること
- 非零な二倍元が実際の `Relation` と `NonZeroGroupElement` と `MapInjective` に遡れること
- 既存の型付き推論コンストラクタによって、対象の一致を検査できること

条件を満たさない証明では説明文を出力しない。Reference と Proof Tree は保持する。

## 完了条件

1. DryRun が通る。
2. 限定 pytest が通る。
3. 既存の公開探索が `complete` のままである。
4. `output/web_narrative.md` に位数4と元の位数4の説明が現れる。
5. Reference の登録済み番号を維持し、偽装 `GIVEN` を追加しない。

次段階で扱うもの: 他群への一般的な文章圧縮や、Phase 171 最終全体テスト。本 Phase では実施しない。
