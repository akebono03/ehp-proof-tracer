# Phase 168 R3-40F — 共通 Renderer の残存互換経路監査

監査専用。実装・固定基準・命題台帳は変更していない。

## 静的監査

- `NarrativeOrderEntry.after_indices` は互換フィールドとして残る: **True**
- 現在の共通 Renderer による `after_indices` 参照: **0 件**
- 現在の Projection による `after_indices` 参照: **0 件**
- 共通 Projection の Proof Tree 依存関係整列: **True**
- 共通 Renderer の Citation Model 参照: **True**
- 旧テストの互換フィールド参照: **True**
- 標準 Web の既定: `{'max_depth': 2, 'mode': 'narrative', 'goal': None, 'citation_source': 'model'}`
- 標準 Web に互換 `legacy` 分岐が残る: **True**
- Web Adapter にモデル未指定時の旧 Narrative fallback が残る: **True**

## 対象4群の実行時監査

| 群 | Steps | Reference | Deferred | 依存逆転 | R3-40E からの変更 |
|---|---:|---:|---|---|---|
| pi3_2 | 18 | 4 | なし | 0 | 一致 |
| pi4_3 | 25 | 4 | なし | 0 | 一致 |
| pi5_4 | 10 | 3 | なし | 0 | 一致 |
| pi6_5 | 10 | 3 | なし | 0 | 一致 |

## 分類・次工程との境界

- `after_indices` は通常描画で未使用でも既存のテストが参照するため、この監査では削除しない。
- `legacy` とモデル未指定時の fallback は、標準 Narrative の既定経路とは別。利用者・テストの実際の使用状況は未確認であり、即時撤去しない。
- 次の変更では、個別の public entry を触る前に呼出元と互換テストを確認する。
- 今回は新しい数学規則・出典登録・Web 分岐変更を行わない。
- 全体 pytest は Phase 168 の最後にだけ実行する。
