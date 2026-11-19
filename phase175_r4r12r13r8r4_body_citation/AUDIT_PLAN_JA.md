# Phase 175 R4R12R13R8R4 — 本文の引用表現

## 現状

R13R8R3 のユーザー実行で Reference R3・R7 の式が表示された。限定 pytest は4件 PASS。完成証明の状態は `generic-complete-proof`。ただし本文では R3 が「[R3]を用いて」、R7 の式には引用番号がない。

R13R8R2 の Proof Tree では R3 は GIVEN step 2 → INFERENCE step 3、R7 は GIVEN step 11 → INFERENCE step 12。R3 の INFERENCE に R3 が直接紐づき、R7 の INFERENCE は直接の GIVEＮ 前提 R7 を持つ。

## 修正範囲

変更ファイルは `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown` のみ。既存 import、その他のクラス・関数・数学規則、データベース・出典レジストリは変更しない。

- 共通の `direct_given_premise_citation_numbers` で、直接 GIVEN が包む命題と後続推論の結論が型・値ともに等しい場合だけ、実在する GIVEN の引用番号を引き継ぐ。
- 共通 BodyLine 経路で、推論が唯一の直接 GIVEN を前提とし、その GIVEN の引用番号が自分の引用番号と一致する場合にだけ、「を用いて」ではなく「より」とする。
- 一般論として、複数前提からの推論は「を用いて」を維持。出典番号の逆引きや新規出典登録はしない。

## 確認

限定 pytest：新規引用表示監査、既存 R13R8R3 Reference テスト。実環境では n=5,k=4 を再探索し、完成状態および R3・R7 本文の接頭語を検査。全体 pytest は Phase 175 の最後にのみ行う。

## 境界

R13R8R4 は引用表示のみ。H 零写像の独立した ProofStep を追加しない。次の Phase での数学推論拡張も行わない。
