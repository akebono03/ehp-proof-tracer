# Phase 162 R10-R2 証明木監査

監査対象は実際の Web replay の ProofStep 証明木と旧 R10 再構築経路。読み取り専用。

## web_replay

- nodes: 97, edges: 109, GIVEN: 43, INFERENCE: 54
- H(nu_prime)=eta5 nodes: [41, 42]
- Lemma 5.2 inference nodes: []
- cited boundary nodes: [41, 42]
- repeated conclusions (identity-distinct): [[1, 55], [2, 63], [3, 57], [4, 58], [5, 59], [6, 60], [7, 34, 54], [8, 35, 56], [9, 25, 45], [10, 61], [11, 64], [12, 65], [13, 66], [14, 67], [15, 68], [16, 69], [17, 70], [18, 71, 94], [19, 72], [20, 73], [23, 43], [24, 44], [26, 46], [27, 47], [28, 48], [29, 49], [30, 50], [31, 51], [32, 52], [33, 53], [41, 42]]

### 引用・Lemma 5.2・Hopf の使用経路

- node 41 given, -, - / -
  - premises=[], consumers=[42]
  - root paths=[[97, 93, 87, 85, 83, 42, 41]]
- node 42 inference, phase162_verified_literature_citation, (5.3) / -
  - premises=[41], consumers=[83]
  - root paths=[[97, 93, 87, 85, 83, 42]]

### 参考文献の帰属

- (4.5): 2 nodes
- (5.2): 2 nodes
- (5.3): 1 nodes
- Proposition 2.7: 2 nodes
- Proposition 4.4: 2 nodes
- Proposition 5.1: 2 nodes
- Proposition 5.3: 7 nodes

## r10_auxiliary_connection

- nodes: 97, edges: 109, GIVEN: 43, INFERENCE: 54
- H(nu_prime)=eta5 nodes: [1, 2]
- Lemma 5.2 inference nodes: []
- cited boundary nodes: [1, 2]
- repeated conclusions (identity-distinct): [[1, 2], [3, 76], [4, 77], [5, 62, 78], [6, 79], [7, 80], [8, 81], [9, 82], [10, 83], [11, 84], [12, 85], [13, 86], [14, 60, 87], [15, 54], [16, 61, 88], [17, 56], [18, 57], [19, 58], [20, 59], [21, 63], [23, 55], [24, 64], [25, 65], [26, 66], [27, 67], [28, 68], [29, 69], [30, 70], [31, 71, 94], [32, 72], [33, 73]]

### 引用・Lemma 5.2・Hopf の使用経路

- node 1 given, -, - / -
  - premises=[], consumers=[2]
  - root paths=[[97, 53, 47, 45, 43, 2, 1]]
- node 2 inference, phase162_verified_literature_citation, (5.3) / -
  - premises=[1], consumers=[43]
  - root paths=[[97, 53, 47, 45, 43, 2]]

### 参考文献の帰属

- (4.5): 2 nodes
- (5.2): 2 nodes
- (5.3): 1 nodes
- Proposition 2.7: 2 nodes
- Proposition 4.4: 2 nodes
- Proposition 5.1: 2 nodes
- Proposition 5.3: 6 nodes

## 解釈上の注意

- `root paths` は実在する ProofStep オブジェクトの identity で追跡した依存経路。
- 結論が同じノードでも、別の引用適用と GIVEN がある場合は2ノードになる。
- 証明木にない文章が Web に現れる場合は Renderer 側の生成過程を別途調べる。
- 文献分類があることと外部文献の数学的真偽検証は同義ではない。
