# Phase 174 R3-R7-R1：零群 Root の出典優先監査

## 目的

先行 R3-R7 JSON は、`pi_12^7` の `TodaPrimaryGroupZeroStatement` を確認したが、`Relation` 候補がないため Root の backward expansion（逆向き推論候補）を測定していない。今回は、その欠落だけを埋める。

## 根拠と、まだ証明されていないこと

- 参照した GitHub `develop`：`992975395195a0e49955617ba1ae772127036dde`。
- Toda Proposition 5.9 の転写本文には、$\pi_{n+5}^{n}=0\ (n\ge 7)$ が記載されている。
- 同じ証明には次の完全列がある。

$$
\pi_{13}^{13}\xrightarrow[\cong]{\Delta}\pi_{11}^{6}\xrightarrow{E}\pi_{12}^{7}\longrightarrow\pi_{12}^{13}=0.
$$

- 数学的には、この列の Exactness（完全性）、$\Delta$ の全射性、および右端の零群が検証できれば、$\pi_{12}^{7}=0$ が従う。
- しかし、これらの typed（型付き）証明前提が探索内で成立していることは未検証である。
- 本監査は Prop 5.9 の群構造結論を直接 GIVEN にせず、群別専用推論規則を追加しない。

## 既存規則について

`toda_stable_group_transport.py` に Toda (4.5) generic zero-group transport（零群の汎用輸送）が存在する。ただし、輸送元の零群の証明が先に必要なため、基準点 $\pi_{12}^{7}$ をこれだけで解決できない。

## 変更対象

**新規ファイルのみ**：

- `phase174_r3_r7_r1_zero_root_audit/audit.py`：read-only の Source Guard、入力 JSON の検査、零群 Root の展開候補調査。
- `phase174_r3_r7_r1_zero_root_audit/tests/test_audit.py`：限定単体テスト。
- `phase174_r3_r7_r1_zero_root_audit/run.ps1`：`-DryRun`／通常実行。
- 同ディレクトリの `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`__init__.py`、`evidence/phase174_r3_r7_audit.json`。

既存ファイル、既存関数、既存 import、5つのプロジェクト文書は変更しない。

## 完了条件

1. GitHub HEAD と出典転写・関連コードの Git blob SHA が一致する。
2. 既存の7群監査 JSON と $\pi_8^5$ 16ステップ完成証拠に矛盾がない。
3. $\pi_{12}^{7}$ の零群 Root を独立出典審査のもとで実際に probe できる。
4. $\pi_{11}^{6}$ の現在の typed 探索状態も計測する。
5. 直接の零群 GIVEN がなく、限定 pytest が PASS する。
6. 全体 pytest は実施しない。

## 次の境界

Root の候補と不足前提の報告まで。EHP Exactness（完全性）由来の一般的な零群推論規則や文献登録、Proof Tree の新規ステップは R3-R7-R2 以降、実測された前提が揃う場合に限る。
