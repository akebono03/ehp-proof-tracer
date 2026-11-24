# Phase 176 R3R34 — 監査・実装境界

## 監査した GitHub develop コード

- `expression.py` の `Composition`, `Suspension`, `HomotopyElement`
- `phase171_r2h_prop22_cited_hopf/source.py` の `_formula_parts`, `expand_cited_prop22_right_formula`
- `phase165_r12_r21_eta_generator_chain.py` の `_composition_eta_suspensions`, `composition_eta_suspension_image_rule`, `expand_cited_eta_generator`
- `phase176_r3r30_generic_hopf_substitution_isolated/source.py` の一般 Hopf 代入規則
- `phase165_r52_r9_shared_math.py` の `shared_expansion_provider`
- `relation_rules.py` の `suspension_composition_functoriality_inference_rule`
- `tests/test_hopf_rules.py` の Hopf 合成テスト

## 変更ファイル・関数

既存ファイルの変更はしない。追加位置はリポジトリ直下の新規 `phase176_r3r34_composite_suspension_isolated/`。

- `source.py`：`composite_suspension_equality_input`, `composite_suspension_equality_rule`, `expand_composite_suspension_equality`
- `audit.py`：`preflight`, `probe`, `run`, `main`
- `tests/test_source.py`：`elements`, `goal` と4つの限定テスト
- `run.ps1`, `README.md`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`

## 実装内容

既存の一般 η-generator 合成懸垂規則が証明できる `GeneratorImage(E, composite, suspended_composite)` から、対応する要素等式を得る一般規則を独立実装する。`GeneratorImage` 自体は通常の再帰証明で `ProofRule.INFERENCE` として検証されなければならない。提示された目標式を GIVEN として扱わない。

合成の始域・終域と懸垂による次数シフトを検証し、型不一致・逆方向の等式を拒否する。

## 予定する限定 pytest

```text
python -m pytest -q -p no:cacheprovider phase176_r3r34_composite_suspension_isolated/tests/test_source.py
python -m pytest -q -p no:cacheprovider tests/test_hopf_rules.py -k "hopf_composition_formula or hopf_invariant_reaches_hopf_composition_formula"
```

## 完了条件

DryRun / 監査 / 限定 pytest が PASS し、`existing_image_candidate_rules` と `existing_equality_candidate_rules` の差を記録できること。

## 次 Phase との境界

本 Phase は isolated のみ。公開 Proof Search 接続、Proposition 2.2 での合成式懸垂の一般化、Hopf 像の完成、EHP の群構造結論は未実装。全体 pytest は Phase 終了時のみ。
