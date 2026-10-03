Phase157-R5-R3 — Literature Statement Boundary catalog expansion

実装前確認:
- GitHub main: 5cdd848e0610408fe88f19db29caef8a50c6dbda
- GitHub main は Phase156 時点であり、Phase157 boundary module はまだ未 push。
- 現在のローカル Phase157-R5-R2 CSV を authoritative source として使用する。
- Toda Proposition 5.8 / 5.9、Lemma 5.7 等の proof records を確認済み。

変更対象:
1. toda_literature_statement_boundary.py
   - fixed statement component catalog を追加
   - R5-R2 の exact locator/rule pairs を fixed / proof-internal に登録
   - _proof_step_reference_locator() を拡張
2. tests/test_phase157_r5_r3_boundary_catalog_expansion.py
   - R5-R2 の exact candidate pairs を軽量 synthetic ProofStep で確認

import:
- 変更なし

class:
- 変更なし

変更関数:
- _proof_step_reference_locator()

新規関数:
- なし

主な fixed statement catalog:
- (4.5): stable-range suspension isomorphism
- (5.2): eta_2 composition isomorphism
- Equation 5.7
- Equation 5.8
- Lemma 5.4
- Lemma 5.7
- Proposition 2.5
- Proposition 3.1
- Proposition 4.4
- Proposition 5.8 finite-dimensional group components
- Proposition 5.9 finite-dimensional group components

既存 aggregate:
- Proposition 5.1
- Proposition 5.3
- Proposition 5.6
- Proposition 5.11
には finite_dimensional_aggregate component を追加する。

安全策:
- R5-R2 catalog_candidates.csv を apply 時に読む。
- 1件でも source-supported classification rule に当てはまらない場合、
  production file を変更する前に exit code 2 で停止する。
- exact local rule names をそのまま mapping に登録する。
- unknown rule を推測で fixed にしない。

今回しないこと:
- Reference selection の112群全面適用（R5-R4）
- 112群 replay の再実行
- full Narrative rendering
- repository-wide pytest

完了条件:
- UNDECIDED rule pairs = 0
- focused lightweight tests all pass
- R5-R2 candidate pairs がすべて fixed_statement / proof_internal のどちらかになる

次:
- Phase157-R5-R4 で generic Reference selection を112群へ接続
- Phase157-R5-R5 で112群再監査
