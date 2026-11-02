# Phase 173 R4-R1：Toda (5.6) 出典付き候補の限定実装

## 対象

- 新規 `phase173_r4_r1_source_bound_56/rule.py`：`_target_generators`、`_diagonal_goal`、`source_bound_toda56_rule`、`expand_source_bound_toda56`。
- 新規 `phase173_r4_r1_source_bound_56/audit.py`：`_git`、`preflight`、`inspect_runtime`、`main`。
- 新規 `run.ps1`、限定テスト `tests/test_rule.py`、`README.md`、`__init__.py`。

既存クラス・既存関数・公式5文書は変更しない。全体 pytest は Phase 173 の終わりまで行わない。

## 数学的条件

Toda Proposition 4.4 の引用済み一般命題、先行する $\pi_6^3=\mathbb Z/4\{\nu'\}$、導出済み $\pi_7^7=\mathbb Z\{\iota_7\}$、独立に導出した $H(\nu_4)=\iota_7$ が4前提。H の関係は `ProofRule.INFERENCE` を必須とする。これが無ければルート候補は未完成のまま残す。

$$
(\alpha,\beta)\mapsto E\alpha+\nu_4\circ\beta
$$

により生成元 $\nu'$ は $E\nu'$ に、$\iota_7$ は $\nu_4$ に写る。DB Goal、出典テキスト、提案そのものを GIVEN にしない。

## 完了条件

1. 既存の reviewed blob が Git HEAD と作業ツリーで変わっていない。
2. 限定 pytest が PASS。
3. ソースの固定引用が1件で、Root が1件以下。
4. SearchStatus と OpenGoals を audit.json に記録する。
5. `COMPLETE=False` なら証明完成と宣言しない。

## 次の境界

今回の孤立した提案実装が数学的に成立することを確認してから、公開経路への常設接続を判断する。$\pi_8^5$ の位数8導出は R4-R2 の範囲とする。
