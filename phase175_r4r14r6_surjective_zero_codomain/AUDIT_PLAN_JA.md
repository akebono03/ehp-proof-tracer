# Phase 175 R4R14R6 監査・実装計画

## 目的

R4R14R5 で接続済みの生成元零像と、EHP 完全性から導かれる懸垂写像の全射性を、零群の一般結論へ接続する。

## 対象

- 変更する既存ファイル: `phase165_r52_r9_shared_math.py`
- 変更する既存関数: `shared_expansion_provider()`（追加の一般候補一つのみ）
- 新規ファイル: `phase175_r4r14r6_surjective_zero_codomain/rule.py`
- 新規関数: `surjective_zero_codomain_inputs()`、`surjective_zero_codomain_rule()`、`expand_surjective_zero_codomain()`
- 新規実行・検証: `installer.py`、`audit.py`、`tests/test_rule.py`、`tests/test_installer.py`、`tests/test_public.py`、`run.ps1`

## 数学的規則

証明済みの $f:A\to B$ 全射性と $\operatorname{im} f=0$ から $B=0$ を導く。対象の $B$ に対する標準的懸垂写像 $E$ を候補として選択するが、両前提は独立の Proof Search に委ねる。

## 出典・証明の境界

Toda (5.9) の一般 GIVEN を再登録しない。$\pi_{10}^6=0$ を直接 GIVEN としない。既存の $\Delta$ 全射ルートを削除しない。共通 Narrative を変更しない。先行群は既存 DB 優先順位規則を利用する。

## 実施

1. DryRun が Git の branch、ステージ状態、R4R14R5 後の共有ソース blob を検査する。
2. 本実行では共有 Provider に一か所のみ追加する。
3. 限定 pytest だけを実行する。`--import-mode=importlib` と `-p no:cacheprovider` を使用する。
4. 実際の Group Proof Search を一回実行し、status、proven_steps、open_goals を JSON に記録する。
5. 全体 pytest は Phase 175 の終了時のみ。

## 完了条件

一般ルールの独立検証、共有 Provider への導入、実探索の正直な状態記録が揃うこと。証明完成は Gate の条件に含めない。実探索が完了した場合も別途 Web と Trust 検証が必要。

## 次段階との境界

探索が partial/search_failed なら、JSON の open goals と proof steps を使い次の不足義務だけを対象とする。別の規則を先回り追加しない。
