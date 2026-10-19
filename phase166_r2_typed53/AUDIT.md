# Phase 166 R2 — 式 (5.3) 型付き対応監査

## 目的

Toda の式 (5.3) に対応する CSV の4行のうち、表示が `\eta3^3` と `2\nu'` に一致する2行について、既存の `HomotopyElement`、`GeneratorSymbol`、`Composition`、`Multiple`、`Relation` を用いた型付き表現を構築し、両辺の定義域・値域を照合する。

## 確認した現行コード

- `expression.py`：`HomotopyElement` の `source` / `target`、`Composition.is_type_compatible()`、`Multiple`。
- `proof.py`：`Relation`、`RelationType.EQUALITY`。
- `toda_literature_statement_boundary.py`：`nu_prime_double_relation` は `RELATION` 役割の構成要素。
- `phase163_r4_registry_bridge.py`：文献構成要素はメタデータとして登録する。
- 関連テスト：`tests/test_expression.py`、`tests/test_repository.py`。

## 型付き候補

- `η₃: S⁴ → S³`、`η₄: S⁵ → S⁴`、`η₅: S⁶ → S⁵` を明示的に構築する。
- `ν′: S⁶ → S³` を明示的に構築する。
- `η₃ ∘ (η₄ ∘ η₅)` と `2ν′` は、ともに `π₆(S³)` の型を持つ。

これは**型の整合性**であり、等式の真偽を検証していない。

## 変更一覧

既存ファイル、クラス、関数の変更はない。新規パッケージ `phase166_r2_typed53` のみに `audit.py`、`test_audit.py`、`run.ps1`、`README.md`、`AUDIT.md` を追加する。`audit.py` の `typed_witness()`、`inspect()`、`main()` を新規追加した。

## テスト

`python -m pytest -q phase166_r2_typed53/test_audit.py` の限定3テスト。全体 pytest は Phase 166 R10 まで実施しない。

## 完了条件と境界

- 4行の抽出、うち2行の表示候補一致。
- 合成の型整合性、両辺の所属 `π₆³`。
- 証明資格0件、数学的同一性確認0件。
- 次工程で原典の具体的主張、記号と式の正規化、生成元データとの照合を行う。R3 の引用資格は与えない。
