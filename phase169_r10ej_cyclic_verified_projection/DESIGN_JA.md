# Phase 169 R10EJ — 検証済み巡回群の文章圧縮

## 現行監査

R10EI で、$\pi_{28}^{22}$ は54 ProofStep、Trust PASS、R10A が14ステップを非表示とする一方、1回懸垂の数式が17本残ることを確認した。$\pi_{32}^{22}$ は68 ProofStep、Trust PASS、R10A は利用不可で、1回懸垂の式が20回（相異なる式10本）表示された。

## 実装変更対象

既存の `phase169_r10a_verified_stable_chain_projection/projection.py` にある `project_verified_stable_image_chain()` だけを変更する。変更後の関数全文は `project_verified_stable_image_chain_FULL.py` に収録。トップレベル import・他の関数・クラスは変更しない。`apply.py` は元ファイルの SHA-256、Git blob、AST、および2つの置換アンカーを確認する。

## 表示の条件

- Proof Tree が完成し、R10A の Toda (4.5) とすべての直接 `GeneratorImage` を型付きで検査できること。
- 合成生成元の表記は既存の `render_toda_public_group_generator_latex` から取得する。表記は証明の根拠としない。
- 非表示にできる追加ステップは、圧縮した生成元像の **祖先** であり、`GeneratorImage` または `GeneratorSuspension` の INFERENCE で、個別 Citation がなく、利用先が非表示ステップまたは圧縮対象の Root のみに限られるもの。
- この条件を不満足とするステップは表示のまま残す。ProofStep・引用・依存辺は削除しない。

## 監査・テスト

`run.ps1` は限定 pytest と、$\pi_{28}^{22}$、$\pi_{32}^{22}$ の残存 $E$ 数式、Trust Boundary、本文、引用を再検証する。$\pi_{10}^{8}$、$\pi_{23}^{15}$、$\pi_5^4$ は非干渉の対照群とする。不合格なら既存コードをバイト単位で復元する。全体 pytest は Phase 169 終了時だけ実施する。

## 次 Phase との境界

11-stem の $\zeta$ 系列や14-stem の $\kappa$ を含む未完成証明について、DB 名から懸垂関係を捏造しない。文献上の証拠収集と型付き推論規則の検討は別工程とする。
