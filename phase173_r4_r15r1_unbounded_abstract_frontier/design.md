# Phase 173 R4-R15R1：任意の k に対する抽象群の先行前提判定

## 位置づけ

Toda Proposition 4.4 と、検証済みの $H(\nu_4)=\iota_7$ から

$$
\pi_{k+4}^{4}\cong\pi_{k+3}^{3}\oplus\pi_{k+4}^{7}
$$

という一般同型を得る。ここに $k=31$ を排除する数学的理由はない。ただし、抽象群の型と具体的な生成元表示の一致は異なる検査項目である。

従来の `checked_general_inputs()` は、`_map_components()` による狭い生成元記法の計算が成功しない場合、先行群の抽象構造が既に利用できるかどうかを独立に報告できなかった。そこで、推論候補の認証を弱めることなく、一般的な構造判定を分離する。

## 変更対象（既存コード）

- `phase173_r4_r10_general_toda56_core/core.py`
  - `homotopy_groups` import の更新。
  - 新規 `_abstract_group_signature()`：群型の自由成分・有限巡回成分の位数を、生成元名とは無関係に抽出する。`checked_general_inputs()` の直前に追加する。
  - 新規 `checked_abstract_inputs()`：任意の整数 $k\ge3$ について、ターゲットと2つの先行データベースの行、DB 先行順序、抽象群の成分を照合する。`checked_general_inputs()` の直前に追加する。
  - 既存 `checked_general_inputs()`：上記を呼ぶが、従来の `_map_components()` と `components_match_alias()` を必須とし、判定を緩めない。

## 数学的根拠と安全境界

$n=4$ と $H(\nu_4)=\iota_7$ の特殊化において、対応する群の抽象構造が2つの前提の直和と一致することは必要条件である。ただしデータベースの群構造は採用した先行結果であり、この判定だけでは新しい `ProofStep` は作れない。

$k=31$ についてはデータベース上、$\pi_{34}^3$ と $\pi_{35}^7$ の両方に4個の $\mathbb Z/2$ 成分があり、ターゲット $\pi_{35}^4$ に8個ある。型の一致を検出することと、`$E\delta_3=\delta_4$` のような具体的関係を文献に基づいて証明することは別である。今回の改修では後者を自動補完しない。

## 公開探索との関係

既存の `expand_general_toda56()` は引き続き `checked_general_inputs()` を使用する。Web では $\pi_{35}^4$ が `generic-partial-proof` のままでよい。構造が一致するからといって、8個の記名生成元をもつ結論を `generic-complete-proof` にしない。

未対応の個別生成元は、`frontier.py` によって `_suspend_verified_shape()` と `_nu4_composed_image()` の双方から構造的に診断される。この2つは名前付き生成元の証明を作らないため、監査では必ず `public_proof_complete_by_this_change=False` を記録する。

## テストと完了条件

新規のインストーラー安全テスト、$k=31$ の抽象前提検査、既存 $k=3$〜$7$ の互換性、$k=8$ の未証明生成元の拒否、改竄ターゲットの拒否、および既存一般 Core の限定 pytest を実行する。対象外の全体 pytest は Phase 173 終了時に実行する。

## 次工程との境界

次の R4-R15R2 は、$\pi_{34}^{3}$ から $\pi_{35}^{4}$ への個々の懸垂像の根拠を、既存の数学規則と原文の出典から認証する。今回、証明探索接続、Reference Renderer、Web Adapter、`sphere.csv`、`HyoujiGen.csv` は変更しない。検証できない生成元関係を勝手に生成しない。
