# Phase 174 R3-R7-R8 監査計画

## 現在の実測

R3-R7-R7 の DryRun・本実行は PASS。限定 pytest は 147 件 PASS。Source Guard は PASS。R7 の公開候補は、合成の生成元像 0 件、左因子の零関係 1 件、生成元の零像 0 件。

## 文献

採用転写 `sources/toda/Toda_05_2.tex` の Proposition 5.9 の証明中には、一般関係式 (5.9) `\nu_n\circ\eta_{n+3}=0`（`n>=6`）と、生成元懸垂像の式 `E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0` がある。これは採用転写上の記載を示すもので、証明済みの `ProofStep` の存在を意味しない。

## 監査対象

- `phase174_r3_r7_r7_composite_zero_audit/audit.py` の R7 候補構築経路。
- `phase169_r10e5_composite_generator_image/rule.py` の汎用合成懸垂則。既存規則の候補数と子 Goal を確認。
- 左因子 `ν₆ ∘ η₉ = 0` の候補 1 件について、その推論規則・直近の子 Goal・source-bound か否かを確認。
- 合成表示の括弧付け、元の型・始域終域のずれを記録。

## 禁止事項

目標結論、零写像、零因子、生成元の像を直接 GIVEN にしない。個別群・個別生成元専用の公開 Narrative を追加しない。全体 pytest を実行しない。R8 は完全証明を宣言しない。

## 完了判定

限定 pytest・DryRun・本実行・Source Guard が PASS し、型付き候補と零因子候補の直近前提が JSON に保存されること。次 R9 では、この監査で見つかった実際の欠落に限定して汎用推論規則や source-bound specialization を検討する。
