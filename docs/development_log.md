# ehp_proof 開発記録

## Phase 1：有限群計算の安定化

### 完了内容
- GroupElement
- GroupMap.apply()
- GroupMap.kernel()
- GroupMap.image()
- EHP 完全列の完全性判定
- n=3, k=5 のテスト
- n=11, k=18 のテスト

### 状態
完了

---

## Phase 2：部分群を構造として扱う

### 2-1 Subgroup 型
- ambient_group
- elements
- generators
- order
- 部分群の等値判定

完了

### 2-2 kernel / image の Subgroup 化
- GroupMap.kernel_subgroup()
- GroupMap.image_subgroup()

完了

### 2-3 生成元の計算
- generated_subgroup_elements()
- find_generators()
- Z/2 ⊕ Z/2 の非巡回部分群をテスト

完了

### 2-4 部分群の抽象群構造
Subgroup.structure() を実装。

例:
- 0 -> ()
- Z/2 -> (2,)
- Z/4 -> (4,)
- Z/2 ⊕ Z/2 -> (2, 2)

完了

### 2-5 structure() の一般化テスト
確認済み:
- Z/2 ⊕ Z/4 -> (2, 4)
- Z/4 ⊕ Z/12 -> (4, 12)
- 自明群 -> ()

完了

### 2-6 EHP への統合
ExactnessResult.image() と kernel() を
元の集合ではなく Subgroup を返すように変更。

以下を追加:
- image_structure
- kernel_structure

完全性判定:
Im(f) = Ker(g)

を Subgroup の等号で判定するように変更。

確認例:
- n=3, k=5
- n=11, k=18

### テスト
2026-08-21

18 passed

---

## 現在の到達点

既知の有限アーベル群と既知の写像について、

- kernel
- image
- 部分群の生成元
- 部分群の位数
- 部分群の抽象群構造
- EHP 完全列の完全性

を計算できる。

---

## 次の予定

### Phase 3：完全列から未知の群構造を推論する

最初の候補:

Phase 3-1
- 商群 B / Im(f) を扱う
- QuotientGroup の導入

完全列

A -> B -> C

に対して

B / Im(f) ≅ Im(g)

を計算できるようにする。