# Phase 169 R10ES-R1 — 合成元の一部分に含まれる冪の共通表示

## 対象と既存コードの確認

2026年10月28日、GitHub `akebono03/ehp-proof-tracer` の `develop`、HEAD `f94d8bff28692e5a2b293e7cbbb654e89284e1ba` を確認した。

既存の `phase169_r10eb_typed_composition_power.display.typed_stable_composition_power_latex()` は、合成元全体が一つの登録系列の連続する元から構成されるときにのみ冪表示を返す。したがって、`Composition(ν_n, Composition(ν_{n+3}, κ̄_{n+6}))` のような混合合成は圧縮されず、`ν_n ν_{n+3} κ̄_{n+6}` と表示される。

R10ER の直和群用射影は `render_toda_public_group_generator_latex()` を利用しており、その内部は最終的に `render_toda_expression_latex()` を呼び出す。よって後者の既存1関数を変更する。

関連テストとして `phase169_r10eb_typed_composition_power/tests/test_r10eb_typed_composition_power.py` と `phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py` を確認した。

## 数学的規則と表示上の変更の区別

型付きの連続合成 $\nu_n\circ\nu_{n+3}$ について、既存の表示規則をその部分式にも適用し、

$$
\nu_n\circ\nu_{n+3}\circ\bar\kappa_{n+6}
\quad\longmapsto\quad
\nu_n^2\bar\kappa_{n+6}
$$

と表示する。部分式が同一系列かどうかは、既存の `typed_stable_composition_power_latex()` で照合する。元の木全体は型付き `HomotopyElement` の連続する可合成な因子でなければならない。元の `Composition`、Proof Tree、Goal、Reference、Citation は変更しない。

これは生成元名に基づく置換ではなく、型付きの合成部分式に対する既存の圧縮規則の適用範囲を広げるものである。一般化した数式の導出・安定元の等式の証明は既存の規則に委ねる。

## 変更対象と関数

既存ファイル `toda_human_readable_renderer.py` の **`render_toda_expression_latex()` 全体**だけを置換する。import、クラス、ほかの関数は変更しない。置換関数の全文は `full_functions/render_toda_expression_latex.py` にある。

新規ファイルは `phase169_r10es_r1_typed_partial_power_display/` 以下の `__init__.py`、`patch.py`、`audit.py`、`tests/test_r10es_display.py`、`run.ps1`、`README.md`、本資料である。テストで用いる import は各テストファイルに省略なしで記載した。

## 検証と完了条件

限定 pytest には新規テスト、既存 R10EB の型付き冪表示テスト、既存 R10ER の直和群圧縮テストを使用する。ライブ監査では $\pi_{56}^{30}$、$\pi_{44}^{30}$、$\pi_{46}^{30}$、$\pi_{39}^{30}$ を再探索し、完成状態と Trust Boundary を検証する。

$\pi_{56}^{30}$ に関して、`\nu_{28}^{2}\bar{\kappa}_{34}`、`\nu_{30}^{2}\bar{\kappa}_{36}`、対応する $E^2$ の式が正しく表示されることを確認する。既存9-stem の表示とすべての出典追跡は維持する。

新しい Definition、文献引用、数学的推論規則は追加しない。全体 pytest は Phase 169 の終了時にだけ実行する。

## 次の段階との境界

今回の対象は合成元の表記統一のみであり、Proof Tree のさらなる圧縮、個別 Definition の整理、群構造生成規則の変更を含まない。
