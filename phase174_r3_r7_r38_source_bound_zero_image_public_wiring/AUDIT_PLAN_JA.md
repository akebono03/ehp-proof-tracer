# Phase 174 R3-R7-R38：一般零像推論の共通 Provider 接続

## 現行ソースの事前確認

GitHub `akebono03/ehp-proof-tracer`, `develop`, HEAD `660cadd928a2cbca00f71c5c35cd3af1230a54e9` を確認した。R37 の独立監査はユーザーの限定 pytest 66 PASS を確認済み。R6 の一般的な有限巡回群の生成元零像規則、R7 の零因子規則、R9 の結合律、Phase 169 の合成写像の懸垂規則、R14 の Toda (5.9) 出典付き一般消滅関係、R36 の context Registry、および関連テストを確認した。

## 数学的目的

$$E:\pi_{10}^{5}\rightarrow\pi_{11}^{6}$$

に関して、次の推論連鎖を共通 Provider の候補として公開する。

1. 未証明の有限巡回群表示 $\pi_{10}^{5}=\mathbb Z/2\{\nu_5\eta_8^2\}$ を **DB の型付き候補としてのみ**取得する。DB prior は独立した Toda 文献引用ではない。
2. R6 はその表示と $E(\nu_5\eta_8^2)=0$ を別々の subgoal として要求する。
3. R7 は検証済みの合成写像像と、Toda (5.9) から **INFERENCE** によって得る $\nu_6\eta_9=0$ を要求する。
4. R9 は結合律を型付きで再適用する。
5. Phase 169 の既存規則と安定代表元の定義は、各因子の懸垂像を証明義務として導く。

この追加 Provider は一般的な次元と型に基づく。`n=5,k=5` による専用証明・特別分岐は設けない。型付き DB prior は補題の proof leaf に変換しない。最終的な根 $\pi_{12}^{7}=0$ は追加しない。

## 変更対象

- 既存：`phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py` の `build_context_expansion_provider_registry()` 全体を置換。既存4個と R36 の条件付き Provider を保持し、R14 の出典付き一般消滅法則がある場合のみ R38 Provider を登録する。
- 新規：`phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py` の `valid_suspension`, `lifted_stable_composition`, `left_associated`, `expand_source_bound_zero_image_chain`。
- 新規：`install.py`, `audit.py`, `tests/test_static.py`, `tests/test_public.py`, `run.ps1`。

## 完了条件と境界

Source Guard PASS、R14 の引用の存在、R6/R7/R9/Phase169 の公開候補を実測、限定 pytest PASS。全体 pytest は Phase 174 closeout まで実行しない。

R38 では候補だけを確認し、E の零像の独立証明、上側 Δ の全射性、Web の root 完成を宣言しない。R39 では検証済み ProofStep の閉包と、R37 の上側 Δ 全射性規則を接続するかを別途検討する。
