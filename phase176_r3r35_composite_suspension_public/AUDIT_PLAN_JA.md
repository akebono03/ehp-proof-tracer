# Phase 176 R3R35 監査・実装計画

## 現行コード・関連テスト

GitHub `akebono03/ehp-proof-tracer` の `develop` を先に確認。対象ファイルは `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()`、既存の `phase171_r2h_prop22_cited_hopf/source.py`、`phase169_r10eq_r1_universal_stable_definition/definition.py`、`phase165_r12_r21_eta_generator_chain.py`、`proof.py`、`tests/test_hopf_rules.py`。既存 R3R34 の `source.py`・`tests/test_source.py` は前段で検証済み。ローカル `develop` のコミット ID との完全一致は要求しないが、変更アンカーを厳密に検査する。

## 変更対象

1. 既存 `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 内部の `expand()` の一か所に、R3R34 を呼ぶ import と候補生成行を追加。既存トップレベル import の変更はない。
2. 新規 `phase176_r3r35_composite_suspension_public/installer.py`: `_shared_expand_location()`、`proposed_code()`、`changed_function_text()`、`git()`、`preflight()`、`install()`、`main()` を追加。
3. 新規同ディレクトリの `audit.py`: `probe()`、`main()` を追加。
4. 新規 `tests/test_installer.py`（4テスト）と `tests/test_public.py`（2テスト）。
5. 新規 `run.ps1`、英語 `README.md`、日本語 `AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

新規ファイルはすべて新規ディレクトリの下。R3R34 の規則本体・既存テスト・既存 API・出典登録・Renderer・既存5文書は変更しない。

## 目的

Source-first（出典優先）の根コンテキストで、型付き関係

$$E(\eta_5\circ\eta_6)=\eta_6\circ\eta_7$$

への `GoalExpansion` を公開 Provider が生成すること、そこから `GeneratorImage` を独立前提として要求することを確認する。孤立した推論の再生と共有 DFS の出典順序による承認は別に扱い、後者の成功や群構造の証明完成を主張しない。

## 実行する限定 pytest

```text
python -B -m pytest -q -p no:cacheprovider phase176_r3r35_composite_suspension_public/tests/test_installer.py
python -B -m pytest -q -p no:cacheprovider phase176_r3r35_composite_suspension_public/tests/test_public.py
python -B -m pytest -q -p no:cacheprovider phase176_r3r34_composite_suspension_isolated/tests/test_source.py
python -B -m pytest -q -p no:cacheprovider tests/test_hopf_rules.py -k "hopf_composition_formula or hopf_invariant_reaches_hopf_composition_formula"
```

全体 pytest は Phase 終了時にだけ実施。

## 完了条件

DryRun と本実行が成功し、変更関数全文・バックアップ・監査レポートが出力され、公開候補1件の独立前提が `GeneratorImage` に一致し、限定 pytest が通ること。Hopf 像と根の群構造は未完成のままとする。

## 次段階との境界

R3R36 以降に Proposition 2.2 の右因子が `Suspension(Composition(...))` である場合の型付き判定、合成懸垂の等式移送、文献順序の Source Guard を別に監査する。結論の直接 GIVEN は作らない。
