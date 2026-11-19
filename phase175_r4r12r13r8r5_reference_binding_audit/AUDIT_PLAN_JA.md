# R13R8R5R2 — Web 退行判定条件の訂正

## 前提

R13R8R5R1 は DryRun PASS、限定 pytest 5 passed だが、実証監査で `R3_R7_WEB_REGRESSION` となった。R13R8R4 の Web 目視確認では R3・R7 の Reference 数式および本文「より」が存在する。

## 原因

以前の `all(value.values())` は `direct_typed_consumer`（GIVEN の包む命題と推論結果の Python オブジェクト完全一致）を表示の必須条件に含めていた。R3 の検証済み記法変換では、この一致は保証されない。

## 修正

- 表示の退行条件を Reference 本文、本文引用、Web provenance に限定。
- `direct_typed_consumer` は調査項目として維持。
- 実際の表示不一致があった場合は対象全件をレポートに記録してから失敗。
- 新規 GIVEN・数学規則・製品コードの変更なし。

## 完了条件

DryRun と限定 pytest の成功、3群の実証監査レポート出力、R3・R7 の表示退行なし。監査合格は全 Reference の自動表示実装完了を意味しない。次の R13R8R6 で残る共通の表示欠落を扱う。
