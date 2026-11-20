# Phase 176 R3R27R1 — Toda (5.5) 第2関係の独立実装

## 対象

$$
4\nu_n=\eta_n^3=\eta_n\circ\eta_{n+1}\circ\eta_{n+2}\quad(n\ge5).
$$

出典は `sources/toda/Toda_05_2.tex` の (5.5)。ハッシュと出典順序の検証は既存の `verify_extension_texts()` を利用し、さらに同一 (5.5) ブロック中の第2関係と直前の $\eta_n^3$ の定義を照合する。

## 確認した既存コード・テスト

- `phase174_r3_r6_source_extension/source.py` と `tests/test_source.py`
- `phase169_r10d2_general_family_definition/family_citation.py`
- `phase165_r12_r20_eta_definition.py`
- `phase171_r2e_toda53_double_reference.py` と関連テスト
- `phase165_r52_r9_shared_math.py`

## 変更対象

既存ファイルの変更は **なし**。次の新規ファイルをディレクトリ `phase176_r3r27r1_toda55_quadruple_isolated/` に追加する。

- `source.py`：新規 `Toda55UniversalQuadrupleStatement` クラス、`build_cited_toda55_quadruple_source`、`canonical_quadruple_goal`、`quadruple_inputs`、`cited_quadruple_rule`、`expand_cited_quadruple`。クラスは import と定数の直後に配置する。
- `audit.py`：`checked_head`、`capture`、`report_path`、`execute`、`main`。
- `tests/test_source.py`：出典検証・n の一般化・型と前提の拒否テスト。
- `run.ps1`：DryRun、本監査、限定 pytest を実行。
- `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`__init__.py`、`tests/__init__.py`。

ソースファイルとテストファイルはすべて新規であり、import は各ファイル全文に含める。追加した新規クラス・関数・テスト関数は `CODE_FULL_JA.md` に省略せず全記載する。

## 証明義務

- ν-family の当該 member は別途 **INFERENCE** で証明される。
- Toda (5.5) の第2関係は出典検証済み **GIVEN**。
- η-family の一般表記は出典検証済み **GIVEN**。
- 上記の3前提をもって型付き関係の特殊化を **INFERENCE** する。
- 不正な添字、変更された右辺、重複・欠落した出典、GIVEN による member の代用を拒否する。

## 完了条件

DryRun、本監査、限定 pytest が PASS し、$n=5$ の特殊化候補と3つの未解決前提が記録される。候補を得たことを ProofStep 完成とは数えない。全体 pytest は Phase 176 終了時だけ。

## 次 Phase 境界

R3R28 では、R3R27R1 のテスト結果を踏まえて、この出典と拡張を共有 Source-first Proof Search へ接続する。今回、既存の共有 provider、既存の (5.5) 第1関係、Web Renderer は変更しない。π₈³ の巡回構造は未完成のままとする。
