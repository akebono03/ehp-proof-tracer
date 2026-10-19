# Phase 166 R1：既存数学データの読取専用監査

## 目的・範囲
提供された `sphere.db` と4種類の CSV の形式・件数・証明資格に関わる欠損を観測する。既存コード、台帳、探索器および原データは変更しない。

## 観測

| 対象 | 件数 | 備考 |
|---|---:|---|
| `sphere(3).csv` / DB `sphere` | 2150 | 群構造・生成元・E/H/P の欄を含む |
| `HyoujiGen.csv` / DB `gen` | 233 | 生成元表示の基本情報 |
| `sphere_relation2.csv` / DB `sphere_relation` | 687 | 関係式を表す内部符号・係数・表示式・出典欄 |
| `TBtable.csv` / DB `TBtable` | 58 | Toda bracket と不確定性 |

関係式 687 行について、`reference` 非空は 675 行、空欄は 12 行、出典文字列の異なりは 625 件。`n` 空欄は11行、`composition` 非空は640行、`rep_linear` 非空は641行、全カラム一致の重複は2行。`order` の内訳は空欄11、0.0が201、1.0が125、2.0が275、4.0が38、8.0が23、16.0が10、32.0が4。

Toda bracket は `reference` 非空53行、`TodaBracket` 非空41行。

## 型付き Relation とデータベースの境界

`Relation(lhs, rhs, relation_type, source, note)` は型付きの等式・零・位数などを保持できる。しかし、CSV の `composition` と `rep_linear` は表示文字列であり、`el_str` と `rep_coe` は符号化値である。`order=0.0` や `order=1.0` の意味も個別検証なしに `RelationType.ORDER` として解釈してはいけない。

`reference` 欄には `(5.3)` のような文献位置と式そのものを含む文字列が混在する。非空は出典が検証済みであることを意味しない。`TodaBracket` も文字列だけでは数学的適用範囲や不確定性を検証できない。

## GitHub の関連実装（前段のコード調査）

- `repository.py`：`SphereRepository` と `RelationRepository`。
- `proof.py`：型付き `Relation`、`ProofStep`、`InferenceRule`。
- `relation_rules.py`：関係式の推論規則。
- `phase165_r8_rule_provider.py`：規則探索モジュールに `relation_rules` を含む。
- `phase165_r9_production_wiring.py`：命題台帳・規則 Provider の構築。既存の関係式 CSV 自動読込経路は確認されていない。
- `phase165_r3_recursive_search.py`：共通逆向き探索と固定文献命題に結び付いた型付き `ProofStep` の選別。

## R2〜R5 に引き継ぐ項目

1. R2：同一数学的事実の識別には、単なる出典文字列や表示式ではなく型、次数、生成元の型、出典識別子を用いる。
2. R3：データベース原文を直接 `ProofRule.GIVEN` に昇格させず、文献引用資格・先行性・循環依存・内部 Proof Tree を確認する。
3. R4：出典・型の検証が通った関係式だけを既存規則台帳の入力候補にし、逆向き探索を限定テストで検証する。
4. R5：群構造・生成元・E/H/P の既知値は目標設定、型検査、結果照合に限定し、自己証明を禁止する。

## 実行と境界

配布物を展開し `powershell -ExecutionPolicy Bypass -File .\phase166_r1_database_audit\run.ps1` を実行する。読取専用で `audit_result.json` のみ更新する。限定 pytest も全体 pytest も実行していない。次は R1 の接続元・出典対応の残余調査、続いて R2 の識別設計。Phase 166 R6〜R9 の証明生成・表示実装は行わない。
