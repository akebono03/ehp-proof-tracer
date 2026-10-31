# Phase 171 R20R2 実装・監査メモ

## 変更対象

- `phase165_r3_recursive_search.py`
  - `RegisteredGoalUnresolved` クラスの説明文（クラス全文あり）
  - `SourceBoundGoal` クラスの説明文（クラス全文あり）
  - `reconstruct_registered_goal()` 全体（全文あり）
- `phase165_r52_r9_shared_math.py`
  - **R20 の未コミット8行に限り**、適用時に認識できれば現在の `HEAD` の内容へ戻す。復元前の生バイトをバックアップする。
  - 復元不能な差分があれば無変更で停止。関数本体の独自変更は今回の成果物に含めない。
- 新規 `phase171_r20r2_first_successful_search/tests/test_first_successful_search.py`
  - `import` 全文、fixture、テスト関数全文を同梱。
- 新規配布用 `install.py`、`run.ps1`、本記録およびコード全文ファイル。

## 仕様

1. Source Bound Goal は元と出典を維持し、直接 GIVEN を利用しない。
2. 直接引用の適格性は従来の登録・公開順などの検査を通す。複数の別個の適格な直接引用がある場合は曖昧として拒否する。
3. 既存の `completed_internal_proofs` は従来の呼び出し順序で再利用する。
4. 推論候補の決定順は `expansion_provider()` が返す tuple の順序に従う。部分目標を再帰証明し、`find_inference_matches_for_rule()` と `derive_inference_proof_step()` を通過し、結論が型も含めて一致した時だけ採用する。
5. 成功した推論の `ProofStep` はその場で返す。後続の証明候補を調べない。
6. 推論照合不能・結論不一致・未証明部分目標・循環の際は次候補へ進む。
7. 未証明の場合は `RegisteredGoalUnresolved` と報告。部分証明の分類は既存 adapter に任せる。
8. 重複除外ヘルパーは既存呼び出しを残して観測 API との互換性を保つ。今回、一意性の判断には用いない。

## 完了条件と境界

- 推論の正しい独立2候補から最初の1個を採用する。
- 不正候補・未証明・循環で別の候補にフォールバックする。
- `SourceBoundGoal`、適格な直接 GIVEN、複数の直接引用の拒否が維持される。
- 限定 pytest がすべて通る。
- $\pi_6^5$、$|\pi_6^3|=4$、$\nu'$、群構造、Web `complete` の順の実群監査は**次工程**。今回のコード変更だけで数学的完成とはみなさない。

## 既知の確認限界

配布時点では、ユーザーの未コミット R20 変更の実バイトを確認できない。スクリプトは `HEAD` との差を検査し、安全性を確認できない場合は復元も探索器変更も実行しない。既存の大規模リポジトリの限定 pytest は、ユーザーのローカル環境で実行する。Phase 全体テストは行わない。
