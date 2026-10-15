# Phase 165 Renderer R5 監査範囲

## 事前確認

GitHub の `akebono03/ehp-proof-tracer` にある公開 Web 入口、`PartialProofResult`、完成証明 Adapter、元の正規 Renderer と関連テストを確認した。GitHub のコードは R4 が適用されたユーザーのローカル環境と一致しない可能性があるため、**合否はローカルコードに対する監査とテストで判定する**。

## 監査項目

- R4 で撤去した Generic モジュールのファイルと旧 import が存在しないこと。
- 正規 Renderer の完成・未完成・共通 Dispatcher が各1定義であること。
- 共通 Model に ProofStep と未解決 Goal の情報があること。
- 公開部分証明と Web Narrative が共通 Dispatcher に到達すること。
- 完成した π₃² の代表例と任意の n=200, k=90 の未完成例が契約に従うこと。
- 補助 Renderer 候補を列挙し、独立した Narrative かどうかは未監査と区別すること。

## 境界

ソースコードの書き換え、補助モジュールの削除、型付き命題や推論規則の変更はしない。全体 pytest も実施しない。静的監査が通っても、すべての動的 import、特殊分岐、未テストの群の経路まで数学的に証明されたわけではない。
