# Phase 169 R10A — 実装・監査記録

## 目的

Phase 169 R9 監査の結果を受け、既存の R7 が証明した $r$ 回の `GeneratorImage` を Proof Tree 上で保持したまま、Narrative では $E^r(\alpha)=\beta$ の一式へ圧縮する。

## 変更ファイルと対象

- **新規** `phase169_r10a_verified_stable_chain_projection/projection.py`：ファイル先頭に `VerifiedStableImageChainDisplay`、その下に `project_verified_stable_image_chain` を追加。import は全文を収録。
- **既存** `phase168_r3_5_model_renderer.py`：`render_model_backed_narrative_markdown` 関数内、本文描画ループの直前に Projection を追加。import は関数内追加のみ。この関数全文を `output/render_model_backed_narrative_markdown_FULL.py` に自動保存。
- **新規** `tests/test_r10a_verified_stable_chain.py`：必要な import とテスト関数全文を収録。
- **新規** `run.ps1`、`patch.py`、`audit.py`：導入・検証・巻き戻し用。

## 圧縮の条件

- 検証済み完了証明のみ。未完成の Narrative に変更なし。
- 目標群が有限巡回群であり、Root の前提が先行群 Relation、Toda (4.5) の $E^r$ 同型、$r\geq3$ 個の連続した `GeneratorImage` である。
- すべての像は `INFERENCE` であり、始点・終点・すべての懸垂写像の群型・指数・次数・位数が一致する。
- 画像 ProofStep の別の消費者がいない。子の `GeneratorSuspension` は、その消費者が全て隠す像に属し、独立の出典を持たないときだけ非表示。
- 出典番号は画像の ProofStep の `GIVEN` 祖先から抽出する。証明された像に引用根拠がない場合は圧縮しない。
- ProofStep 自体と Reference は削除せず、表示される文章だけを短縮する。

## 期待される証明文章

従来の `E(η₄²)=η₅²`、`E(η₅²)=η₆²` などの逐次表示を、`[R3]より, $E^4(\eta_4^2)=\eta_8^2$.` にまとめる。

## 限定テスト

```powershell
python -m pytest -q phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py phase169_r7_general_stable_transport/tests/test_r7_general_stable_transport.py phase169_r6a_pi86_two_step_transport/tests/test_r6a_two_step_transport.py phase169_r5b_pi75_prior_transport/tests/test_r5b_pi75_transport.py
```

## 完了条件と次の境界

限定テストが PASS、$\pi_{10}^8$ が `complete` のまま、同一 Proof Tree と3つの Reference を維持し、$E^4(\eta_4^2)=\eta_8^2$ が一式のみ表示されること。

次の Phase では `HyoujiGen.csv` の `kinds=0` と文献の型付き系列定義を結合して $\eta,\nu,\sigma$ などへ一般化する。R10A では出典を持たない生成元同定を増やさない。3-stem の基点 $\pi_8^5$ の未完成もこの Phase で無条件に解消しない。
