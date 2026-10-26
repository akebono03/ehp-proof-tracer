# R3S1 実装・監査記録

## 障害原因

`phase165_r52_r12_component_bridge.expand_cited_given_components()` は
親の `AssertionEntry` を `dataclasses.replace()` で複製して子を登録するため、
子の `scope` も `typed_composite_fields` のままです。
R3S はこれを親複合命題と誤認し、子の dataclass に親の全フィールドを要求して例外となりました。

## 変更対象・単位

- 変更ファイル：`phase168_r3_37c_reference_projection.py`
- 変更関数：`project_reference_bodies()` 全体
- 新規テスト：`tests/test_r3s1_composite_scope.py` の4関数
- import 変更：なし。その他の本番コードと既存テストは変更しません。

## 修正

`scope` 内のフィールド一覧と実体の dataclass フィールド一覧が一致した場合だけ
複合命題を展開します。一致しないときは登録済みの唯一の親依存関係、同じ `scope`、
親側の全フィールド一覧、子の数学的内容と親フィールドの値の一致を検証します。
これに通った個別成分はそのまま表示し、不整合な入力は従来どおり拒否します。
特定の群番号・推論規則名・Reference番号による分岐はありません。

## 検証と境界

新規限定テスト4件、R3Sの4件、既存Reference3件、1-stem回帰10件を順に実行します。
未実施の実リポジトリテストを PASS と報告しません。
全体 pytest は Phase 169 の最後だけです。

`(5.1)` を $\pi_5^5$ の証明木に追加したり、$\pi_7^5$ の検索経路を修正したりしません。
