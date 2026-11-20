# Phase 176 R3R8 — Lemma 5.7 既存 Provider の独立接続検証

## 既知の事実

R3R7 は出典1件から $E(\eta_2\circ\nu')=0$ の型付き生成元零像を既存規則で導出し、限定テスト7件を PASS。共有 Provider の同じ目標に対する候補数は0件、$(n,k)=(3,5)$ は Open Goals 3件のまま。

## 今回の変更対象

新規 `phase176_r3r8_lemma57_provider_binding/` のみ。`audit.py`、`run.ps1`、`tests/test_audit.py`、`__init__.py`、`tests/__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md` を追加。既存クラスとメソッドは変更しない。

## 証明の境界

1. Phase 175 の採用 Toda Lemma 5.7 を出典ハッシュと登録順序で再確認する。
2. 既存の独立出典選別により、対象と同じ群構造の結論を直接採用しない。
3. 既存 `expand_cited_lemma57_explicit_zero` を使い、基礎零像に限り1件の追加推論候補を提示する。
4. 真の `GIVEN` 出典から matcher/factory 経由で `INFERENCE` ステップを生成し、未検証の `GIVEN`、根の直接証明、公開 Provider の変更を禁止する。
5. 別の目標に対する候補が変更されないことを確認する。

## 完了条件

DryRun PASS、限定 pytest PASS、独立接続監査 PASS、候補数が基礎目標に限り1件増加し、実際の推論ステップが検証されること。公開の $\pi_8^3$ 完成証明は依然対象外。

## 次工程との境界

右合成移送、懸垂の零像、Hopf 単射性、$\ker\Delta$ の位数2の像の生成元同定を将来の工程として残す。今回の一時 Provider を公開探索へ自動追加しない。Phase 174 Source Guard 既知4失敗は変更しない。全体 pytest は Phase 176 の最後だけ実施する。
