# ehp_proof 設計メモ

## 基本方針

EHP 完全列に固有の処理と、
一般的なアーベル群の計算を分離する。

一般的な群論処理は `algebra.py` に置き、
`ehp.py` はそれらを組み合わせて
EHP 完全列を扱う薄い層とする。

将来的に、

- double EHP
- Toda bracket
- composition relations
- その他の完全列

を追加したときにも、同じ algebra 層を再利用できる構造を目指す。

---

## Subgroup の設計

部分群は単なる元の集合ではなく、

- ambient group
- elements
- generators
- abstract structure

を持つオブジェクトとして扱う。

理由:

EHP 完全列で

```text
Im(E)
Ker(H)
Im(H)
Ker(P)
```

などを単なる集合ではなく、
群構造として比較・推論するため。

`Subgroup.structure()` により、

```text
()
(2,)
(4,)
(2, 2)
(2, 4)
```

などの有限アーベル群の抽象構造を取得する。

---

## QuotientGroup の設計

完全列

```text
A --f--> B --g--> C
```

から

```text
B / Im(f) ≅ Im(g)
```

を扱うため、商群を独立したオブジェクトとして表現する。

`QuotientGroup` は、

- ambient_group
- subgroup
- cosets
- quotient addition
- order
- abstract structure

を持つ。

現段階では有限アーベル群のみ対応する。

商群を単に位数だけで扱わず、

```text
Z/4
```

と

```text
Z/2 ⊕ Z/2
```

のような同じ位数を持つ異なる群も区別する。

---

## InducedMap の設計

準同型

```text
f : G → H
```

について、第一同型定理

```text
G / Ker(f) ≅ Im(f)
```

をプログラム上で明示的に扱う。

`InducedMap` は、

- quotient 上で well-defined か
- injective か
- surjective か
- isomorphism か

を検証する。

これは完全列から商群を推論する際の基礎とする。

---

## ExactSequenceStep の設計

連続する2写像

```text
A --f--> B --g--> C
```

を1つの単位として扱う。

主な責務:

- `Im(f)`
- `Ker(g)`
- exactness
- `B / Im(f)`
- `Im(g)`
- induced isomorphism

完全性

```text
Im(f) = Ker(g)
```

から、

```text
B / Im(f) ≅ Im(g)
```

を導く。

この一般的な完全列処理を EHP 固有コードから分離する。

---

## Extension の扱い

短完全列

```text
0 → A → B → C → 0
```

だけでは `B` は一般に一意に決まらない。

例えば、

```text
0 → Z/2 → B → Z/2 → 0
```

では、

```text
B ≅ Z/4
```

または

```text
B ≅ Z/2 ⊕ Z/2
```

が可能。

そのため、未知群を即座に1つへ決定せず、
candidate の集合として保持する設計とする。

この曖昧性はエラーではなく、
完全列から得られる情報そのものとして扱う。

将来的には、

- composition relations
- Toda brackets
- Steenrod operations
- 元の位数
- 文献上の関係式

などを追加条件として使い、
候補集合を絞り込む。

---

## ExtensionCandidate の設計

候補中間群 `B` が

```text
0 → A → B → C → 0
```

の中間群として成立可能かを判定する。

具体的には `B` の部分群 `H` で、

```text
H ≅ A
B / H ≅ C
```

となるものが存在するかを調べる。

現段階では有限アーベル群を対象とし、
小さな群について全部分群を列挙して検証する。

---

## 有限アーベル群候補の自動生成

短完全列

```text
0 → A → B → C → 0
```

では有限群の場合、

```text
|B| = |A| |C|
```

となる。

この位数から有限アーベル群の
invariant factor decomposition

```text
Z/d1 ⊕ ... ⊕ Z/dr

d1 | d2 | ... | dr
```

を満たすすべての同型型を生成する。

例えば

```text
|B| = 8
```

なら、

```text
Z/8
Z/2 ⊕ Z/4
Z/2 ⊕ Z/2 ⊕ Z/2
```

を生成する。

その後 `ExtensionCandidate` によって
実際に short exact sequence を構成可能な候補だけを残す。

候補の列挙と extension の成立判定を分離する。

---

## EHP と extension 推論の接続

EHP の連続する写像

```text
A --f--> B --g--> C
```

が完全なら、

```text
0 → Im(f) → B → Im(g) → 0
```

という短完全列が得られる。

したがって未知の中間群 `B` を推論するときに使うのは、
元の `A`, `C` そのものではなく、

```text
Im(f)
Im(g)
```

である。

`ExactSequenceStep` がこれらを抽象群として取り出し、
extension candidate の生成へ渡す。

EHP 層はこの一般機構を wrapper として利用する。

---

## algebra 層と EHP 層の分離

一般的な群論処理は `algebra.py` に置く。

主な対象:

- group elements
- homomorphisms
- subgroup
- quotient
- induced map
- exact sequence
- extension candidates
- finite abelian group classification

`ehp.py` は、

- E
- H
- P

を構成し、一般的な algebra 層へ渡す。

これにより将来、

- double EHP
- Toda bracket
- その他の完全列

でも同じ algebra 層を再利用できるようにする。

---

## 既知値と推論結果を区別する

`sphere.csv` に記録された群構造は既知データである。

一方、EHP 完全列から生成された

```text
Z/8
Z/2 ⊕ Z/4
```

などは推論候補である。

両者は混同しない。

既知値を使って候補を生成するのではなく、

```text
EHP data
→ exactness
→ extension
→ candidate structures
```

として候補を生成し、
必要に応じて既知値と比較する。

将来的な Proof Tracer では、

- known
- derived
- candidate
- excluded

の区別を明示的に持たせることを検討する。

---

## presentation ベースの一般アーベル群計算

初期実装では、一部の群論処理について

* 群の全元
* 部分群の全列挙
* quotient cosets

を実際に列挙していた。

この方式は小さな有限アーベル群では実装が単純であり、
結果を直接確認しやすいという利点がある。

一方、

```text
Z
Z ⊕ Z/2
Z^2
```

など自由部分を含む群では全元列挙はできない。

そのため Phase 4 では、
有限生成アーベル群を presentation として扱う計算経路を導入した。

基本的な計算経路は、

```text
finitely generated abelian group
↓
relation matrix
↓
integer lattice
↓
Hermite normal form
↓
Smith normal form
↓
kernel / image / cokernel
```

とする。

これにより、

```text
Z^r ⊕ finite torsion
```

という一般の有限生成アーベル群を
同じ algebra 層で扱えるようにする。

---

## 有限群列挙方式の位置づけ

presentation ベースの計算を一般的な計算経路とするが、
有限群の全元列挙方式は削除しない。

有限群では、

```text
全元列挙方式
```

と

```text
presentation / lattice / HNF / SNF
```

という独立した2通りの計算が可能である。

したがって全元列挙方式は、

> presentation 計算を検証するための reference implementation

として利用する。

有限群に対する

```text
kernel
image
cokernel
exactness
```

について両方式を cross-check することで、
presentation ベースの一般計算に対する
回帰テストとして利用する。

---

## algebra 層の責務

`algebra.py` は有限生成アーベル群とその準同型に関する
一般的な代数計算を担当する。

主な責務は、

* finitely generated abelian groups
* group homomorphisms
* presentations
* integer lattices
* kernel
* image
* cokernel
* subgroup
* quotient
* induced map
* exact sequence
* extension candidates
* finite abelian group classification

である。

algebra 層は、

```text
E
H
P
Toda bracket
composition relation
```

などのホモトピー論的意味を知らない。

例えば、

```text
f : G → H
```

が suspension homomorphism `E` であるかどうかに関係なく、
単なる有限生成アーベル群の準同型として処理する。

---

## EHP 層の責務

`ehp.py` は EHP 完全列に固有の情報を管理する。

主な責務は、

* 対象となるホモトピー群を選ぶ
* E, H, P を構成する
* source / target generators を対応させる
* EHP データから準同型行列を構成する
* algebra 層の完全列計算を呼び出す

ことである。

依存方向は、

```text
EHP layer
↓
GroupMap / ExactSequenceStep
↓
algebra layer
```

とする。

`algebra.py` から `ehp.py` への依存は作らない。

これにより将来、

* double EHP
* Toda bracket
* composition relations
* その他の完全列

を導入した場合にも、
同じ algebra 層を再利用できる。

---

## 群構造と generator の数学的名称の分離

抽象アーベル群の構造と、
ホモトピー群の generator の数学的意味は分離する。

例えば、

```text
π ≅ Z/8 ⊕ Z/4 ⊕ Z/2
```

について algebra 層が必要とするのは、

```text
Z/8
Z/4
Z/2
```

という抽象群構造である。

一方、

```text
ξ'
ξ' + λ'
η11 μ̄12
```

などの generator 名や、
それらの Toda 的・ホモトピー論的意味は
homotopy data 層で管理する。

これにより、
純粋なアーベル群計算と
数学的 generator relation を混同しない。

---

## 完全性と抽象群同型の区別

完全列

```text
A --f--> B --g--> C
```

における完全性は、

```text
Im(f) = Ker(g)
```

という `B` の部分群としての一致で判定する。

一方、完全性から第一同型定理により得られる

```text
B / Im(f) ≅ Im(g)
```

は抽象アーベル群としての同型である。

したがって、

```text
部分群として等しい
```

ことと、

```text
抽象群として同型
```

であることを別の概念として扱う。

単に両者の抽象群構造が同じであることを理由に
完全性を判定してはならない。

---

## primary decomposition の設計境界

algebra 層では、

```text
Z/2
Z/4
Z/3
Z/9
Z/5
```

などをすべて同じ有限生成アーベル群として扱う。

algebra 層自体には、

```text
2-primary
3-primary
p-primary
```

というホモトピー論上の区別を持ち込まない。

将来的に、

```text
classical EHP
double EHP
2-primary data
3-primary data
```

など異なる計算・データソースを導入しても、
最終的には同じ `AbelianGroup` / `GroupMap` の計算基盤へ渡す。

したがって primary decomposition は、
必要に応じて homotopy data / inference 層で扱う。

---

## 計算エンジンと proof engine の境界

現在の algebra / EHP 計算基盤が担当するのは、

```text
既知の群
+
既知の準同型
↓
kernel / image / cokernel
↓
exactness
↓
quotient / extension
↓
群構造候補
```

という計算である。

一方、

```text
E(α) = β
H(γ) = δ
P(ε) = ζ
```

などの準同型データそのものを
数学的定理から導出することは別の責務とする。

将来の proof / inference layer では、

* composition relations
* Toda brackets
* Steenrod operations
* Hopf invariant
* stable range
* literature references
* 元の位数
* 既知の定理

などを用いて、

```text
数学的事実
↓
準同型・relation
↓
algebra layer
```

という推論を行う。

つまり、

```text
proof / inference layer
↓
homotopy / EHP data layer
↓
abelian group algebra
↓
integer linear algebra
```

という層構造を基本とする。

---

## Phase 4 時点の設計原則

Phase 4 以降は、次の原則を維持する。

1. 有限生成アーベル群を統一的に扱う。
2. 自由部分を特殊ケースとして別実装しない。
3. kernel / image / cokernel の一般計算は presentation を中心とする。
4. 有限群の全元列挙は reference implementation として残す。
5. algebra 層は EHP や Toda の意味論を知らない。
6. 群の抽象構造と generator の数学的名称を分離する。
7. E/H/P の構築は EHP / homotopy data 層の責務とする。
8. exactness は一般の群準同型に対する algebra の概念として扱う。
9. 2-primary / odd-primary の区別を algebra 層へ持ち込まない。
10. 既知データからの代数計算と、定理から事実を導く proof engine を分離する。

この境界を維持することで、
将来 Toda の計算を拡張した場合にも、
algebra 基盤を作り直さずに利用できる構造を目指す。

# Proof / Relation 層

Phase 5 では、algebra 層および EHP 層の上に、
証明過程を追跡するための proof / inference 層を導入する。

---

## Relation の設計

`Relation` は、
既知の数学的事実や関係式を表す。

例えば、

```text
2η_n = 0
E(ν_n) = ν_{n+1}
```

のような関係や、

* 元の位数に関する関係
* composition relation
* suspension に関する関係
* 文献から与えられる既知関係

などを扱う。

`Relation` は数学的な入力データであり、
algebra 層による計算結果そのものではない。

例えば、

```text
2η_n = 0
```

が既知の関係式として与えられている場合は
`Relation` として扱う。

一方、

```text
Ker(f) ≅ Z/2
```

が実際の kernel 計算から得られた場合は、
`Relation` ではなく計算によって得られた
`ProofStep` として扱う。

---

## RelationType の設計

関係式の種類を区別するため、
`RelationType` を持たせる。

Phase 5-1 では最小限として、

```text
EQUALITY
ZERO
ORDER
```

を定義する。

現段階では関係式の種類を細かく分類しすぎず、
必要になった段階で、

* composition
* suspension
* Hopf invariant
* Whitehead product
* Toda bracket

などへ拡張する。

---

## ProofStep の設計

`ProofStep` は、
1回の推論または計算を表す。

基本構造は、

```text
premises
↓
rule
↓
conclusion
```

とする。

`ProofStep` は、

* `premises`
* `rule`
* `conclusion`
* 必要に応じた補足情報

を持つ。

例えば、

```text
Ker(H) = ...
Im(E) = ...
```

という計算結果や、

```text
Im(E) = Ker(H)
```

という EHP 完全性の適用を、
それぞれ独立した `ProofStep` として記録する。

---

## ProofRule の設計

`ProofStep` がどの種類の推論によって得られたかを
`ProofRule` で表す。

Phase 5-1 では、

```text
GIVEN
RELATION
EHP_EXACTNESS
KERNEL_COMPUTATION
IMAGE_COMPUTATION
COKERNEL_COMPUTATION
```

を定義する。

これにより、

```text
既知事実
数学的 relation の適用
EHP 完全性
kernel 計算
image 計算
cokernel 計算
```

を区別して記録できるようにする。

将来的には、

* composition relation
* Toda bracket
* Steenrod operation
* stable range
* literature theorem

などの推論規則を追加する。

---

## Proof の設計

`Proof` は、
ある特定の結論に対する導出全体を表す。

Phase 5-1 では、

```text
conclusion
steps
```

を持つ単純な構造とする。

例えば、

```text
step 1:
  Ker(H) を計算

step 2:
  Im(E) を計算

step 3:
  EHP 完全性を適用

step 4:
  群構造を決定
```

という一連の推論を
1つの `Proof` として保持する。

将来的には複数の推論が同じ中間結果を共有するため、
Proof は依存関係グラフとして扱うことを想定する。

ただし Phase 5-1 では、
まず `ProofStep` の順序付きリストとして保持し、
DAG 構造そのものはまだ実装しない。

---

## Relation と ProofStep の役割分担

`Relation` と `ProofStep` は明確に区別する。

```text
Relation
= 既知の数学的事実・関係式

ProofStep
= 既知事実や計算結果を使った1回の推論

Proof
= 特定の結論に至る ProofStep の集合
```

例えば、

```text
2η_n = 0
```

が文献から既知なら `Relation` である。

一方、

```text
Ker(H) ≅ Z/2
```

を `algebra.py` の kernel 計算によって得た場合は
`ProofStep` である。

この区別により、

```text
数学的入力
```

と

```text
プログラムによる計算・推論
```

を混同しない。

---

## algebra 層との境界

algebra 層は、
Proof / Relation 層の存在を知らない。

`algebra.py` は引き続き、

* finitely generated abelian groups
* homomorphisms
* kernel
* image
* cokernel
* quotient
* exactness
* extension

などの純粋な代数計算だけを担当する。

Proof 層は algebra 層の計算結果を利用できるが、
algebra 層の数学的意味論を変更しない。

依存方向は、

```text
proof / inference layer
↓
homotopy / EHP data layer
↓
algebra layer
↓
integer linear algebra
```

とする。

`algebra.py` から proof 層への依存は作らない。

---

## ホモトピー論的対象との境界

Phase 5-1 では、

```text
η_n
ν_n
σ_n
```

などのホモトピー元を
専用クラスとしてまだ実装しない。

また、

```text
2η_n
η_n ○ η_{n+1}
E(ν_n)
```

などを表す式構造もまだ導入しない。

そのため Phase 5-1 の `Relation` や `ProofStep` では、
`lhs`、`rhs`、`premises`、`conclusion` に
一時的に汎用的な値を保持できる設計とする。

ホモトピー元や式を構造化する仕組みは、
Phase 5-2 以降で導入する。

---

## Phase 5-1 時点の設計原則

Phase 5-1 では、次の原則を採用する。

1. `Relation` は既知の数学的事実を表す。
2. `ProofStep` は1回の推論または計算を表す。
3. `Proof` は特定の結論に対する導出全体を表す。
4. 数学的入力と計算結果を区別する。
5. algebra 層に proof の概念を持ち込まない。
6. Proof 層は algebra 層の計算結果を利用する側とする。
7. Proof は将来的に依存関係グラフへ拡張可能な設計とする。
8. Phase 5-1 では DAG を実装せず、順序付き `ProofStep` の集合として保持する。
9. ホモトピー元や式の構造化は Phase 5-2 以降へ分離する。
10. Phase 5-1 では既存の EHP / algebra 計算機能を変更しない。

# Expression / HomotopyElement 層

Phase 5-2 では、
`Relation` の左辺・右辺などに現れるホモトピー論的な式を、
単なる文字列ではなく構造化されたオブジェクトとして扱うための
最小 Expression モデルを導入する。

Phase 5-1 では例えば、

```text
2η3 = 0
```

を文字列として保持していた。

Phase 5-2 ではこれを、

```text
Multiple(2, eta(3))
=
Zero()
```

のような構造として表現できるようにする。

これにより、
後の proof / inference 層から式の内部構造を参照し、
relation の適用や式変形を機械的に扱えるようにする。

---

## Expression の設計

`Expression` は、
ホモトピー論的な式を表すための基底クラスとする。

Phase 5-2 では最小構成として、

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
└── Composition
```

を導入する。

現段階では式の評価や簡約は行わず、
数学的な構造を保持することだけを責務とする。

例えば、

```text
2η_3
```

は、

```text
Multiple
├── coefficient = 2
└── expression = η_3
```

として保持する。

また、

```text
η_3η_4
```

は、

```text
Composition
├── left = η_3
└── right = η_4
```

として保持する。

---

## Zero の設計

零元を文字列 `"0"` ではなく、
独立した `Zero` オブジェクトとして表す。

例えば、

```text
2η_3 = 0
```

という relation は、

```text
lhs = Multiple(2, eta(3))
rhs = Zero()
```

として保持する。

零元を専用オブジェクトとして扱うことで、
将来的に文字列表現に依存せず、

```text
式が零か
零との relation か
```

などを判定できるようにする。

---

## HomotopyElement の設計

`HomotopyElement` は、
個々のホモトピー元の名前と添字を保持する。

Phase 5-2 では、

```text
name
dimension
```

を持つ最小構造とする。

例えば、

```text
η_3
ν_4
σ_8
```

をそれぞれ、

```text
HomotopyElement("η", 3)
HomotopyElement("ν", 4)
HomotopyElement("σ", 8)
```

として表す。

現段階では、
その元が実際にどのホモトピー群に属するか、
source / target dimension が何か、
stable element との対応が何か、
といった意味論までは持たせない。

それらは必要になった段階で
homotopy data 層として拡張する。

---

## generator factory の設計

頻繁に使う基本 generator については、
直接 `HomotopyElement` を構築する代わりに、

```text
eta(n)
nu(n)
sigma(n)
```

という factory function を用意する。

例えば、

```text
eta(3)
```

は、

```text
HomotopyElement("η", 3)
```

を生成する。

これにより、
relation データを記述するときの可読性を高める。

将来的に必要に応じて、

```text
mu(n)
epsilon(n)
xi(n)
```

などを追加する。

factory function は数学的な新しい型を導入するものではなく、
`HomotopyElement` を簡潔に生成するための補助とする。

---

## Multiple の設計

整数倍を表すために `Multiple` を導入する。

`Multiple` は、

```text
coefficient
expression
```

を持つ。

例えば、

```text
2η_3
```

を、

```text
Multiple(
  2,
  eta(3),
)
```

として表す。

これにより、

```text
係数が何か
どの式の整数倍か
```

を文字列解析なしで取得できる。

Phase 5-2 では、
係数の正規化や、

```text
1α = α
0α = 0
(-1)α = -α
```

などの簡約は行わない。

式の簡約は Expression のデータモデルとは別の責務として扱う。

---

## Composition の設計

ホモトピー元の合成を表すために
`Composition` を導入する。

`Composition` は、

```text
left
right
```

を持つ。

例えば、

```text
η_3η_4
```

を、

```text
Composition(
  eta(3),
  eta(4),
)
```

として保持する。

Phase 5-2 では、
composition が実際に定義可能かどうかの dimension check は行わない。

また、

```text
Composition(alpha, beta)
```

を数学的にどちら向きの写像合成として解釈するかについても、
現段階では式構造の保持に限定する。

Toda の記法との対応や、
source / target dimension に基づく妥当性検査は
後の homotopy expression 層で追加する。

---

## Expression と文字列表現の分離

Phase 5-2 では、
`Expression` に表示処理を持たせない。

例えば、

```text
eta(3)
```

を、

```text
η3
η₃
\eta_3
```

のどの形式で表示するかは、
Expression 自体の数学的構造とは別の問題である。

将来的には、

```text
Expression
↓
formatter
├── plain text
├── Unicode
└── TeX
```

のように表示層を分離することを想定する。

そのため Phase 5-2 では、
`__str__` や TeX 出力などは導入しない。

---

## Expression と Relation の接続

Phase 5-1 で導入した `Relation` は、

```text
lhs
rhs
```

を持つ。

Phase 5-2 では、
これらに Expression オブジェクトを入れられることを確認する。

例えば、

```text
2η_3 = 0
```

を、

```text
Relation(
  lhs=Multiple(2, eta(3)),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

として保持できる。

これにより、
既知 relation を文字列ではなく
構造化された数学データとして管理する基礎ができる。

---

## Relation の型をまだ Expression に限定しない

Phase 5-2 時点では、
`Relation` の、

```text
lhs
rhs
```

の型を `Expression` に固定しない。

今後、

```text
ord(α) = 2
Ker(H) = ...
Im(E) = ...
π_n(S^m) ≅ Z/2
```

など、
単純なホモトピー元の式とは異なる種類の命題を
proof engine で扱う可能性があるためである。

したがって現段階では、

```text
Expression
```

と、

```text
Statement
```

の責務をまだ統合しない。

Phase 5-2 では、
Relation の中に Expression を格納できることだけを保証する。

より一般的な Statement モデルが必要かどうかは、
実際の proof trace を構築する段階で判断する。

---

## EHP 層との境界

Phase 5-2 では、
`expression.py` と既存の `ehp.py` をまだ接続しない。

現在の EHP 層では、
repository から取得した generator 名などを利用して
準同型を構築している。

Phase 5-2 の目的は、
これを直ちに置き換えることではない。

まず、

```text
数学的な式を構造化して保持できる
```

という独立した基盤を作り、
既存 EHP 計算を壊さないことを優先する。

したがって、

```text
algebra.py
ehp.py
repository.py
```

の既存仕様は Phase 5-2 では変更しない。

---

## Expression 層の責務

`expression.py` は、
ホモトピー論で使用する式の構造だけを担当する。

Phase 5-2 時点での責務は、

* ホモトピー元の表現
* 零元の表現
* 整数倍の表現
* composition の表現

である。

一方、

* 群演算の実計算
* kernel / image / cokernel
* EHP 完全性
* relation の検索
* relation の適用
* expression の簡約
* dimension の整合性判定
* Toda bracket
* Steenrod operation
* suspension
* Hopf invariant

などは担当しない。

---

## algebra 層との境界

`Expression` は、
`algebra.py` の `GroupElement` とは別の概念とする。

`GroupElement` は、
具体的な有限生成アーベル群内部の元として
代数計算を行うためのオブジェクトである。

一方 `HomotopyElement` は、

```text
η_n
ν_n
σ_n
```

などの数学的名称を持つホモトピー元を表す。

したがって、

```text
HomotopyElement
≠
GroupElement
```

とする。

将来的には homotopy data 層によって、

```text
HomotopyElement
↓ 対応付け
GroupElement
```

という関係を持たせる可能性があるが、
両者を同一クラスにはしない。

これにより、

```text
数学的 generator の意味
```

と、

```text
抽象アーベル群内での座標
```

を分離する。

---

## Phase 5-2 時点の設計原則

Phase 5-2 では、次の原則を採用する。

1. ホモトピー論的な式を文字列ではなく構造化して保持する。
2. `Expression` を式構造の基底とする。
3. 零元は `Zero` として独立して表現する。
4. 基本 generator は `HomotopyElement` として表現する。
5. 整数倍は `Multiple` として表現する。
6. composition は `Composition` として表現する。
7. `eta(n)`、`nu(n)`、`sigma(n)` は generator 生成の補助関数とする。
8. Expression 層では式の評価や簡約を行わない。
9. Expression 層では composition の dimension 妥当性をまだ検証しない。
10. Expression と表示形式を分離する。
11. `HomotopyElement` と algebra 層の `GroupElement` を混同しない。
12. `Relation` は Expression を保持できるが、まだ Expression 専用にはしない。
13. Expression より広い Statement モデルの必要性は後の proof engine 実装時に判断する。
14. Phase 5-2 では既存の algebra / EHP / repository の仕様を変更しない。

この境界を維持することで、
今後 relation repository、
proof trace、
composition relations、
Toda bracket などを追加する際にも、
既存の algebra 基盤とホモトピー論的な式表現を分離したまま拡張できる構造を目指す。


# Relation Repository / Proof 構築 / Formatter

Phase 5-3 以降では、
Phase 5-1 で導入した `Relation` / `ProofStep` / `Proof` と、
Phase 5-2 で導入した `Expression` を接続し、
既知 relation の検索から proof trace の構築・表示までを
段階的に実装する。

---

## RelationRepository の設計

既知の数学的 relation を保存・検索するため、
`RelationRepository` を導入する。

`RelationRepository` は、

```text
Relation の保存
Relation の検索
```

のみを責務とする。

検索条件として、

```text
lhs
rhs
relation_type
source
```

を利用できる。

複数条件が指定された場合は AND 条件として扱う。

Expression は構造的 equality を持つため、

```python
Multiple(
  2,
  eta(3),
)
```

のような式を、
文字列へ変換せずそのまま検索キーとして利用する。

`RelationRepository` 自体は、

```text
relation の適用
式変形
proof の生成
自動推論
```

を行わない。

これらは proof / inference 層の責務とする。

---

## Relation から ProofStep への変換

Repository から取得した `Relation` を
証明の一部として扱うため、

```python
relation_proof_step()
```

を導入する。

Relation は、

```text
既知の数学的事実
```

そのものであり、

ProofStep は、

```text
証明の中でその事実を使用可能な形にしたもの
```

とする。

したがって、

```text
Relation
↓
relation_proof_step()
↓
ProofStep
```

という変換を行う。

Relation を直接 Proof の依存関係に置くのではなく、
Proof の中では原則として ProofStep を依存単位とする。

---

## algebra 計算結果の ProofStep 化

kernel / image / cokernel の計算結果についても、
単なる返り値ではなく ProofStep として記録できるようにする。

対応する関数は、

```text
kernel_proof_step()
image_proof_step()
cokernel_proof_step()
```

とする。

それぞれ、

```text
Ker(f)
Im(f)
Coker(f)
```

の一般アーベル群構造を計算し、

```text
KernelStatement
ImageStatement
CokernelStatement
```

として conclusion に保持する。

これらは algebra 層そのものを変更するのではなく、
proof 層から既存 algebra API を呼び出して
計算結果を ProofStep として包む構造とする。

依存方向は引き続き、

```text
proof layer
↓
algebra layer
```

とする。

---

## Exactness の ProofStep 化

連続する準同型

```text
A --f--> B --g--> C
```

について、

```text
Im(f)
Ker(g)
```

の計算結果を premises とし、

```text
Im(f) = Ker(g)
```

を conclusion とする ProofStep を構成する。

基本形は、

```text
image step
kernel step
↓
exactness rule
↓
Im(f) = Ker(g)
```

とする。

このため、

```python
exactness_proof_step()
```

は、

```text
image_step
kernel_step
```

を明示的な premises として保持する。

EHP 完全列については、

```python
ehp_exactness_proof_step()
```

を用い、

```text
ProofRule.EHP_EXACTNESS
```

として一般の exactness と区別する。

---

## EHP Proof の構築

EHP 完全列の一部分について、

```text
Im(E)
Ker(H)
Im(E) = Ker(H)
```

または、

```text
Im(H)
Ker(P)
Im(H) = Ker(P)
```

という proof trace を自動構築する。

例えば sphere 側では、

```text
step 1:
Im(E) を計算

step 2:
Ker(H) を計算

step 3:
step 1, step 2 を前提として
Im(E) = Ker(H)
```

という構造を持つ。

この proof を、

```python
ehp_sphere_proof()
```

および、

```python
ehp_hopf_target_proof()
```

から取得できるようにする。

これにより従来の、

```text
exactness = True
```

という結果だけでなく、

```text
なぜ exact と判定されたか
```

を Proof として保持できる。

---

## Proof の premises

ProofStep の依存関係は `premises` に保持する。

Phase 5 初期では `premises` に汎用値を入れられる設計としていたが、
proof trace を構築する段階では、
ProofStep 同士の依存関係を主要な利用方法とする。

例えば、

```text
step 1
Im(E) ≅ 0

step 2
Ker(H) ≅ 0

step 3
Im(E) = Ker(H)
```

では、

```python
step3.premises == (
  step1,
  step2,
)
```

となる。

これにより Proof の `steps` は順序付きリストのままでも、
各 step がどの step に依存するかを追跡できる。

Phase 5 では完全な DAG オブジェクトはまだ導入せず、
ProofStep の参照によって依存関係を表現する。

---

## Relation を premise とする推論

既知 Relation を使用した推論についても、
Relation を ProofStep に変換した上で
premise として保持する。

基本形は、

```text
Relation
↓
relation_proof_step
↓
relation inference step
```

とする。

例えば、

```text
2η_3 = 0
```

という Relation から、

```text
η_3 has order dividing 2
```

を導く場合、

```text
step 1:
2η_3 = 0
[relation]

step 2:
η_3 has order dividing 2
[relation]
premise = step 1
```

という Proof を構成する。

このため、

```python
relation_inference_proof_step()
```

は `relation_step` を premise として受け取り、
その step が、

```text
ProofRule.RELATION
```

を持ち、かつ conclusion が `Relation` であることを確認する。

これにより、
Repository から取得された既知 relation が、
実際の proof dependency に組み込まれる。

---

## Proof Formatter の設計

Proof の内部データ構造と表示処理を分離するため、
formatter 層を導入する。

formatter は、

```text
Expression
Statement
ProofStep
Proof
```

を人間が読める文字列表現へ変換する。

主な関数は、

```text
format_expression()
format_statement()
format_proof_step()
format_proof()
```

とする。

Expression や Proof 自体には
表示形式を持たせない。

これにより将来的に、

```text
plain text
Unicode
TeX
Markdown
HTML
```

など複数の表示形式へ拡張できる余地を残す。

---

## ProofStep の番号と依存関係表示

Proof を表示するとき、
各 ProofStep に通し番号を付ける。

例えば、

```text
1. Im(E) ≅ 0
2. Ker(H) ≅ 0
3. Im(E) = Ker(H)
```

とする。

さらに step 3 の premises が
step 1 と step 2 である場合、

```text
Premises: 1, 2
```

と表示する。

Proof 内部では ProofStep のオブジェクト参照を保持し、
formatter が Proof 内での番号へ変換する。

したがって proof model 自体は、
表示用の step number を保持しない。

step number は表示層だけの概念とする。

---

## Relation metadata と ProofStep metadata の区別

`Relation` と `ProofStep` は、
それぞれ独立した補足情報を持つことができる。

Relation の、

```text
source
note
```

は、
既知の数学的事実そのものに関する metadata とする。

例えば、

```text
source = "Toda"
note = "stable range"
```

などである。

一方 `ProofStep.note` は、
その relation や計算結果を今回どのように使用したかという
推論上の補足情報とする。

したがって、

```text
Relation.note
```

と、

```text
ProofStep.note
```

は統合しない。

将来的な proof formatter では、
必要に応じて両方を表示できるようにする。

---

## Phase 5-10 時点の proof pipeline

現在の proof / inference 基盤は、

```text
Expression
↓
Relation
↓
RelationRepository
↓
relation_proof_step
↓
ProofStep
↓
premises
↓
Proof
↓
formatter
```

という経路を持つ。

また EHP 計算については、

```text
GroupMap
↓
kernel / image calculation
↓
ProofStep
↓
exactness ProofStep
↓
Proof
↓
formatter
```

という経路を持つ。

これにより、

```text
既知 relation に基づく推論
```

と、

```text
algebra / EHP 計算に基づく推論
```

を同じ Proof / ProofStep モデルで表現できる基盤ができた。

---

## Phase 5-10 時点の設計原則

1. Relation は既知の数学的事実として保持する。
2. Repository は relation の保存・検索のみを担当する。
3. Relation を proof で利用するときは ProofStep に変換する。
4. kernel / image / cokernel の計算結果も ProofStep とする。
5. exactness は image / kernel step を premises とする。
6. EHP exactness は一般 exactness と同じ構造を利用する。
7. ProofStep 同士の依存関係は premises で表現する。
8. Proof の step number は formatter 側だけで付与する。
9. Proof model と表示処理を分離する。
10. Relation の metadata と ProofStep の metadata を区別する。
11. algebra 層は proof 層を知らない。
12. Proof はまだ専用 DAG 型へ変更せず、順序付き step と参照によって依存関係を表現する。
13. Relation の適用は現段階では明示的に構築し、一般的な pattern matching や自動推論はまだ行わない。
14. 既知 relation と algebra 計算の両方を同一の Proof モデルへ統合できる構造を維持する。


# Relation metadata / LiteratureReference

## Relation metadata の表示

Phase 5-11 では、
Relation および ProofStep が保持している metadata を
Proof formatter へ反映する。

対象は、

```text
Relation.source
Relation.note
ProofStep.note
```

である。

`Relation.source` は、
その数学的 relation がどこから得られたかを表す。

`Relation.note` は、
relation 自体についての数学的補足情報を表す。

一方、

`ProofStep.note` は、
その relation や計算結果を今回の推論で
どのように利用したかについての補足とする。

したがって、

```text
Relation.note
```

と、

```text
ProofStep.note
```

は統合しない。

例えば、

```text
1. 2η_3 = 0
   [relation]
   Source: Toda
   Relation note: classical eta relation

2. η_3 has order dividing 2
   [relation]
   Premises: 1
   Note: derived from the zero relation
```

のように、
数学的事実そのものの metadata と
推論 step の metadata を区別して表示する。

---

## LiteratureReference の設計

Phase 5-12 では、
Relation の出典を単なる文字列ではなく、
構造化された文献参照として保持できるようにする。

そのため、

```text
LiteratureReference
```

を導入する。

基本構造は、

```text
label
author
title
year
locator
```

とする。

例えば、

```python
LiteratureReference(
  label="Toda",
  author="H. Toda",
  title=(
    "Composition Methods in "
    "Homotopy Groups of Spheres"
  ),
  year=1962,
  locator="...",
)
```

のように文献情報を保持できる。

ここで、

```text
label
```

は Proof 表示や簡潔な識別に使用する名前、

```text
author
title
year
```

は書誌情報、

```text
locator
```

は relation が文献中のどこに記載されているかを表す
位置情報とする。

locator には将来的に、

```text
Theorem ...
Proposition ...
Lemma ...
Chapter ...
p. ...
equation (...)
```

などを格納できる。

現段階では locator の内部構造までは分解せず、
文字列として保持する。

---

## Relation.source の後方互換性

Phase 5-12 では、

```text
Relation.source
```

を完全に `LiteratureReference` 専用にはしない。

型は、

```text
LiteratureReference | str | None
```

とする。

これにより従来の、

```python
source="Toda"
```

も引き続き利用できる。

新しく構造化された source を利用する場合は、

```python
source=LiteratureReference(...)
```

とする。

この後方互換性によって、
既存 Relation データを一度に書き換える必要をなくし、
relation データの追加に合わせて段階的に
structured source へ移行できる。

---

## LiteratureReference と Relation.note の区別

文献情報と数学的補足は混在させない。

例えば、

```text
Toda の Proposition ...
```

のような文献上の位置は、

```text
LiteratureReference.locator
```

に保持する。

一方、

```text
stable range で成立
classical eta relation
```

など relation 自体の数学的説明は、

```text
Relation.note
```

に保持する。

したがって、

```text
LiteratureReference
= relation の出典情報

Relation.note
= relation の数学的補足

ProofStep.note
= その relation を利用した推論上の補足
```

という3つの責務を分離する。

---

## LiteratureReference の表示

formatter 層では、

```text
format_literature_reference()
format_source()
```

によって source を表示する。

structured source の例:

```text
Source: Toda — H. Toda, Composition Methods in Homotopy Groups of Spheres, 1962 — ...
```

従来の文字列 source:

```text
Source: Toda
```

も同じ formatter から表示できる。

文献情報の表示方法は formatter 層の責務とし、
`LiteratureReference` 自体に表示処理を持たせない。

---

## RelationRepository との接続

`LiteratureReference` は frozen dataclass として
構造的 equality を持つ。

そのため既存の `RelationRepository` を変更せず、

```python
repository.find_relations(
  source=reference,
)
```

によって structured source を持つ relation を検索できる。

Phase 5-12 では、

```text
author
title
year
label
locator
```

を個別条件として検索する機能は導入しない。

RelationRepository は引き続き、
Relation オブジェクトの保存と基本検索のみを責務とする。

より高度な文献検索や文献データ管理が必要になった場合に、
別途 literature repository 等の導入を検討する。

---

## Phase 5-12 時点の source pipeline

現在、

```text
LiteratureReference
        ↓
Relation.source
        ↓
Relation
        ↓
relation_proof_step
        ↓
Proof
        ↓
format_source
        ↓
Proof trace
```

という経路が成立している。

これにより Proof trace は、

```text
何を使ったか
```

だけでなく、

```text
その数学的事実はどこから得られたか
```

まで追跡できる基盤を持つ。

---

## Phase 5-12 時点の設計原則

1. 文献情報は構造化された `LiteratureReference` として保持できる。
2. `Relation.source` は当面 `LiteratureReference | str | None` とする。
3. 既存の文字列 source との後方互換性を維持する。
4. 書誌情報と relation の数学的 note を分離する。
5. 文献中の位置は `locator` に保持する。
6. locator は現段階では文字列とし、過剰に構造化しない。
7. 文献の表示方法は formatter 層の責務とする。
8. LiteratureReference 自体に表示処理を持たせない。
9. RelationRepository は structured source でも既存 equality 検索を利用する。
10. 文献検索専用 Repository はまだ導入しない。
11. BibTeX / DOI / ISBN 等の管理は必要になった段階で追加する。
12. テスト用 locator と実際の文献 locator を混同しない。


# 複数 premise を用いる Relation inference

## Phase 5-13：Relation inference の一般化

Phase 5-12 までの relation inference は、

```text
1つの Relation
↓
relation ProofStep
↓
inference ProofStep
```

という形を基本としていた。

しかし実際の数学的推論では、

```text
複数の既知 relation
+
既に得られている計算結果
↓
新しい結論
```

という形が必要になる。

Phase 5-13 では、
relation inference が複数の ProofStep を
premises として利用できるように一般化する。

---

## relation_steps と premises の区別

`relation_inference_proof_step()` では、

```text
relation_steps
premises
```

を別の引数として扱う。

`relation_steps` は、

```text
ProofRule.RELATION
```

を持ち、
conclusion が `Relation` である ProofStep に限定する。

一方 `premises` は、
既に得られている一般の ProofStep を受け取る。

例えば、

```text
relation step 1
relation step 2
kernel computation step
↓
relation inference
↓
conclusion
```

のような推論を表現できる。

この区別により、

```text
relation として利用する既知の数学的事実
```

と、

```text
既に得られている計算結果・推論結果
```

を API 上で区別できる。

---

## Proof dependency の単位

Relation を直接 `premises` に格納するのではなく、

```text
Relation
↓
relation_proof_step()
↓
ProofStep
```

という変換を行った上で dependency に利用する。

したがって proof trace における
主要な依存関係の単位は `ProofStep` とする。

これにより、

```text
既知 relation
計算結果
既に導出された中間結果
```

を同じ dependency model で扱える。

例えば、

```text
Relation 1
↓
ProofStep 1

Relation 2
↓
ProofStep 2

kernel computation
↓
ProofStep 3

ProofStep 1, 2, 3
↓
relation inference
↓
ProofStep 4
```

という構造を表現できる。

---

## 単一 Relation との後方互換性

複数 relation へ一般化したが、
従来の、

```python
relation_inference_proof_step(
  conclusion,
  relation_step,
)
```

という単一 premise の形式も維持する。

内部では単一 ProofStep を、

```text
(step,)
```

へ正規化して処理する。

同様に `relation_inference_proof()` も、

```text
Relation
```

または、

```text
tuple/list of Relation
```

の両方を受け取る。

これにより既存コードに breaking change を導入せず、
複数 relation inference へ拡張する。

---

## normalize helper

入力形式を統一するため、

```text
_normalize_proof_steps()
_normalize_relations()
```

を導入する。

`_normalize_proof_steps()` は、

```text
ProofStep
```

または、

```text
tuple/list of ProofStep
```

を受け取り、
内部的には tuple に統一する。

`_normalize_relations()` は、

```text
Relation
```

または、

```text
tuple/list of Relation
```

を受け取り、
内部的には tuple に統一する。

また、
tuple / list 内に不正な型が含まれている場合は、
早い段階で `TypeError` とする。

これにより inference 本体では、
単一入力と複数入力を個別に処理する必要がなくなる。

---

## relation_steps の検証

`relation_inference_proof_step()` に渡される
`relation_steps` は、
単なる ProofStep であれば何でもよいわけではない。

各 step は、

```text
ProofRule.RELATION
```

を持ち、
さらに、

```text
step.conclusion
```

が `Relation` であることを要求する。

したがって、

```text
kernel computation
image computation
given
exactness
```

などの ProofStep を
`relation_steps` として渡すことはできない。

これらを推論の前提として利用する場合は、

```text
premises
```

として渡す。

---

## 追加 premises

Phase 5-13 では、
Relation 以外の既存 ProofStep を、

```text
premises
```

として追加できる。

例えば、

```text
1. α = β
   [relation]

2. γ = δ
   [relation]

3. Ker(H) ≅ Z/2
   [kernel computation]

4. desired conclusion
   [relation]
   Premises: 1, 2, 3
```

のような proof dependency を構築できる。

これにより、

```text
文献上の既知 relation
+
algebra による計算結果
+
以前に導出された結果
```

を組み合わせるための基礎ができる。

---

## 空 relation の禁止

relation inference は、
少なくとも1つの relation を使用するものとする。

したがって、

```text
relation_steps = ()
```

または、

```text
relations = ()
```

は許可しない。

この場合は `ValueError` とする。

relation を使用しない一般的な推論については、
将来的に別の inference rule / API を導入する。

---

## formatter との接続

formatter は既に ProofStep の `premises` を走査し、

```text
Premises: 1, 2, ...
```

と表示できる。

そのため Phase 5-13 では
formatter 本体の変更は必要ない。

例えば、

```text
1. 2η_3 = 0
   [relation]

2. 2η_4 = 0
   [relation]

3. combined result
   [relation]
   Premises: 1, 2
```

のように複数 dependency を表示できる。

Phase 5-13 では integration test を追加し、
複数 Relation を premises とする Proof が
正しく番号表示されることを確認する。

---

## Phase 5-13 時点の inference pipeline

現在、

```text
Relation 1
     ↓
ProofStep 1

Relation 2
     ↓
ProofStep 2

other ProofStep
     ↓

ProofStep 1
ProofStep 2
other ProofStep
     ↓
relation inference
     ↓
new ProofStep
     ↓
Proof
     ↓
formatter
```

という構造を表現できる。

これにより、
単一 relation に基づく例示的な推論から、

```text
複数の数学的事実
+
計算結果
+
既存の推論結果
↓
新しい結論
```

という、
より一般的な proof construction へ進んだ。

---

## ProofStep.premises の型について

`ProofStep` の型定義自体は現在、

```python
premises: tuple[Any, ...]
```

のままとする。

Phase 5-13 の inference API では
premises に ProofStep を要求するが、
既存コードには Relation などを直接 premises に格納する
初期段階の利用例も残っている。

そのため Phase 5-13 では、
`ProofStep.premises` 自体を

```text
tuple[ProofStep, ...]
```

へ変更することは行わない。

Proof 全体で dependency の単位を
ProofStep に統一するかどうかは、
既存コードを整理する後続フェーズで検討する。

---

## Phase 5-13 時点の設計原則

1. Relation は Proof に入る前に ProofStep 化する。
2. Proof dependency の主要単位は ProofStep とする。
3. relation inference は複数 relation を利用できる。
4. relation inference は追加の一般 ProofStep も premise にできる。
5. `relation_steps` と追加 `premises` は API 上区別する。
6. `relation_steps` は `ProofRule.RELATION` を持つ必要がある。
7. `relation_steps` の conclusion は Relation でなければならない。
8. relation inference には少なくとも1つの Relation が必要である。
9. 単一 Relation を利用する従来 API との後方互換性を維持する。
10. 単一入力と複数入力は normalize helper によって統一する。
11. formatter は既存の複数 premises 表示機能をそのまま利用する。
12. `ProofStep.premises` 自体の型制限はまだ強化しない。
13. premises の再帰的収集や DAG 自動構築はまだ行わない。
14. relation の自動検索や pattern matching はまだ導入しない。
15. relation を使用しない一般 inference rule は後続フェーズで検討する。


# InferenceRule と推論規則の構造化

## Phase 5-14：InferenceRule の導入

Phase 5-13 までに、
複数の Relation および既存の ProofStep を
premises とする relation inference を構築できるようになった。

しかし Phase 5-13 時点では、
relation inference によって生成された ProofStep はすべて、

```text
ProofRule.RELATION
```

として扱われていた。

このため、

```text
どの ProofStep を前提として使ったか
```

は `premises` から追跡できる一方、

```text
それらの premises から
どの数学的推論規則を使って
conclusion を導いたのか
```

は構造化されていなかった。

Phase 5-14 では、
この情報を明示的に保持するため、

```text
InferenceRule
```

を導入する。

---

## ProofRule と InferenceRule の区別

`ProofRule` と `InferenceRule` は
異なる責務を持つ。

`ProofRule` は、
ProofStep の処理の大分類を表す。

例えば、

```text
GIVEN
RELATION
EXACTNESS
EHP_EXACTNESS
KERNEL_COMPUTATION
IMAGE_COMPUTATION
COKERNEL_COMPUTATION
```

などである。

一方 `InferenceRule` は、
premises から conclusion を導く際に使用した
具体的な数学的推論規則を表す。

例えば、

```text
zero relation implies order bound
```

という推論規則は、

```text
mα = 0
↓
ord(α) divides m
```

という数学的推論を表す。

したがって、

```text
ProofRule
= ProofStep の大分類

InferenceRule
= premises から conclusion を導く具体的規則
```

とする。

---

## InferenceRule の設計

Phase 5-14 では、
`InferenceRule` を最小構造として導入する。

保持する情報は、

```text
name
description
```

とする。

例えば、

```python
InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
  ),
  description=(
    "If m alpha = 0, "
    "the order of alpha divides m."
  ),
)
```

のように表現する。

`name` は Proof trace に表示する短い名称とする。

`description` は、
推論規則の数学的意味を説明する補足情報とする。

Phase 5-14 では、
`description` は保持するだけであり、
Proof formatter にはまだ表示しない。

---

## ProofStep と InferenceRule の接続

`ProofStep` に、

```text
inference_rule
```

を追加する。

型は、

```text
InferenceRule | None
```

とする。

これにより、

```text
premises
↓
InferenceRule
↓
conclusion
```

という構造を ProofStep 内に保持できる。

例えば、

```text
1. 2η_3 = 0
   [relation]

2. η_3 has order dividing 2
   [relation]
   Inference rule: zero relation implies order bound
   Premises: 1
```

という Proof trace を構築できる。

内部構造としては、

```text
ProofStep
├── conclusion
├── premises
├── rule
├── note
└── inference_rule
```

となる。

---

## inference_rule は optional とする

既存の ProofStep には
InferenceRule を持たないものが多数存在する。

例えば、

```text
kernel computation
image computation
cokernel computation
given
```

などについては、
Phase 5-14 で新しい InferenceRule を強制しない。

また既存の relation inference API との
後方互換性も維持する。

したがって、

```text
inference_rule = None
```

を許可する。

従来の、

```python
relation_inference_proof(
  relation,
  conclusion,
)
```

もそのまま動作する。

必要な場合のみ、

```python
relation_inference_proof(
  relation,
  conclusion,
  inference_rule=rule,
)
```

とする。

---

## inference_rule の検証

relation inference API に渡される
`inference_rule` は、

```text
InferenceRule
```

または、

```text
None
```

に限定する。

文字列などを直接渡すことは許可しない。

例えば、

```python
inference_rule=(
  "zero relation implies order bound"
)
```

のような入力は使用しない。

必ず、

```python
InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
  ),
)
```

として構造化する。

これにより将来的に、

```text
rule name
description
premise pattern
conclusion construction
source
```

などへ拡張できる。

---

## relation inference との接続

Phase 5-13 で一般化した、

```text
relation_inference_proof_step()
relation_inference_proof()
```

に、

```text
inference_rule
```

引数を追加する。

例えば、

```python
rule = InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
  ),
)

proof = relation_inference_proof(
  relation,
  conclusion,
  inference_rule=rule,
)
```

とする。

生成された inference ProofStep は、

```text
rule = ProofRule.RELATION
```

を維持しつつ、

```text
inference_rule = rule
```

として具体的な推論規則も保持する。

このため、

```text
ProofRule.RELATION
```

を細かな数学的規則ごとに増やす必要はない。

---

## formatter との接続

formatter に、

```text
format_inference_rule()
```

を追加する。

Phase 5-14 では、
InferenceRule の `name` を表示する。

例えば、

```text
Inference rule: zero relation implies order bound
```

と表示する。

Proof trace 全体では、

```text
1. 2η_3 = 0
   [relation]
   Source: Toda — H. Toda, Composition Methods in Homotopy Groups of Spheres, 1962
   Relation note: example zero relation

2. η_3 has order dividing 2
   [relation]
   Inference rule: zero relation implies order bound
   Premises: 1
   Note: derived from the zero relation
```

のようになる。

これにより、

```text
使用した数学的事実
使用した推論規則
依存した ProofStep
推論時の補足
```

をそれぞれ区別して表示できる。

---

## metadata の責務分離

Phase 5-14 時点では、
proof trace 上の情報を次のように区別する。

```text
LiteratureReference
= Relation の文献出典

Relation.note
= Relation 自体の数学的補足

ProofStep.note
= その ProofStep における補足

ProofRule
= ProofStep の処理の大分類

InferenceRule
= premises から conclusion を導く具体的な数学的規則
```

これらを統合しない。

例えば、

```text
Source
```

と、

```text
Inference rule
```

は異なる。

Source は、

```text
その数学的事実をどこから得たか
```

を表す。

InferenceRule は、

```text
その事実からどの規則を使って
新しい結論を得たか
```

を表す。

---

## Phase 5-14 時点の inference pipeline

現在の relation inference は、

```text
LiteratureReference
        ↓
Relation
        ↓
relation_proof_step
        ↓
ProofStep
        │
        ├──────────────┐
        │              │
        ↓              ↓
    premises      InferenceRule
        │              │
        └──────┬───────┘
               ↓
       inference ProofStep
               ↓
             Proof
               ↓
           formatter
```

という構造を持つ。

これにより、

```text
何を使ったか
```

だけでなく、

```text
どの推論規則を使ったか
```

も Proof trace に保持できるようになった。

---

## Phase 5-14 ではまだ行わないこと

Phase 5-14 の `InferenceRule` は、
推論規則の metadata を構造化する段階とする。

まだ、

```text
premise pattern の定義
pattern matching
rule applicability 判定
conclusion の自動生成
InferenceRule の apply()
InferenceRule repository
自動 relation 検索
自動 proof construction
```

は行わない。

したがって現段階では、

```text
InferenceRule
```

を指定しても、
その rule が本当に premises に適用可能かを
機械的に判定するわけではない。

conclusion も引き続き明示的に指定する。

自動適用機構は後続フェーズで導入する。

---

## Phase 5-14 時点の設計原則

1. `ProofRule` と `InferenceRule` を区別する。
2. `ProofRule` は ProofStep の大分類とする。
3. `InferenceRule` は具体的な数学的推論規則とする。
4. `InferenceRule` は `name` と `description` を持つ。
5. `ProofStep` は optional な `inference_rule` を保持できる。
6. inference_rule を持たない既存 ProofStep との後方互換性を維持する。
7. relation inference は InferenceRule を明示的に受け取れる。
8. 不正な inference_rule 型は拒否する。
9. formatter は InferenceRule の name を表示する。
10. LiteratureReference と InferenceRule を混同しない。
11. Relation.note と InferenceRule を混同しない。
12. ProofStep.note と InferenceRule を混同しない。
13. InferenceRule の pattern matching はまだ実装しない。
14. InferenceRule の自動適用はまだ実装しない。
15. conclusion は引き続き明示的に構築する。
16. algebra 層には InferenceRule の概念を持ち込まない。


# InferenceRule の premise pattern

## Phase 5-15：InferenceRule に premise pattern を持たせるための最小基盤

Phase 5-14 では、
具体的な数学的推論規則を表す

```text
InferenceRule
```

を導入した。

これにより、

```text
premises
↓
InferenceRule
↓
conclusion
```

という推論構造を ProofStep に保持できるようになった。

ただし Phase 5-14 の `InferenceRule` が持つ情報は、

```text
name
description
```

だけであり、

```text
その inference rule が
どのような premise を必要とするか
```

はまだ構造化されていなかった。

Phase 5-15 では、
InferenceRule が要求する premise の種類を記述するための
最小構造として、

```text
PremisePattern
```

を導入する。

---

## PremisePattern の設計

`PremisePattern` は、

```text
InferenceRule が要求する
1つの premise の条件
```

を表す。

Phase 5-15 では最小構造として、

```text
proof_rule
statement_type
relation_type
```

を保持する。

定義は、

```python
@dataclass(frozen=True)
class PremisePattern:
  proof_rule: ProofRule | None = None
  statement_type: type | None = None
  relation_type: RelationType | None = None
```

とする。

各項目を optional とすることで、
必要な条件だけを指定できる。

---

## proof_rule

`proof_rule` は、
premise として要求する ProofStep の
大分類を表す。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
)
```

は、

```text
ProofRule.RELATION
```

を持つ ProofStep を要求する pattern を表す。

将来的には、

```text
ProofRule.GIVEN
ProofRule.EXACTNESS
ProofRule.EHP_EXACTNESS
ProofRule.KERNEL_COMPUTATION
ProofRule.IMAGE_COMPUTATION
ProofRule.COKERNEL_COMPUTATION
```

なども pattern 条件として利用できる。

Phase 5-15 では、
この条件を保持するだけであり、
実際の ProofStep に対する一致判定はまだ行わない。

---

## statement_type

`statement_type` は、
ProofStep の、

```text
conclusion
```

に要求する型を表す。

例えば、

```python
PremisePattern(
  statement_type=Relation,
)
```

は、

```text
conclusion が Relation
```

である ProofStep を要求する pattern を表す。

将来的には、

```text
KernelStatement
ImageStatement
CokernelStatement
ExactnessStatement
```

なども同じ仕組みで指定できる。

これにより、

```text
ProofRule
```

だけでなく、

```text
どの種類の Statement を
conclusion とする ProofStep か
```

という条件を rule 側に記述できる。

---

## relation_type

`statement_type` が `Relation` である場合、
さらに Relation の種類を限定できるように、

```text
relation_type
```

を持たせる。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

は、

```text
ProofRule.RELATION
+
conclusion が Relation
+
RelationType.ZERO
```

という premise を要求する pattern を表す。

これにより、

```text
ZERO relation
ORDER relation
EQUALITY relation
```

を rule の要求条件として区別できる。

---

## InferenceRule.premise_patterns

`InferenceRule` に、

```text
premise_patterns
```

を追加する。

型は、

```text
tuple[PremisePattern, ...]
```

とする。

既存の InferenceRule との後方互換性を維持するため、

```text
()
```

をデフォルト値とする。

したがって従来の、

```python
InferenceRule(
  name="example rule",
)
```

もそのまま利用できる。

一方、
premise pattern を持つ rule は、

```python
InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
  ),
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.RELATION,
      statement_type=Relation,
      relation_type=RelationType.ZERO,
    ),
  ),
)
```

のように表現できる。

この rule は構造上、

```text
ZERO relation を1つ premise として要求する
```

という情報を保持する。

---

## 複数 premise pattern

`premise_patterns` は tuple とするため、
複数の premise を要求する rule も表現できる。

例えば、

```python
InferenceRule(
  name="combined rule",
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.RELATION,
      statement_type=Relation,
      relation_type=RelationType.ZERO,
    ),
    PremisePattern(
      proof_rule=ProofRule.GIVEN,
    ),
  ),
)
```

のように、

```text
ZERO relation
+
GIVEN step
```

を必要とする rule を記述できる。

Phase 5-15 では、
tuple の順序を premise pattern の記述順として保持する。

ただし、

```text
実際の premises と
premise_patterns の順序を
どのように対応させるか
```

についての意味論はまだ確定しない。

実際の matching を実装する段階で整理する。

---

## PremisePattern を独立型とする理由

InferenceRule に直接、

```text
required_proof_rules
required_statement_types
required_relation_types
```

などを個別に持たせるのではなく、

```text
1つの premise に対する条件
```

を `PremisePattern` としてまとめる。

例えば、

```text
ProofRule.RELATION
+
Relation
+
RelationType.ZERO
```

は、
すべて同じ1つの premise に対する条件である。

これらを別々の tuple として保持すると、

```text
どの proof_rule と
どの statement_type と
どの relation_type が
同じ premise を表しているか
```

が不明確になる。

そのため、

```text
PremisePattern
= 1つの premise に対する条件
```

として独立したデータ構造を採用する。

---

## optional field の意味

Phase 5-15 では、
各条件を、

```text
None
```

にできる。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
)
```

は、

```text
ProofRule.RELATION であることだけを要求する
```

という意味になる。

また、

```python
PremisePattern(
  statement_type=ExactnessStatement,
)
```

のように、

```text
ProofRule は問わず
conclusion の型だけを要求する
```

という pattern も表現できる。

この設計によって、
pattern の条件を最初から過度に固定せず、
必要な条件だけを段階的に追加できる。

---

## Phase 5-15 では matching を行わない

Phase 5-15 の目的は、

```text
InferenceRule が
どのような premise を必要とするかを
データとして表現できる
```

ところまでとする。

まだ、

```text
PremisePattern
+
ProofStep
↓
match / no match
```

という判定は行わない。

したがって、

```python
rule = InferenceRule(
  name="example",
  premise_patterns=(pattern,),
)
```

を作成しても、

```text
実際に渡された ProofStep が
pattern に一致しているか
```

は検証されない。

既存の、

```text
relation_inference_proof_step()
relation_inference_proof()
```

の挙動にも変更を加えない。

---

## Expression pattern はまだ導入しない

Phase 5-15 では、

```text
ProofRule
Statement type
RelationType
```

までを premise pattern の条件とする。

例えば、

```text
mα = 0
```

という relation に対して、

```text
lhs が Multiple
rhs が Zero
Multiple.coefficient を m として束縛
Multiple.expression を α として束縛
```

といった Expression 内部の pattern matching はまだ行わない。

したがって、

```python
PremisePattern(
  relation_type=RelationType.ZERO,
)
```

によって、

```text
ZERO relation
```

であることまでは表現できるが、

```text
mα = 0
```

という具体的な式構造までは記述しない。

Expression pattern は、
ProofStep レベルの matching が安定した後の
後続フェーズで導入する。

---

## Pattern variable はまだ導入しない

将来的には、

```text
m
α
β
n
```

などを pattern variable として使い、

```text
mα = 0
↓
ord(α) divides m
```

のような rule を
一般化する必要がある。

しかし Phase 5-15 では、

```text
変数束縛
unification
substitution
```

は導入しない。

まず、

```text
どの種類の ProofStep を premise とするか
```

という粗い構造を記述できるようにする。

---

## Repository との接続はまだ行わない

`PremisePattern` を導入しても、

```text
RelationRepository
```

から pattern に一致する Relation を
自動検索することはまだ行わない。

Phase 5-15 時点では、

```text
RelationRepository
= Relation の保存・基本検索

InferenceRule
= 推論規則と premise 要求の記述
```

として責務を分離する。

将来的には、

```text
InferenceRule
↓
PremisePattern
↓
RelationRepository / existing ProofSteps
↓
candidate premises
```

という接続を検討する。

---

## Phase 5-15 時点の inference rule 構造

Phase 5-15 により、

```text
InferenceRule
├── name
├── description
└── premise_patterns
      │
      ├── PremisePattern
      │     ├── proof_rule
      │     ├── statement_type
      │     └── relation_type
      │
      └── PremisePattern
            └── ...
```

という構造を持つようになった。

Phase 5-14 では、

```text
どの規則を使ったか
```

を記録できるようになった。

Phase 5-15 ではさらに、

```text
その規則が
どのような premise を期待するか
```

を記述できるようになった。

ただしこれはまだ、

```text
rule specification
```

の段階であり、

```text
rule execution
```

ではない。

---

## Phase 5-15 時点の推論基盤

現在の inference 層は、

```text
Expression
↓
Relation
↓
RelationRepository
↓
ProofStep
↓
premises
        +
InferenceRule
        │
        └── premise_patterns
↓
inference ProofStep
↓
Proof
↓
formatter
```

という構造を持つ。

InferenceRule は、

```text
具体的な数学的規則
```

だけでなく、

```text
その規則が要求する premise の種類
```

も保持できるようになった。

---

## Phase 5-15 ではまだ行わないこと

Phase 5-15 では、以下は実装しない。

```text
PremisePattern と ProofStep の matching
InferenceRule applicability 判定
Expression 内部の pattern matching
pattern variable
変数束縛
unification
substitution
conclusion の自動生成
InferenceRule.apply()
InferenceRule repository
RelationRepository からの自動 relation 選択
既存 ProofStep からの自動 premise 選択
proof の自動構築
Proof DAG の自動構築
```

これらは、
premise pattern の最小モデルを基礎として
後続フェーズで段階的に追加する。

---

## Phase 5-15 時点の設計原則

1. `InferenceRule` は要求する premise の pattern を保持できる。
2. 1つの premise に対する条件は `PremisePattern` としてまとめる。
3. `PremisePattern` は `proof_rule` を条件にできる。
4. `PremisePattern` は conclusion の `statement_type` を条件にできる。
5. Relation については `relation_type` も条件にできる。
6. 各 pattern 条件は optional とし、必要な条件だけを指定できる。
7. `InferenceRule.premise_patterns` は tuple とする。
8. premise pattern を持たない既存 InferenceRule との後方互換性を維持する。
9. 複数 premise を要求する rule を表現可能にする。
10. Phase 5-15 では pattern の保持だけを行う。
11. PremisePattern と ProofStep の一致判定はまだ行わない。
12. Expression 内部の pattern matching はまだ行わない。
13. pattern variable や変数束縛はまだ導入しない。
14. conclusion の自動生成はまだ行わない。
15. RelationRepository との自動接続はまだ行わない。
16. algebra 層には premise pattern の概念を持ち込まない。
17. InferenceRule の specification と rule の実行機構を分離する。
18. 次段階では ProofStep が PremisePattern に一致するかを判定する最小 matching 基盤を検討する。


# PremisePattern と ProofStep の matching

## Phase 5-16：PremisePattern と ProofStep の最小 matching 基盤

Phase 5-15 では、
`InferenceRule` が要求する premise の条件を表すため、

```text
PremisePattern
```

を導入した。

これにより、

```text
proof_rule
statement_type
relation_type
```

を用いて、

```text
その inference rule が
どのような ProofStep を premise として期待するか
```

を構造化して記述できるようになった。

ただし Phase 5-15 では、
PremisePattern は rule specification を保持するだけであり、

```text
PremisePattern
+
ProofStep
↓
match / no match
```

という実際の一致判定は行っていなかった。

Phase 5-16 では、
この最小 matching 基盤として、

```text
matches_premise_pattern()
```

を導入する。

---

## matches_premise_pattern() の設計

`matches_premise_pattern()` は、

```text
PremisePattern
ProofStep
```

を受け取り、

```text
True
False
```

を返す。

基本形は、

```python
matches_premise_pattern(
  pattern,
  step,
)
```

とする。

この関数の責務は、

```text
1つの PremisePattern
```

と、

```text
1つの ProofStep
```

の一致判定だけとする。

Phase 5-16 ではまだ、

```text
InferenceRule 全体の applicability
複数 premise の割り当て
premise の自動検索
```

などは扱わない。

---

## 空の PremisePattern

すべての条件が `None` である、

```python
PremisePattern()
```

は、
任意の ProofStep に一致するものとする。

つまり、

```text
proof_rule = None
statement_type = None
relation_type = None
```

は、

```text
その条件について制約を設けない
```

という意味になる。

例えば、

```python
pattern = PremisePattern()

step = ProofStep(
  conclusion="given fact",
  premises=(),
  rule=ProofRule.GIVEN,
)
```

に対して、

```python
matches_premise_pattern(
  pattern,
  step,
)
```

は、

```text
True
```

となる。

この意味論により、
PremisePattern の optional field が、

```text
未指定
=
wildcard
```

として機能する。

---

## proof_rule の matching

`PremisePattern.proof_rule` が指定されている場合、

```text
step.rule
```

との一致を要求する。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.GIVEN,
)
```

は、

```text
ProofRule.GIVEN
```

を持つ ProofStep に一致する。

一方、

```text
ProofRule.RELATION
```

など異なる rule を持つ ProofStep には一致しない。

判定は、

```text
step.rule == pattern.proof_rule
```

を基準とする。

`proof_rule` が `None` の場合は、
ProofStep の rule を条件にしない。

---

## statement_type の matching

`PremisePattern.statement_type` が指定されている場合、

```text
step.conclusion
```

がその型であることを要求する。

例えば、

```python
PremisePattern(
  statement_type=Relation,
)
```

は、

```text
conclusion が Relation
```

である ProofStep に一致する。

判定には、

```python
isinstance(
  step.conclusion,
  pattern.statement_type,
)
```

を使用する。

したがって、
単純な型の完全一致ではなく、
Python の `isinstance()` の意味論に従う。

`statement_type` が `None` の場合は、
conclusion の型を条件にしない。

---

## relation_type の matching

`PremisePattern.relation_type` が指定されている場合、

```text
step.conclusion
```

が `Relation` であり、
さらに、

```text
step.conclusion.relation_type
```

が指定された RelationType と一致することを要求する。

例えば、

```python
PremisePattern(
  relation_type=RelationType.ZERO,
)
```

は、

```text
conclusion が Relation
+
RelationType.ZERO
```

である ProofStep に一致する。

RelationType が異なる場合は一致しない。

また、

```text
relation_type
```

が指定されていても、

```text
step.conclusion
```

が Relation でなければ、
一致しない。

つまり、

```text
relation_type を指定する
```

こと自体が暗黙に、

```text
conclusion は Relation である
```

という条件を含む。

---

## relation_type と statement_type の関係

例えば、

```python
PremisePattern(
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

では、

```text
conclusion が Relation
```

という条件と、

```text
その Relation が ZERO type
```

という条件の両方を検証する。

一方、

```python
PremisePattern(
  relation_type=RelationType.ZERO,
)
```

だけでも、
relation_type の判定時に conclusion が Relation であることを確認する。

したがって、

```text
statement_type=Relation
```

の明示は必須ではない。

ただし InferenceRule の specification を
人間が読む際の明確さを重視する場合には、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

のように、
要求条件を明示的にすべて記述できる。

---

## 複数条件は AND として扱う

PremisePattern に複数の条件が指定されている場合、
すべての条件を満たしたときだけ一致する。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

は、

```text
step.rule == ProofRule.RELATION
AND
step.conclusion is Relation
AND
step.conclusion.relation_type == RelationType.ZERO
```

を要求する。

このうち1つでも満たさない場合は、

```text
False
```

を返す。

したがって PremisePattern は、

```text
指定された条件の conjunction
```

として解釈する。

---

## matching の判定順序

Phase 5-16 の実装では、
概念的に次の順序で条件を確認する。

```text
proof_rule
↓
statement_type
↓
relation_type
```

条件に一致しないことが判明した時点で、

```text
False
```

を返す。

すべての指定条件を通過した場合に、

```text
True
```

を返す。

ただしこの順序自体を
数学的意味として外部 API に依存させない。

matching の意味はあくまで、

```text
指定されたすべての条件を満たすか
```

である。

---

## 型検証

`matches_premise_pattern()` は、
入力型を明示的に検証する。

第1引数は、

```text
PremisePattern
```

でなければならない。

それ以外を渡した場合は、

```text
TypeError
```

とする。

同様に第2引数は、

```text
ProofStep
```

でなければならない。

それ以外を渡した場合も、

```text
TypeError
```

とする。

これにより、

```text
match しない
```

という数学的・論理的な結果と、

```text
API の利用方法自体が不正
```

というプログラム上のエラーを区別する。

---

## False と TypeError の区別

Phase 5-16 では、

```text
正しい型の pattern と step を比較した結果、
条件が一致しない
```

場合は、

```text
False
```

とする。

一方、

```text
pattern 自体が PremisePattern ではない
step 自体が ProofStep ではない
```

場合は、

```text
TypeError
```

とする。

例えば、

```python
matches_premise_pattern(
  PremisePattern(
    proof_rule=ProofRule.RELATION,
  ),
  given_step,
)
```

で `given_step.rule` が `ProofRule.GIVEN` なら、

```text
False
```

となる。

一方、

```python
matches_premise_pattern(
  "invalid",
  given_step,
)
```

は、

```text
TypeError
```

となる。

この区別により、
matching failure と API misuse を明確に分離する。

---

## InferenceRule との位置づけ

Phase 5-16 で追加するのは、

```text
PremisePattern
+
ProofStep
↓
match / no match
```

という1対1の判定だけである。

まだ、

```text
InferenceRule.premise_patterns
+
複数 ProofStep
↓
rule applicable / not applicable
```

という判定は行わない。

例えば、

```python
rule = InferenceRule(
  name="combined rule",
  premise_patterns=(
    pattern1,
    pattern2,
  ),
)
```

があっても、

```text
2つの pattern に対して
どの ProofStep を対応させるか
```

を自動判定する機能は Phase 5-16 には含めない。

Phase 5-16 で得られるのは、
その後の applicability 判定を実装するための
最小 primitive である。

---

## premise_patterns の順序問題はまだ扱わない

Phase 5-15 では、

```text
InferenceRule.premise_patterns
```

を tuple として保持した。

Phase 5-16 では、
1つの PremisePattern と
1つの ProofStep の matching のみを扱うため、

```text
pattern1 ↔ step1
pattern2 ↔ step2
```

のように、
複数 pattern と複数 step を
位置対応させるかどうかはまだ決めない。

今後 applicability 判定を導入する段階で、

```text
順序付き matching
順序なし matching
重複利用の可否
1つの step が複数 pattern を満たせるか
```

などを整理する。

---

## Expression 内部の matching はまだ行わない

Phase 5-16 で判定する条件は、

```text
proof_rule
statement_type
relation_type
```

だけである。

例えば、

```text
2η_3 = 0
```

と、

```text
3ν_4 = 0
```

は、
どちらも、

```text
ProofRule.RELATION
Relation
RelationType.ZERO
```

であれば、
同じ PremisePattern に一致し得る。

まだ、

```text
lhs が Multiple か
rhs が Zero か
coefficient が何か
expression が何か
```

などは判定しない。

したがって、

```text
mα = 0
```

という数学的 pattern そのものを
認識できる段階ではない。

---

## pattern variable と binding はまだ行わない

Phase 5-16 では、

```text
m
α
β
n
```

などを pattern variable として扱わない。

したがって、

```text
mα = 0
↓
ord(α) divides m
```

という rule について、

```text
m = 2
α = η_3
```

のような binding を生成することはできない。

Phase 5-16 の matching は、

```text
ProofStep レベルの粗い分類条件
```

だけを扱う。

Expression-level matching、
変数束縛、
unification、
substitution は後続フェーズへ分離する。

---

## RelationRepository との接続はまだ行わない

Phase 5-16 では、

```text
RelationRepository
```

から PremisePattern に一致する Relation を
自動取得する機能は追加しない。

現在の責務は、

```text
RelationRepository
= Relation の保存・基本検索

PremisePattern
= premise requirement の specification

matches_premise_pattern()
= ProofStep との1対1 matching
```

とする。

将来的には、

```text
InferenceRule
↓
PremisePattern
↓
existing ProofSteps / RelationRepository
↓
candidate premises
```

という自動選択機構を構築できる。

---

## Phase 5-16 時点の matching pipeline

Phase 5-16 により、

```text
InferenceRule
       │
       ↓
PremisePattern
       │
       │
       ├──────────────┐
       │              │
       ↓              ↓
pattern condition   ProofStep
       │              │
       └──────┬───────┘
              ↓
matches_premise_pattern()
              ↓
         True / False
```

という最小 matching 経路が成立した。

Phase 5-15 まででは、

```text
rule が何を要求するか
```

を記述できるだけだった。

Phase 5-16 ではさらに、

```text
実際の ProofStep が
その要求を満たしているか
```

を機械的に判定できるようになった。

---

## rule specification と matching の分離

現在の責務は、

```text
PremisePattern
= 条件のデータ表現

matches_premise_pattern()
= 条件と ProofStep の照合
```

として分離する。

PremisePattern 自体に、

```text
matches()
```

などの振る舞いを持たせず、
matching は独立した関数として実装する。

これにより、
pattern のデータモデルと
matching algorithm を分離した状態を維持する。

今後 Expression pattern や binding を導入した際にも、
PremisePattern の役割と
matching engine の役割を整理しやすくする。

---

## Phase 5-16 ではまだ行わないこと

Phase 5-16 では、以下は実装しない。

```text
InferenceRule 全体の applicability 判定
複数 PremisePattern と複数 ProofStep の対応付け
premise の順序・順序なし matching の決定
既存 ProofStep からの自動 premise 選択
RelationRepository からの自動 relation 選択
Expression 内部の pattern matching
Multiple / Zero 等の構造 pattern
pattern variable
変数束縛
binding environment
unification
substitution
conclusion の自動生成
InferenceRule.apply()
InferenceRule repository
proof の自動構築
Proof DAG の自動構築
```

まず、

```text
1 pattern
+
1 ProofStep
↓
match / no match
```

という最小 primitive を安定させる。

---

## Phase 5-16 時点の設計原則

1. `PremisePattern` と `ProofStep` の一致を機械的に判定できる。
2. 一致判定は `matches_premise_pattern()` に分離する。
3. `PremisePattern()` の未指定条件は wildcard として扱う。
4. `proof_rule` が指定されている場合は `ProofStep.rule` と一致する必要がある。
5. `statement_type` が指定されている場合は `isinstance()` によって conclusion の型を判定する。
6. `relation_type` が指定されている場合は conclusion が Relation でなければならない。
7. `relation_type` が指定されている場合は RelationType も一致する必要がある。
8. 複数の指定条件は AND 条件として扱う。
9. 条件不一致は `False` とする。
10. pattern または step の入力型が不正な場合は `TypeError` とする。
11. matching failure と API misuse を区別する。
12. PremisePattern は specification、matching 関数は照合処理として責務を分離する。
13. Phase 5-16 では1つの pattern と1つの ProofStep の matching のみを扱う。
14. InferenceRule 全体の applicability 判定はまだ行わない。
15. 複数 pattern と複数 premise の割り当てはまだ行わない。
16. Expression 内部の pattern matching はまだ行わない。
17. pattern variable や変数束縛はまだ導入しない。
18. conclusion の自動生成はまだ行わない。
19. RelationRepository からの自動 premise 選択はまだ行わない。
20. algebra 層には matching の概念を持ち込まない。
21. 次段階では `InferenceRule.premise_patterns` と実際の複数 ProofStep を用いた applicability 判定を検討する。


# InferenceRule 全体の premise matching

## Phase 5-17：InferenceRule.premise_patterns と複数 ProofStep の適合判定

Phase 5-16 では、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

という、
1つの premise pattern と1つの ProofStep の
最小 matching 基盤を導入した。

これにより、

```text
proof_rule
statement_type
relation_type
```

という ProofStep レベルの条件について、
実際の ProofStep が pattern を満たすかを
機械的に判定できるようになった。

Phase 5-17 では、
この個別 matching を組み合わせ、

```text
InferenceRule.premise_patterns
+
複数の ProofStep
↓
rule 全体として match / no match
```

を判定する最小基盤を導入する。

---

## matches_inference_rule() の設計

InferenceRule 全体の premise matching を行うため、

```text
matches_inference_rule()
```

を導入する。

基本形は、

```python
matches_inference_rule(
  inference_rule,
  steps,
)
```

とする。

入力は、

```text
InferenceRule
ProofStep または ProofStep の tuple / list
```

であり、

```text
True
False
```

を返す。

この関数は、

```text
InferenceRule.premise_patterns
```

と、

```text
実際に与えられた ProofStep 列
```

を比較する。

---

## ProofStep 入力の正規化

`steps` には、

```text
単一の ProofStep
```

または、

```text
tuple / list of ProofStep
```

を受け取れる。

内部では既存の、

```text
_normalize_proof_steps()
```

を利用し、

```text
tuple[ProofStep, ...]
```

へ統一する。

これにより、

```python
matches_inference_rule(
  rule,
  step,
)
```

と、

```python
matches_inference_rule(
  rule,
  (step,),
)
```

および、

```python
matches_inference_rule(
  rule,
  [step],
)
```

を同じ意味で扱える。

新しい normalize mechanism は追加せず、
Phase 5-13 で導入した既存 helper を再利用する。

---

## premise pattern と ProofStep は位置対応とする

Phase 5-17 では、

```text
InferenceRule.premise_patterns
```

と、

```text
steps
```

を順序付きで対応させる。

つまり、

```text
premise_patterns[0] ↔ steps[0]
premise_patterns[1] ↔ steps[1]
premise_patterns[2] ↔ steps[2]
...
```

とする。

例えば、

```text
patterns:

1. RELATION
2. GIVEN
```

に対して、

```text
steps:

1. RELATION
2. GIVEN
```

なら match する。

一方、

```text
steps:

1. GIVEN
2. RELATION
```

では match しない。

したがって Phase 5-17 では、
premise pattern の tuple 順序に意味を持たせる。

---

## 順序付き matching を採用する理由

一般には、

```text
複数 pattern
+
複数 ProofStep
```

について、
順序を無視した matching を考えることもできる。

しかし順序なし matching を導入すると、

```text
どの step をどの pattern に割り当てるか
1つの step を複数 pattern に利用できるか
複数の割り当て候補をどう扱うか
```

などの問題が生じる。

Phase 5-17 では、
InferenceRule matching の最小基盤を構築することを優先し、

```text
pattern と step は位置対応
```

という単純で明確な意味論を採用する。

より柔軟な premise search / assignment は、
自動 inference を実装する後続フェーズで検討する。

---

## premise 数は完全一致を要求する

Phase 5-17 では、

```text
len(inference_rule.premise_patterns)
```

と、

```text
len(steps)
```

が一致することを要求する。

数が異なる場合は、

```text
False
```

を返す。

したがって、

```text
必要な premise より少ない
```

場合だけでなく、

```text
余分な ProofStep が存在する
```

場合も match しない。

例えば、

```text
pattern 数 = 2
step 数 = 1
```

は `False`。

同様に、

```text
pattern 数 = 1
step 数 = 2
```

も `False` とする。

この段階では、

```text
rule が要求する premises
```

と、

```text
rule 適用に渡された ProofSteps
```

が完全に対応することを要求する。

---

## 各 premise の判定

pattern 数と step 数が一致した場合、
対応する各組について、

```text
matches_premise_pattern()
```

を利用する。

概念的には、

```text
pattern 1 ↔ step 1
pattern 2 ↔ step 2
...
```

について、

```text
すべて match
```

した場合のみ、

```text
True
```

を返す。

1組でも match しなければ、

```text
False
```

となる。

実装上は、

```python
all(
  matches_premise_pattern(
    pattern,
    step,
  )
  for pattern, step in zip(
    patterns,
    normalized_steps,
  )
)
```

という構造になる。

したがって Phase 5-16 の
個別 matching logic を重複して実装しない。

---

## 空の premise_patterns

InferenceRule の、

```text
premise_patterns = ()
```

は、

```text
premise を必要としない rule
```

として解釈する。

したがって、

```text
premise_patterns = ()
steps = ()
```

なら、

```text
True
```

となる。

一方、

```text
premise_patterns = ()
steps = (some_step,)
```

なら、

```text
False
```

となる。

これは、

```text
pattern 数と step 数の完全一致
```

という一般ルールの自然な結果である。

---

## 不正な inference_rule

`matches_inference_rule()` の第1引数は、

```text
InferenceRule
```

でなければならない。

文字列などの不正な型を渡した場合は、

```text
TypeError
```

とする。

これは、

```text
rule が premises に適合しない
```

という論理的結果と、

```text
API に渡した値そのものが不正
```

というプログラム上のエラーを区別するためである。

---

## 不正な steps

`steps` は、

```text
ProofStep
```

または、

```text
tuple / list of ProofStep
```

でなければならない。

不正な型を直接渡した場合や、

```text
tuple / list
```

内部に ProofStep 以外の値が含まれている場合は、

```text
TypeError
```

とする。

この検証には既存の、

```text
_normalize_proof_steps()
```

を利用する。

---

## matches_premise_pattern() との責務分離

Phase 5-17 時点では、

```text
matches_premise_pattern()
```

と、

```text
matches_inference_rule()
```

を明確に分離する。

```text
matches_premise_pattern()
= 1 pattern と 1 ProofStep の matching
```

であり、

```text
matches_inference_rule()
= InferenceRule 全体と ProofStep 列の matching
```

である。

後者は前者を組み合わせて使用する。

これにより matching logic の重複を避け、
各層の責務を明確にする。

---

## matching と applicability の境界

Phase 5-17 の `matches_inference_rule()` は、

```text
指定された ProofStep 列が
InferenceRule.premise_patterns に一致するか
```

を判定する。

一方、

```text
手元に存在する多数の ProofStep の中から
rule を適用できる組を自動的に探す
```

ことはまだ行わない。

したがって現段階では、

```text
matching
```

と、

```text
candidate premise search
```

を別の責務とする。

例えば、

```text
existing steps
=
step A
step B
step C
step D
```

から、

```text
rule の pattern に合う
step B と step D を自動選択する
```

ような処理は Phase 5-17 には含まれない。

---

## Expression pattern はまだ扱わない

InferenceRule 全体を matching できるようになったが、
個々の PremisePattern が判定できる条件は引き続き、

```text
proof_rule
statement_type
relation_type
```

だけである。

例えば、

```text
2η_3 = 0
```

という Relation と、

```text
3ν_4 = 0
```

という Relation は、
どちらも、

```text
ProofRule.RELATION
Relation
RelationType.ZERO
```

という pattern に一致し得る。

まだ、

```text
mα = 0
```

という Expression 内部の一般 pattern を認識したり、

```text
m = 2
α = η_3
```

のような変数束縛を行うことはできない。

---

## Phase 5-17 時点の matching pipeline

現在、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

という個別 matching の上に、

```text
InferenceRule
│
└── premise_patterns
      │
      ├── pattern 1
      ├── pattern 2
      └── ...
             +
      ProofStep sequence
             ↓
matches_inference_rule()
             ↓
        True / False
```

という rule-level matching が成立した。

これにより、

```text
rule requirement の記述
```

だけでなく、

```text
実際に与えられた premises が
その rule requirement 全体を満たすか
```

まで機械的に判定できるようになった。

---

## Phase 5-17 ではまだ行わないこと

Phase 5-17 では以下は実装しない。

```text
順序なし premise matching
pattern と step の組合せ探索
candidate ProofStep の自動検索
1つの step の複数 pattern への割り当て
RelationRepository からの自動 relation 選択
InferenceRule の自動選択
Expression-level pattern matching
pattern variable
変数束縛
binding environment
unification
substitution
conclusion の自動生成
InferenceRule.apply()
proof の自動構築
Proof DAG の自動構築
```

まず、

```text
rule specification
+
明示的に与えられた premises
↓
match / no match
```

までを安定した primitive とする。

---

## Phase 5-17 時点の設計原則

1. `InferenceRule.premise_patterns` 全体と複数 ProofStep を比較できる。
2. rule-level matching は `matches_inference_rule()` に分離する。
3. 単一 ProofStep と tuple / list の両方を入力できる。
4. ProofStep 入力は既存 `_normalize_proof_steps()` で正規化する。
5. premise pattern と ProofStep は位置ごとに対応させる。
6. premise matching は順序付きとする。
7. pattern 数と step 数は完全一致を要求する。
8. premise が不足している場合は `False` とする。
9. premise が余分にある場合も `False` とする。
10. 各 pattern / step の判定には `matches_premise_pattern()` を再利用する。
11. すべての pattern / step が一致した場合のみ `True` とする。
12. 空の premise_patterns は空の steps にのみ一致する。
13. 不正な InferenceRule は `TypeError` とする。
14. 不正な ProofStep 入力は `TypeError` とする。
15. matching failure と API misuse を区別する。
16. rule matching と candidate premise search を分離する。
17. 順序なし matching はまだ導入しない。
18. Expression-level matching はまだ導入しない。
19. pattern variable や変数束縛はまだ導入しない。
20. conclusion の自動生成はまだ行わない。
21. algebra 層には inference matching の概念を持ち込まない。
22. 次段階では、既存 ProofStep 集合から InferenceRule に適合する premise 候補を探索する仕組みを検討する。


# InferenceRule に対する premise candidate search

## Phase 5-18：既存 ProofStep 集合から matching premise を探索する

Phase 5-17 では、

```text
InferenceRule.premise_patterns
+
明示的に与えられた ProofStep 列
↓
matches_inference_rule()
↓
True / False
```

という rule-level matching を導入した。

これにより、

```text
この ProofStep 列を
この InferenceRule の premises として
使用できるか
```

を機械的に判定できるようになった。

ただし Phase 5-17 では、
使用する ProofStep 自体は呼び出し側が
明示的に選択する必要があった。

Phase 5-18 では一段階進めて、

```text
InferenceRule
+
利用可能な ProofStep 集合
↓
premise_patterns に適合する ProofStep を探索
↓
matching premise sequence
```

という最小 premise search を導入する。

---

## find_matching_premises() の設計

InferenceRule が要求する premises を、
既存の ProofStep 集合から探索するため、

```text
find_matching_premises()
```

を導入する。

基本形は、

```python
find_matching_premises(
  inference_rule,
  available_steps,
)
```

とする。

入力は、

```text
InferenceRule
ProofStep または ProofStep の tuple / list
```

である。

適合する premises が見つかった場合は、

```text
tuple[ProofStep, ...]
```

を返す。

必要な premise をすべて見つけられない場合は、

```text
None
```

を返す。

これにより、

```text
match の成否だけを判定する
```

`matches_inference_rule()` と、

```text
実際に使用可能な premise を探索する
```

`find_matching_premises()` の責務を分離する。

---

## available_steps の正規化

`available_steps` は、

```text
単一 ProofStep
tuple of ProofStep
list of ProofStep
```

を受け取る。

内部では既存の、

```text
_normalize_proof_steps()
```

を利用し、

```text
tuple[ProofStep, ...]
```

へ正規化する。

したがって、

```python
find_matching_premises(
  rule,
  step,
)
```

と、

```python
find_matching_premises(
  rule,
  (step,),
)
```

および、

```python
find_matching_premises(
  rule,
  [step],
)
```

を同じ入力モデルで扱える。

不正な型が与えられた場合は、
既存の ProofStep 正規化ルールに従って
`TypeError` とする。

---

## premise pattern の順序に従った探索

Phase 5-18 では、

```text
InferenceRule.premise_patterns
```

の順序に従って premise を探索する。

例えば、

```text
pattern 1 = RELATION
pattern 2 = GIVEN
```

であり、
利用可能な step が、

```text
step A = GIVEN
step B = RELATION
```

という順序で保持されていても、

```text
pattern 1
↓
step B

pattern 2
↓
step A
```

という対応を探索できる。

したがって Phase 5-17 の、

```text
明示的な ProofStep 列に対する
position-based matching
```

とは異なり、

Phase 5-18 の premise search では、

```text
available_steps の位置
```

と、

```text
premise_patterns の位置
```

を直接対応させない。

各 pattern ごとに、
利用可能な ProofStep 全体から候補を探索する。

ただし、

```text
どの pattern を先に処理するか
```

については、
`premise_patterns` の順序を維持する。

---

## 最初に一致する ProofStep を採用する

Phase 5-18 の最小実装では、
1つの premise pattern に対して
複数の ProofStep が一致する場合、

```text
available_steps の中で
最初に一致した ProofStep
```

を採用する。

例えば、

```text
pattern = GIVEN
```

に対して、

```text
step 1 = GIVEN
step 2 = GIVEN
```

の両方が一致する場合は、

```text
step 1
```

を選択する。

現段階では、

```text
すべての候補を返す
全組合せを列挙する
最適な premise を選ぶ
backtracking する
```

といった処理は行わない。

探索結果を決定的かつ単純にするため、

```text
first match
```

を採用する。

---

## 同じ ProofStep を複数 premise に再利用しない

1つの ProofStep は、
同じ `find_matching_premises()` 呼び出し内で
複数の premise pattern に再利用しない。

例えば、

```text
pattern 1 = GIVEN
pattern 2 = GIVEN
```

という rule に対して、
利用可能な ProofStep が、

```text
step A = GIVEN
```

1つしかない場合、

```text
step A
```

を2つの pattern の両方へ割り当てることはしない。

この場合、

```text
find_matching_premises(...)
```

は、

```text
None
```

を返す。

一方、

```text
step A = GIVEN
step B = GIVEN
```

という2つの異なる ProofStep が存在すれば、

```text
(
  step A,
  step B,
)
```

を返す。

このため実装では、
既に利用した ProofStep の index を記録し、
後続 pattern の探索対象から除外する。

---

## ProofStep の識別

Phase 5-18 では、
同じ ProofStep を再利用したかどうかを、

```text
available_steps 内の index
```

によって管理する。

これは、

```text
ProofStep の structural equality
```

と、

```text
premise candidate としての個々の出現
```

を不用意に混同しないためである。

探索中に使用済みとなった
`available_steps[index]` は、
後続 pattern では利用しない。

現段階では ProofStep に
専用 ID を導入しない。

ProofStep identity や proof graph node identity が
必要になった段階で、
別途設計を検討する。

---

## pattern matching 自体は既存機能を再利用する

各 pattern と ProofStep の一致判定には、
Phase 5-16 で導入した、

```text
matches_premise_pattern()
```

をそのまま利用する。

したがって現在の premise search が利用する条件は、

```text
proof_rule
statement_type
relation_type
```

のみである。

例えば、

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

に対しては、

```text
ProofRule.RELATION
+
conclusion が Relation
+
RelationType.ZERO
```

をすべて満たす ProofStep を探索する。

Phase 5-18 では、
新しい matching semantics を
`find_matching_premises()` 内に重複実装しない。

```text
PremisePattern
↓
matches_premise_pattern()
```

を個別判定の唯一の基盤として再利用する。

---

## 一部だけ見つかった場合

複数 premise を要求する rule について、
途中まで適合する ProofStep が見つかっても、
すべての premise pattern を満たせなければ
探索全体を失敗とする。

例えば、

```text
pattern 1 = RELATION
pattern 2 = GIVEN
```

に対して、

```text
RELATION step
```

しか存在しない場合、

pattern 1 は満たせるが
pattern 2 は満たせない。

この場合、

```text
None
```

を返す。

部分的に見つかった premise tuple は返さない。

したがって返り値は、

```text
すべての premise が見つかった
→ tuple[ProofStep, ...]

少なくとも1つ不足した
→ None
```

とする。

---

## premise を必要としない rule

InferenceRule が、

```text
premise_patterns = ()
```

を持つ場合、
必要な premise は存在しない。

したがって、

```python
find_matching_premises(
  rule,
  available_steps,
)
```

は、
`available_steps` の内容に関係なく、

```text
()
```

を返す。

これは、

```text
premise を要求しない rule
```

に対して、

```text
premise search は成功しており、
選択された premise は0個である
```

ことを表す。

このため、

```text
()
```

と、

```text
None
```

は明確に区別する。

```text
()
= premise を必要とせず、探索成功

None
= 必要な premise を満たせず、探索失敗
```

とする。

---

## matches_inference_rule() との役割分担

Phase 5-18 時点では、

```text
matches_inference_rule()
```

と、

```text
find_matching_premises()
```

は異なる用途を持つ。

`matches_inference_rule()` は、

```text
InferenceRule
+
既に選択された ProofStep 列
↓
その列が rule 全体に適合するか
```

を判定する。

一方、

`find_matching_premises()` は、

```text
InferenceRule
+
利用可能な ProofStep 集合
↓
rule に利用できる ProofStep 列を探す
```

ための関数である。

概念的には、

```text
available ProofSteps
↓
find_matching_premises()
↓
selected premises
↓
matches_inference_rule()
```

という利用も可能である。

ただし Phase 5-18 では、
`find_matching_premises()` の結果に対して
自動的に inference を適用する機構はまだ導入しない。

---

## greedy search と backtracking の境界

Phase 5-18 の premise search は、
各 premise pattern について、

```text
未使用の available_steps を先頭から調べる
↓
最初に一致した step を採用する
↓
次の pattern へ進む
```

という greedy search とする。

例えば、
ある ProofStep が複数の pattern に一致し得る場合でも、
後の pattern のためにその step を残しておくべきかを考慮して
選択をやり直すことはしない。

したがって理論上、

```text
別の割り当てなら全 pattern を満たせる
```

場合でも、
最初の greedy 選択によって
`None` になる可能性は残る。

これは Phase 5-18 では意図的な制限とする。

一般的な premise assignment は、

```text
backtracking
candidate enumeration
unordered matching
constraint solving
```

などを必要とする可能性があるため、
後続フェーズとして分離する。

---

## RelationRepository とはまだ直接接続しない

Phase 5-18 で探索対象とするのは、

```text
既に ProofStep になっているオブジェクト
```

である。

したがって、

```text
RelationRepository
↓
Relation を検索
↓
relation_proof_step()
↓
premise candidate
```

という処理を
`find_matching_premises()` 自体が行うことはない。

RelationRepository からの relation 自動取得と、
ProofStep 集合内からの premise search は
別の責務として扱う。

将来的には、

```text
RelationRepository
+
existing ProofSteps
+
InferenceRule
↓
candidate facts
↓
premise search
```

という上位 inference engine を構築できるが、
Phase 5-18 ではまだ導入しない。

---

## Expression-level pattern matching はまだ行わない

Phase 5-18 の探索は、
Phase 5-16 以来の、

```text
proof_rule
statement_type
relation_type
```

だけを利用する。

例えば、

```text
RelationType.ZERO
```

を持つ relation を探すことはできる。

しかし、

```text
mα = 0
```

という Expression 内部構造を調べたり、

```text
m = 2
α = η_3
```

のように値を束縛したりすることはできない。

したがって、

```text
premise candidate search
```

と、

```text
expression pattern matching / unification
```

は引き続き分離する。

---

## Phase 5-18 時点の matching pipeline

現在の inference-rule matching 基盤は、

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

から始まり、

```text
InferenceRule.premise_patterns
+
明示的 ProofStep 列
↓
matches_inference_rule()
↓
True / False
```

まで拡張されている。

Phase 5-18 ではさらに、

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
matched ProofStep tuple
or
None
```

という探索経路が追加された。

これにより、

```text
rule requirement を記述する
↓
個別 step と比較する
↓
明示的 premise 列を検証する
↓
既存 step 集合から premise を探す
```

という段階的な matching 基盤が成立した。

---

## Phase 5-18 ではまだ行わないこと

Phase 5-18 では、
premise candidate search の最小実装だけを扱う。

まだ、

```text
すべての matching candidate の列挙
複数の premise assignment の列挙
backtracking
最適な premise assignment の選択
unordered rule matching
Expression pattern
pattern variable
variable binding
substitution
conclusion の自動生成
InferenceRule.apply()
RelationRepository からの自動 relation 検索
rule applicability の一括探索
複数 InferenceRule の自動選択
自動 inference
recursive proof construction
proof DAG construction
```

は行わない。

特に、

```text
find_matching_premises()
```

は、

```text
premise を見つける
```

ところまでを責務とし、

```text
その rule を実際に適用して
新しい ProofStep を作る
```

ところまでは担当しない。

---

## Phase 5-18 時点の設計原則

1. `find_matching_premises()` は既存 ProofStep 集合から rule の premise を探索する。
2. matching 条件自体は `matches_premise_pattern()` を再利用する。
3. `available_steps` は単一 ProofStep、tuple、list を受け付ける。
4. 入力は `_normalize_proof_steps()` で統一する。
5. premise pattern は `InferenceRule.premise_patterns` の順に処理する。
6. 各 pattern について available_steps の先頭から探索する。
7. 複数候補がある場合は最初に一致した ProofStep を採用する。
8. 同じ available step を複数 premise pattern に再利用しない。
9. 使用済み step は available_steps 内の index で管理する。
10. すべての pattern が満たされた場合のみ ProofStep tuple を返す。
11. 1つでも必要な premise が見つからなければ `None` を返す。
12. premise_patterns が空なら `()` を返す。
13. `()` は premise 不要の成功、`None` は探索失敗として区別する。
14. Phase 5-17 の `matches_inference_rule()` は明示的 premise 列の検証用として維持する。
15. Phase 5-18 の `find_matching_premises()` は available steps からの探索用とする。
16. premise search は greedy とし、backtracking はまだ行わない。
17. available_steps の順序は first-match selection に影響する。
18. RelationRepository から Relation を自動取得する処理はまだ行わない。
19. Expression 内部の pattern matching はまだ行わない。
20. pattern variable、変数束縛、substitution はまだ導入しない。
21. conclusion の自動生成はまだ行わない。
22. InferenceRule の自動適用はまだ行わない。
23. premise search と rule application の責務を分離する。
24. algebra 層には premise search の概念を持ち込まない。
25. 次段階では、premise search の結果を用いた inference-rule applicability または rule application への接続を検討する。








