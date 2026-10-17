# R4-R11 監査仕様

- 対象：$\pi_4^3$ の共通 Goal、FULL と SCREENED の Reference Context。
- 観測：R26、Witness R2、Seeded R4、文献スカラー特殊化、$\eta$ 特殊化、および Shared Provider（`proof_target` の有無）。
- 規則：候補は `ProofStep` ではなく、成功した証明ともみなさない。
- 制限：Provider の各出力の出典 ID が保持されていない場合は推測しない。監査から正規探索の採用結果を断定しない。
- 変更：本番ファイル変更なし。全体 pytest は Phase 165 終了時のみ。
