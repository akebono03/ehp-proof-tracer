# Phase 173 R15R17-R3R4 設計記録

## 背景

R15R17-R3R2 の監査では, 既存の公開 Web テストと旧来の抽象群専用 Section を扱う補助 API テストが混在していることが判明した.

R15R17-R1 により, 検証済み抽象群の ProofStep が `ProofNarrativeModel.steps` に統合された. 通常の公開経路は Reference を一度だけ生成し, 共通 Renderer が抽象群の結論を通常の推論ステップとして出力する. 一方, 明示的な legacy 経路と補助 API は互換性のため独立の出力を維持する.

R15R17-R3R3 は, `open_goals` の各型付き命題を残し, 公開表示だけを集約する変更である.

## 変更範囲

今回変更するのは歴史的なテスト10ファイルに限定する. `test_projection.py` の補助 API テストは維持し, 公開 model 経路の Section 出現期待のみを更新する. `legacy` 経路を明示したテストでは, model と legacy を分けて検証する.

変更対象のテスト関数は `FULL_CHANGED_UNITS.md` に全文出力する. import の変更は行わない. 全関数を削除せず, `skip` や `xfail` へ変更しない. Phase 173 とは無関係なテストも触れない.

## 数学的・表示上の不変条件

- `status` と `conclusion` と `open_goals` は検索結果のまま保持する.
- Certified Abstract Structure の実際の `proof_step` が共通 Model に含まれる.
- 完成した記名生成元証明を抽象群だけの証明から捏造しない.
- 通常の公開経路で Reference は1か所にまとまる.
- 別の検証済み証明木の Reference と抽象群専用 Section は通常の公開経路に追加されない.
- 旧来の明示的な helper/legacy API の直接契約は保持する.
- n,k や群名を条件にした新しい Renderer 分岐を追加しない.

## 実行・保全

`run.ps1 -DryRun` で厳密な Git blob guard と変更後のテスト関数全文を確認する. 通常実行では対象テストだけをバックアップ付きで置き換え, 旧テストファイル10件と新回帰テスト, R3R3 と R1 の限定回帰を実行する. 失敗時はこの Phase で変更したテストファイルだけを元に戻す. Git index や本体ファイルは操作しない. 全体 pytest は Phase 終了時にのみ実行する.

## 次工程との境界

R3R4 は過去の表示テスト契約の修正のみ. 実装の新しい検索規則や生成元証明の追加は扱わない. 終了後に必要であれば実 Web 表示の再監査へ進む.
