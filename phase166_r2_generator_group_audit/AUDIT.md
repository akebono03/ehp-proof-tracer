# Phase 166 R2 — 生成元・群構造の対応監査

## 監査対象

- `HyoujiGen.csv` の `id`, `display`, `k`, `n`, `latex`, `orders`
- `sphere(3).csv` の `n`, `k`, `id`, `generator`, `orders`, `Element`, `gen_coe`
- 既存 `repository.py` の `SphereRepository` と、`expression.py` の `GeneratorSymbol`, `HomotopyElement` の設計境界

## 方針

`Element` の数列から `HyoujiGen.csv` の `id` を検索する。ただし、ID が一致しただけでは、生成元・合成・懸垂・群構造の数学的内容を証明したことにしない。`Element` は複数 ID を含むため、単一生成元名との単純な文字列一致を主張しない。生成元の `k,n` は基礎生成元の値であり、合成後の群次数との相違を直ちに誤りとみなさない。

## 完了条件

欠損 ID と重複 ID を検出でき、候補対応の一覧を出力できること。すべての行の証明資格は未付与であること。

## R3 との境界

R2 はデータの候補対応のみ。文献命題との意味的同一性の確定と引用資格は行わない。全体 pytest は R10 のみ。
