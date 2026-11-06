# Phase 174 R3-R7-R7 監査計画

## 監査済みコード

GitHub `akebono03/ehp-proof-tracer` の `develop` HEAD `67c57fc9ae63ce783ffdf9b502d472900abad57f` を確認。前回の `cbe3b866b1e39f15fc1c6965004b705e31d61de5` からの差分は、R6 パッケージの追加ファイルだけ。`SOURCE_BLOBS` を個々に検査する。

## 数学的な推論

`GeneratorImage(E,g,a∘b)` と `Relation(a,Zero(),EQUALITY)` が、それぞれ独立した **INFERENCE** の証明を持つときのみ、`GeneratorImage(E,g,Zero())` を推論できる。合成の次元と懸垂写像の始域・終域は全て検査する。群や生成元に固有の規則分岐は置かない。

## 出典

Toda Proposition 5.9 の採用転写で、(5.9) の一般関係 `ν_n ∘ η_{n+3} = 0 (n >= 6)` と、生成元の懸垂像の合成表示を確認する。転写中にある結論そのものを GIVEN にしない。

## 変更対象と追加位置

既存プロダクションファイルの変更はなし。ルート直下の新規ディレクトリ `phase174_r3_r7_r7_composite_zero_audit/` に、`rule.py`（`expression_endpoints`, `composite_zero_generator_inputs`, `generator_zero_from_composite_rule`, `expand_generator_zero_from_composite`）、`audit.py`（Git・出典・前工程・候補数監査）、テスト、`run.ps1` を追加する。

## 検証

R7 の新規テストと R6/R5/R4/R3 の回帰、既存の限定数学テストを**別プロセス**で実行する。全体 pytest は実行しない。

## 完了条件

Source Guard、前工程 R6 の本実行記録、型付き候補の生成、子 Goal の探索候補数、公開 provider 非変更が確認できること。子 Goal が未完成なら目標も未完成を維持する。

## 次との境界

R7 は読み取り専用の監査と独立規則の検証まで。R8 以降で初めて、(5.9) の一般定義・生成元の像が出典付きに成立するか、プロダクションへの共通接続を検討する。専用 Narrative 追加は行わない。
