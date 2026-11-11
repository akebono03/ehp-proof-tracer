<!-- PHASE174_R73_CLOSEOUT_PREPARATION_20261111 -->

## Phase 174 R73 — 共通証明経路と Closeout 前の設計境界（2026-11-11）

Phase 174 は **R73 時点では正式終了していない**。R71・R72 の限定 Gate は通過したが、Phase 末尾の現行アクティブ `tests/` 全体 pytest と最終 Git・文書整合確認は未実施である。R73 は全文文書を整備する工程であり、新しい数学的証明を追加する工程ではない。

### 現在有効な公開経路

```text
出典付きの型付き Goal
→ Source-first Backward Search（出典優先の逆向き探索）
→ Verified Proof Tree（検証済み証明木）
→ 単一 ProofNarrativeModel（証明文章モデル）
→ 共通 Narrative Renderer（文章表示器）
→ Web Group proof
```

探索は First Successful Proof Search（最初に成功した証明で終了）であり、唯一性検査を実施しない。`GIVEN`（文献・先行結果の採用）と `INFERENCE`（一般規則による導出）の責務を分ける。特定の群・生成元・次元専用の Narrative（文章分岐）や、結論を直接 GIVEN とする登録は導入しない。

### R70／R70R1 の表示限定性

`phase174_r3_r7_r70_verified_narrative_projection/projection.py` は、完成した証明木の根の祖先内にある型付き ProofStep と Citation の対応を要求し、合成像・結合法則・零像、Δ 全射性、EHP 完全性による説明を共通の表示へ投影する。R70R1 は associativity（結合法則）による一段の型付き証明連鎖をたどる条件を補正した。不一致・欠落・曖昧な場合には表示変換を実行しない fail-closed（検証不能なら変換しない）方式を維持する。

`E=0` と `H の単射性` の説明は、既に検証された四前提の零群一般推論規則の論理的帰結を文章にしたものであり、新たな独立 ProofStep として数えてはならない。`ProofSearchStatus`、`conclusion`、`open_goals`、`diagnostics`、証明木と引用数は Renderer が変更しない。

### 公開回帰の境界

R71 は完成8群の実探索と共通表示・引用数を監査し、限定 pytest 81 PASS。R72 はその保存レポートを確認し、未完成の $\pi_{12}^{4}$ と $\pi_{35}^{4}$ が `SEARCH_FAILED` のまま共通 Renderer／Web で表示されることを確認し、限定 pytest 38 PASS。R72 までの本番コード変更、新規 GIVEN、新規数学推論規則はいずれも 0 件。

これは登録されたすべての数学的文章の意味を個別に証明したという認定ではない。文献転記全件の正しさ、任意の $(n,k)$ の証明完成、ブラウザにおける全数式の画素単位の表示確認も未認定である。正式 Closeout は次の最終 Gate で判定する。
