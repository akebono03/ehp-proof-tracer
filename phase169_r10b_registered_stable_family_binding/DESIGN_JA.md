# Phase 169 R10B — 登録済み安定系列の型付き同定

## 変更対象

- **既存** `phase169_r7_general_stable_transport/rule.py` — `_intermediate_typed_generator()` 全体だけを置換。import は変更しない。
- **新規** `phase169_r10b_registered_stable_family_binding/family_registry.py` — `RegisteredStableFamily`、`read_registered_stable_families()`、`registered_family_of()`、`registered_stable_family_pair()` を追加。import はファイル冒頭。
- **新規** `phase169_r10b_registered_stable_family_binding/tests/test_r10b_registered_family.py` — 40行のうち零元を除く39件の照合、任意回数、合成元、偽装 ID・次数、1回懸垂の境界、証明未生成、パッチ可逆性をテスト。
- **新規** `patch.py`、`audit.py`、`run.ps1`、`__init__.py` — 導入・限定検証・失敗時復元。

## 基本原理

`HyoujiGen.csv` の `kinds=0` は「懸垂系列の命名に使うメタデータ」であり、数学的な懸垂等式の証明ではない。

`n_min` は系列の最小次元。Freudenthal 安定範囲は独立に `n >= k + 2` を要求する。安定範囲外にある `η_2`、`ν_4`、`σ_8` などは、DB 上の名前としては成立しても、その時点で群の懸垂同型とは限らない。

R10B の ID 同定は source/target の完全な `HomotopyElement` 型と照合し、`symbol.family`、`index`、`dimension`、`source`、`target`、`display`、`minimum_n` を検証する。単純な名前一致による GeneratorImage の導入は禁止する。

R7 は引き続き群構造の先行する命題、Toda (4.5)、各回の証明済み `GeneratorImage` を必要とする。Proof Tree と Reference は変更しない。

## 変更した関数・追加コードの全文

`CHANGED_CODE_JA.md` に、追加した `family_registry.py` 全文、置換用 `_intermediate_typed_generator()` 全文、追加テストファイル全文を収録した。実行後は `output/_intermediate_typed_generator_FULL.py` と `output/phase169_r7_general_stable_transport.rule.py.FULL` も出力する。

## 完了条件

限定 pytest（R10B/R7/R10A/R10A2）が PASS、代表的 1-stem と 2-stem の Proof Tree 検証・Web 検証が PASS、既存 Reference と Renderer を変更していない、CSV から証明済み GIVEN を作らない、全体 pytest を実行しない。

## 次段階との境界

R10B では $$ で定義や引用を推測しない。特に `ν` と `σ` の一般定義が現行の共通スクリーン済み命題台帳から ProofStep として参照可能かは別途調査する。データベースに系列名があるだけで $\pi_8^5$ が complete になることはない。
