# Phase 174 R70R1：結合法則を挟む合成像の表示修正

## 現行コード・関連テストの事前確認

GitHub `akebono03/ehp-proof-tracer` の `develop` を、ユーザー実行の HEAD `fa98a4301026820714cd51da80ffacfd99e47b20` と比較し、同一であることを確認した。R70 自体は作業ツリー上の未追跡ディレクトリのため、配布した R70.zip の内容を確認した。

確認した主な規則は、R7（零因子）、R9（結合法則）、Phase 169 R10E5（合成像の2前提）、R38/R41（公開接続）、R40（独立監査）である。関連テスト R7/R9/R70/Phase171 も確認した。

## 原因

R70 の `_project_composite_images()` は、零像の前提である左結合の合成像が直接2つの構成要素画像を前提とすると仮定していた。公開の Verified Proof Tree では R9 の結合法則で左結合へ移した1前提のステップが存在し、その直前の右結合の像が2前提を持つ。R70 の `component_image_obligations()` は左結合の画像には適用されず、表示が統合されなかった。

## 変更の範囲

- 既存 `phase174_r3_r7_r70_verified_narrative_projection/projection.py` の `_project_composite_images` 関数だけを置換する。
- R9 の正規化された1前提の推論と R10E5 の2構成要素の推論を、ともに型とルール名および root 祖先で検査する。
- 前提が一致しない場合や文章中に他の証明が割り込む場合、文章を統合しない。
- 既存 Renderer、Reference、ProofStep、推論規則、GIVEN、公開 Search provider は変更しない。
- 全体 pytest は実施しない。

## 完了条件

1. R70R1 DryRun Source Guard PASS。
2. R70R1 限定 pytest PASS。
3. R70 の公開実証監査が `PASS_R70_PUBLIC_GENERAL_EXPLANATIONS`。
4. `PASS_R70R1_FOCUSED_AND_PUBLIC_ASSOCIATIVITY`。

## 次作業との境界

R70R1 では既存の証明ステップから表示可能な文章のみを修復する。追加の数学的な推論規則やほかの群の Narratives への拡張は行わない。
