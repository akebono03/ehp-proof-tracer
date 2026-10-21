# Phase 166 R3-AT — 生成元の一次結合の復元

## 変更対象

- `phase166_r3aj_structured_generator.py`
  - `database_structured_group_goal_candidates()` 関数全体を置換します。
- 限定テストを新規追加します。

## 理由

`sphere.csv` の `Element` は各表示元を構成するID列です。`gen_coe` はその表示元たちの一次結合係数です。従来は、巡回群の各成分の `Element` を生成元と誤認していました。

たとえば `n=10, k=18` の第2成分は `Element=42` ですが、`gen_coe=1 1 0 ...` なので生成元は `ξ''+λ''` です。

## 実装

全表示元を `Element` から型付きで構成し、各 `gen_coe` から `Sum` / `Multiple` を組み合わせて巡回成分の生成元を作ります。DB行の値が欠損・不整合なら、推測せずに空の候補を返します。DBは証明根拠に変換しません。Rendererは変更しません。

## 実行

PowerShellで `run.ps1` を実行してください。バックアップを作成した後、限定pytestを実行します。全体pytestは行いません。

## 完了条件と境界

限定テストがPASSし、Webで `π_28^10` の第2生成元が `ξ'' + λ''` と表示されること。Phaseの証明探索には着手しません。
