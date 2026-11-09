# Phase 174 R3-R7-R31 — Δ 全射性の一般推論監査

## 変更対象（最初に明示）

既存ファイル・クラス・関数・import・テストは変更しない。追加位置はリポジトリ直下の新規ディレクトリ `phase174_r3_r7_r31_delta_surjectivity_general_audit/` のみ。

- 新規 `audit.py`：`git`、`git_blob_sha`、`matches_pinned_blob`、`verify_checkout`、`inspect_toda_source`、`inspect_typed_obligations`、`report`、`main` を新規追加。
- 新規 `tests/test_audit.py`：7個のテスト関数を追加。完全な import と関数本体は同ファイルに記載。
- 新規 `run.ps1`：Source Guard、DryRun、通常監査、限定 pytest（各グループ独立）を実施。
- 新規 `README.md`（英語）、本ファイル（日本語）、`__init__.py`。既存の5文書には変更を加えない。

## 数学的正当性

一般の可換群準同型 `f:A→B`、`h:B→C`、`d:C→D` と `a∈A`、`w∈C` に対し、以下を**それぞれ独立に証明**できれば `f` は全射。

1. `h` が単射。
2. `im(h)=ker(d)`（中間で完全）。
3. `ker(d)=〈w〉`。
4. `h(f(a))=±w`。

証明：任意の `b∈B` の像 `h(b)` は `im(h)=ker(d)=〈w〉` に属する。よって `h(b)=k w=±k h(f(a))` と書ける。`h` は単射なので `b=±k f(a)`。したがって `B=〈f(a)〉`、特に `f` は全射。符号が確定していなくても結論は不変。

Toda の場合は `f=Δ:π13^13→π11^6`、`h=H:π11^6→π11^11`、`d=Δ:π11^11→π9^5`、`a=ι13`、`w=2ι11`。

## まだ独立した証明が必要な前提

- `Eπ10^5=0`：Proposition 5.9 の途中の式は結論を利用した GIVEN ではない。`π10^5=Z/2{ν5η8²}` と (5.9) の消滅から証明すること。
- `h` の単射：`Eπ10^5=0` と Proposition 4.2 の `E-H` 完全性から導出すること。既存 R5 一般規則を再利用可能。
- `im(h)=ker(d)`：Proposition 4.2 の `H-Δ` 完全性から導出すること。
- `ker(d)=〈2ι11〉`：`π11^11=Z{ι11}`、`π9^5=Z/2{ν5η8}`、式 (5.10) `Δ(ι11)=ν5η8` の三つから導出すること。Proposition 5.9 の**証明途中に印刷された結果を直接 GIVEN にしてはいけない**。
- `h(f(a))=±2ι11`：R30 の引用付き型付き Proposition 2.7 推論。既存 R30 はこの前提のみを接続した。
- 上記すべての Verified ProofStep をつなぐ一般規則は R31 では設置しない。特に R30 の `Prop27TypedHopfDeltaStatement` は `GeneratorImage` そのものではなく、型付き輸送の橋渡しが必要。

## Source Guard と引き継ぎ

2026-11-09 に GitHub `develop` の現行 HEAD `25118e281445ca17b30c60c8fd02d00acaa25ea5` を確認。引き継ぎの `42025c9fb7198f766d3e09531e35bfe04142ceb7` から2コミット進み、R30の10行が反映された。R31 は両方の**検査済み**ローカル状態を認め、GitHub 現行 HEAD が変われば fail-closed とする。R30 の未コミット変更・未追跡ディレクトリを消さない。

## 検証範囲・完了条件・次工程との境界

DryRun の Source Guard、Toda 原文の根拠順序、型付き upper/lower Δ と H の接続、限定 pytest が PASS することが完了条件。Web HTTP、Δ全射性、root complete は一切主張しない。全体 pytest は Phase 174 最終段階のみ。次工程では下側 Δ の核・E像零をそれぞれ source-first に実証し、必要なら一般生成元輸送規則を独立に設計する。
