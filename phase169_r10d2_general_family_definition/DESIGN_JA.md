# Phase 169 R10D2 — 系列に依存しない型付き定義の証明接続

## 目的

R10D の `FamilyDefinitionAdapter` に `TodaNuFamilyDefinitionStatement` を直接登録する実装は、系列ごとにクラス・推論を用意しなければならず、共通化として不十分だった。R10D2 は単一の `CitedStableFamilyDefinition`、単一の `StableFamilyMemberDefinition`、単一の `GeneratorImage` 推論規則へ変更する。

## 今回の変更対象

- `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` 全体、`shared_expansion_provider()` 全体。
- `phase168_r3_37c_reference_projection.py` の `project_reference_bodies()` 全体。
- 新規 `phase169_r10d2_general_family_definition/family_citation.py`：引用・型付き定義と推論を共有する関数群（全文を含む）。
- 新規 `tests/test_r10d2_general_family.py`：限定テスト（関数全文、import 全文を含む）。

既存 API は維持し、R7 の規則本体、Proof Tree、既存 renderer、DB ファイルを変更しない。既存の η の導出は互換性維持のためそのまま残す。

## 証拠の境界

`HyoujiGen.csv` の `kinds=0` は系列 ID・stem・最小次元・生成元の名前と型の情報。これだけを根拠に `GeneratorImage` を `GIVEN` にすることはできない。

採用した TeX 転記原稿の次の定義を、文献掲載順の両側にある登録済み位置によって確認する。

- ν：$\nu_n=E^{n-4}\nu_4\ (n\ge4)$。Lemma 5.5 と (5.5) の間、位置 8550。
- σ：$\sigma_n=E^{n-8}\sigma_8\ (n\ge8)$。Lemma 5.14 と (5.15) の間、位置 10450。

原本との照合を済ませたという意味ではない。採用された転記原稿を根拠とした位置である。μ を含む他の系列は、対応する出典がないため推論対象に追加しない。

## 共通の Proof Tree

$\alpha_n=E^{n-n_0}\alpha_{n_0}$ という引用済み系列定義から、`CitedStableFamilyDefinition` (`GIVEN`) を1件登録する。各 `StableFamilyMemberDefinition` はこの定義からの `INFERENCE` とする。2つの連続する実際に証明済みの定義から `GeneratorImage(E,\alpha_n,\alpha_{n+1})` を `INFERENCE` とする。R7 は、先行群構造の `GIVEN`、Toda (4.5) の `INFERENCE`、各 `GeneratorImage` の `INFERENCE` を要求する。未証明の目標を前提として昇格させない。

`Reference` には引用された一般形を、証明本文には必要な具体式を載せる。引用には `publication precedence` の既存の審査を用いる。

## テスト・Phase 境界

本 Phase の限定 pytest と監査のみ実行し、全体 pytest は Phase 169 の終了時に実行する。1-stem と2-stemの完成状態を維持する。3-stem が未完成なら原因を記録し、虚偽の complete を表示しない。系列ごとの新規クラス・推論規則、将来の追加系列に対する架空の原典の登録は行わない。

実行時に `output/` に変更後の関数全文・本番ファイル全文・バックアップ・監査ファイルを出力する。失敗時は両本番ファイルを復元する。
