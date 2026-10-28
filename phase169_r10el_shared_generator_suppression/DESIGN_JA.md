# Phase 169 R10EL — 巡回群と直和群の表示抑制判定の共通化

## 根拠と実装範囲

R10EK において、巡回群 $\pi_{28}^{22}$、$\pi_{32}^{22}$、直和群 $\pi_{23}^{15}$、$\pi_{33}^{24}$ はすべて `complete`、Trust Boundary PASS であり、共通の非表示安全条件を満たした。既存の R10EJ / R10EC の表示数式・推論・引用は変更せず、補助 ProofStep の非表示判定だけを R10EL で共有する。

変更対象は `phase169_r10a_verified_stable_chain_projection/projection.py` の `project_verified_stable_image_chain()`、`phase169_r10ec_direct_sum_narrative_projection/projection.py` の `project_verified_direct_sum_transport()`、および新規 `phase169_r10el_shared_generator_suppression/core.py` の `exclusive_generator_inference_indices()` である。既存 API、データクラス、共通 Renderer、数学的推論規則は変更しない。

## 共通判定の条件

非表示候補は、実際の根の生成元像 `GeneratorImage` とその前提の連鎖に含まれる `GeneratorImage` または `GeneratorSuspension` で、かつ推論ステップであり、独立した Citation を持たないものに限定する。ProofStep の照合は表示文字列ではなく**オブジェクト同一性**で行う。必要な祖先が Proof Narrative Model の表示順に含まれなければ失敗させる。

非表示にするステップの利用先が根、または同時に非表示にする他のステップに限られることを確認する。巡回群側では他で使用される祖先の文章を残せる。直和群側では既存 R10EC の厳格な一括非表示条件を維持し、未処理の非表示候補が残る場合は Projection 全体を拒否する。

共通判定は推論も引用の新規登録も行わず、検証済み Proof Tree の文章表示だけに作用する。検証済みであることは呼び出し側の Trust Boundary が担保する。表示変換を信頼境界の代替としない。

## 実行と完了条件

`run.ps1` から、Git ancestor と対象ファイル2件の SHA-256 を検査し、バイト保存後に最小変更を適用する。限定 pytest のキャッシュを禁止し、4群を再探索して Trust Boundary、Reference、Proof Tree の不変性、重複0件、および表示省略数 $31,40,10,110$ を検査する。失敗した場合は対象2件を元のバイト列に戻す。追加の 11-stem、14-stem の群構造・出典登録、自由部分の一般化は本段階では行わない。

全体 pytest は Phase 169 の最後にのみ実行する。
