# Phase 174 R56 一般規則の分離と公開接続

## 数学的目標

Toda Proposition 2.7 と EHP 完全性から、次の二段階を独立に証明する。

1. $H:A\to B$ が単射で、$\operatorname{Im}H=\mathbb Z\{2\iota\}$、$H(\Delta(\iota'))=\pm2\iota$ が証明されれば、$A=\mathbb Z\{\Delta(\iota')\}$。
2. $A=\mathbb Z\{\Delta(\iota')\}$ と、引用済み命題に基づき型付き $\Delta(\iota')$ が確認できれば、$\Delta$ は全射。

この実装で扱うのは R37 がすでに検証している一般の偶数 EHP 添字 $(n\ge4)$ の場合である。整数 $n=6$ 専用の規則を作らない。全写像についての新しい抽象群論 API に拡張することはこの R56 の範囲外。

## 変更対象

- `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()`：両規則を共通 provider に接続する。既存 R37 は互換性のため残す。
- 同ファイルの `search_shared_group_goal()`：R53 の引用済み核推論候補を通常の群構造探索でも利用する。
- 新規 `phase174_r3_r7_r56_cyclic_generator_bridge/rule.py`：型付き生成元の表現・2規則・2候補供給関数。
- 新規 `tests/test_rule.py`：数学的前提を欠いた誤用、偶数添字以外、型の異なる生成元、未証明 GIVEN を拒否。
- 新規 `tests/test_public.py`：実際の公開検索と信頼境界、先行 DB 結果の採用、再証明の不存在を検査。
- 新規 `tests/test_installer.py`：Git blob と正確な置換範囲の確認。

既存の import 節に変更はない。追加 import は変更関数の内部に置く。変更済み関数全文は本実行後、`output/CHANGED_FUNCTIONS_FULL_JA.md` に書き出す。

## Source-first の境界

- `data/HyoujiGen.csv` の表示名 `Δ(ι13)` はそれだけでは証拠にならない。
- 生成元の候補表現は `Prop27TypedHopfDeltaStatement` の型付き写像・次数から構成し、目標の構造と厳密一致させる。
- 規則1の4前提はいずれも `INFERENCE` として証明させる。
- 規則2の群構造は `INFERENCE` か、既存探索で正当な先行 DB `GIVEN` として採用されたものに限る。命題の特殊化は `INFERENCE` が必須。
- 新しい証明結果の GIVEN 登録、検索結果キャッシュ、群専用 Narrative は追加しない。
- 最初に成功した証明で終了。唯一性検査は追加しない。

## 完了条件

- $(n,k)=(6,5)$ が独立に `generic-complete-proof` となり、検証済みの4前提を持つ生成元の証明木を表示する。
- $(n,k)=(7,5)$ が引き続き `generic-complete-proof` となり、前の群構造の証明を再実行せず、順序を確認した先行 DB 結果を使う。
- R37 の既存 API を維持し、R35 と R37 の限定数学テストが PASS。
- Source Guard、限定 pytest、公開証明木の検証が PASS。
- 全体 pytest は Phase 最終 Gate まで実施しない。

## 過去監査との境界

R53〜R55 の一部監査は旧探索経路の「28ステップ」「引用6〜7件」を固定している。R56 の新規経路は数学的に同じ結論でもステップ数が変化し得る。過去監査の記録を改竄せず、新規公開監査は実証された結論・出典・再利用条件を確認する。全体回帰を Phase 終了時に監査し、必要な履歴監査のテスト契約修正を行う。
