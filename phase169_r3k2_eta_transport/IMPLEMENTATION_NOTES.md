# Phase 169 R3K2 — 実装内容と境界

## 変更対象

1. `phase168_r3_27_typed_statement_projection.py`：`element_tex()` を関数全体で置換する。新規クラスは追加しない。モジュール先頭の import は変更しない。関数内で `Composition` を import する。
2. `phase168_r3_5_model_renderer.py`：`render_model_backed_narrative_markdown()` を関数全体で置換する。モジュール先頭の import は変更しない。関数内で `GeneratorImage` を import する。
3. `phase169_r3k2_eta_transport/`：インストーラー、監査、限定テスト（新規ファイル）。既存テストを変更しない。

## 実装根拠

GitHub develop の `phase165_r12_r21_eta_generator_chain.py` を確認済み。`composition_eta_suspension_image_rule()` は、2つの INFERENCE `GeneratorSuspension` を前提とする型付き `GeneratorImage` を生成する。R3J1 実績では該当 Step 24 が2前提の INFERENCE である。`element_tex()` は従来 `Composition` を処理していなかったため、正規生成元 `η_n²` が本文に表示されなかった。

`element_tex()` は、左右がそれぞれ `η_n` と `η_{n+1}` である型付き `Composition` のみ `η_n²` と表示する。それ以外の合成は従来どおり非対応とする。Renderer は当該 `GeneratorImage` に実際の `TodaEtaFamilyGeneralDefinition` の引用祖先があるときだけ `[R...]` を表示する。

生成元の単独懸垂の本文行は、表示可能な合成 `GeneratorImage` に直接使われ、別の消費者がなく、独自の引用を持たない場合だけ省略する。ProofStep そのものは省略・改変しない。

`Chapter V, i)` の実際の locator と R 番号を変えず、表示見出しだけ `η 系列の定義（Chapter V, i）` とする。出典を隠したり、出典を増減させたりしない。

## 検査

- R3K が実装済みであり、実行結果の JSON に `status=complete` があることを事前確認する。
- `pytest -q`：新規5件＋R3J1監査4件を実行する。
- 1-stem の既存回帰テストを別プロセスで実行する。
- 実際の公開 Web 経路を取得して、合成像の推論根拠・式の重複・Reference の保持を監査する。
- 全体 pytest は Phase 169 の最後にだけ行う。

## 完了条件

- $E(\eta_2^2)=\eta_3^2$ が実際の `GeneratorImage` に対応し本文に1回現れる。
- 使われた2つの単独懸垂の表示が、引用を失うことなく合成像の1行へ統合される。
- R6 の実際の出典 locator と引用対応を保持する。
- 既存1-stem表示の回帰テストが成功する。

## 次工程との境界

R3K2 は説明文・引用の投影処理に限る。EHP の証明探索、先行文献順、命題台帳、$\pi_6^4$ 以降の探索には手を加えない。本文全体の圧縮や引用番号の再採番は、完成出力を確認してから別工程で判断する。
