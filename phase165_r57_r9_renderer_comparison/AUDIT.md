# Phase 165 R57-R9：監査内容

- `web_group_proof.build_standard_web_group_proof_view(4,1)` から実際の探索結果を観測する。
- 完成証明の public Renderer をそのまま実行する。
- 同じ `PartialProofResult` に対して、専用安定輸送表示の優先分岐を実行時のみ停止させ、共通処理による Narrative を生成する。
- 表示差と `ProofStep` の推論規則・前提数・未解決 Goal 数を JSON に保存する。
- 推論根拠が旧分岐に依存するかを調べる。欠落があっても今回の監査では補完しない。
- 本番ファイルの変更なし。全体 pytest は実行しない。

この監査では Toda (4.5) の ProofStep が生成済みであるとは推定しない。Reference や式の見かけの一致のみで旧分岐の削除を許可しない。
