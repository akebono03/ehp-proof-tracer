# Phase 174 R3-R7-R12 — Toda (5.9) 一般消滅関係の出典監査

## 現行コード・既存テストの確認

2026-11-06 に GitHub `akebono03/ehp-proof-tracer` の `develop` の
HEAD `162a72e42a7eadc16c62555de8239391bb5175cc` を確認した。
R11 の監査・テスト、R10 の出典監査、既存の型付き一般特殊化
`phase165_r57_r20_general_specialization.py`、
`phase169_r10d2_general_family_definition/family_citation.py`、
`phase169_r10b_registered_stable_family_binding/family_registry.py`、
`proof.py` と関連する tests を確認した。

## 変更対象

新設の `phase174_r3_r7_r12_toda59_annihilator_source/` 配下に限定。

- `source.py`：`CitedFamilyAnnihilator`（新設クラス）、`verify_toda59_annihilator_text()`、`reviewed_toda59_annihilator_schema()` を追加。
- `rule.py`：`canonical_annihilator_instance()`、`annihilator_specialization_inputs()`、`cited_annihilator_specialization_rule()`、`expand_cited_annihilator_specialization()` を追加。
- `audit.py`：Source Guard、R11 の認証済みレポート、公開候補数、未登録の出典命題を読み取り専用で照合。
- `tests/test_source.py`、`tests/test_rule.py`、`tests/test_audit.py`：否定条件を含む限定テスト。
- `run.ps1`：限定 pytest の別プロセス実行、DryRun と本実行。
- `README.md`：英語の実行説明。

既存の本番ソース、既存テスト、共通 Renderer、主要5文書は変更しない。

## 数学上の責務

採用転写 `sources/toda/Toda_05_2.tex` の Proposition 5.9 の証明中にある
(5.9) の一般関係は以下のとおり。

$$\nu_n\circ\eta_{n+3}=0\quad(n\ge6).$$

`HyoujiGen.csv` の ν（family ID 4）・η（family ID 2）は名前・型の
メタデータであって証明ではない。採用転写の照合だけでも `ProofStep` は作らない。
今回の一般推論規則は、正式に出典認証された一般命題が別途 `GIVEN`
として存在するときに限り、その型付き特殊化を `INFERENCE` として許可する。
今回は出典命題そのものを登録しない。群 `π₁₂⁷=0` の直接 GIVEN も禁止する。

## 完了条件・次段階

- Source Guard と R11 証拠検査 PASS、限定 pytest PASS。
- ν₆∘η₉=0 の型付き候補1件、公開に出典一般命題 GIVEN 0件を実測。
- 公開の左因子零関係が依然 `equality symmetry` のみなら未完成維持。
- 既存 Proof Search・Narrative・Web 非変更、全体 pytest は行わない。

次の R13 は、証明出典の参照・registry と接続するための設計監査とし、
Source-first の信頼境界を通らず直接目標を GIVEN にしない。
