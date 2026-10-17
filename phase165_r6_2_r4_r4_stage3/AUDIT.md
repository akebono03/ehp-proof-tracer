# Phase 165 R6-2 R4-4 第3段階

## 対象

- `map_property_rules.py` の末尾に `ImageZeroStatement`、`KernelWholeStatement` を追加。
- `exactness_and_zero_image_implies_zero_kernel_inference_rule()` を追加。
- `exactness_and_whole_kernel_implies_whole_image_inference_rule()` を追加。
- 既存の import、クラス、関数は変更しない。

## 数学的条件

正確な連続写像 $A\xrightarrow{f}B\xrightarrow{g}C$ に対して $\operatorname{Im}f=\ker g$ を前提とする。

- $\operatorname{Im}f=0$ なら $\ker g=0$。
- $\ker g=B$ なら $\operatorname{Im}f=B$。

これらの規則は `ExactnessStatement` と、型付きの零像・全核命題を必要とする。`KernelStatement` および `ImageStatement` の任意の `structure` 値から上の命題を捏造しない。

## 制約・次段階

逆向きで隣接する写像の変数が結論だけから束縛されない場合、R26 は候補生成を拒否する。文献証人による正しい束縛と EHP の型の橋渡しが今後必要。$\pi_4^3$ 専用 Adapter は復活させない。全体 pytest は未実施。
