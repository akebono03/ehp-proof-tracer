Phase156-R7 — Reference attribution + derived map-property ownership audit

目的
====

pi_6^3 の Narrative で、Reference attribution（参照帰属）と
derived map-property ownership（導出写像性質の所有関係）が
数学的な証明構造と一致しているかを読み取り専用で監査する。

Production code は変更しない。

監査対象
========

1. pi_5^2

期待する既知結果:

$$
\pi_5^2=\mathbb Z/2\{\eta_2\eta_3\eta_4\}.
$$

現行 repository では
`Toda Proposition 5.6 pi_5^2 eta_2 cube`
として保持されている。

ただし pi_6^3 の root 自身も Proposition 5.6 なので、
`exclude_toda_group_proof_narrative_root_reference()` が
同じ LiteratureReference を丸ごと除外している可能性を調べる。

2. pi_6^5

必要な右端群:

$$
\pi_6^5=\mathbb Z/2\{\eta_5\}.
$$

現行 pi_6^3 graph では
`Toda Lemma 5.4 pi_6^5 finite-cyclic specialization`
に帰属している。

一方 Proposition 5.1 の aggregate data に
higher eta-family result が存在するため、
Proposition 5.1 からの specialization として扱うべきかを
次の実装判断に必要な形で監査する。

3. pi_5^3

$$
\pi_5^3=\mathbb Z/2\{\eta_3\eta_4\}.
$$

これは Proposition 5.3 statement 側の既知結果として
保持されているか確認する。

4. E: pi_4^2 -> pi_5^3

$$
E:\pi_4^2\longrightarrow\pi_5^3
$$

の isomorphism は現行 code では
`Toda Proposition 5.3 n=3 suspension isomorphism`
という step だが、bootstrap 上では Proposition 5.1 と
EHP exactness 等から構成される derived step である。

その premises / consumers を表示する。

5. H: pi_6^3 -> pi_6^5

$$
H:\pi_6^3\longrightarrow\pi_6^5
$$

の surjectivity は Proposition 5.3 statement として
Reference 化すべきなのか、それとも pi_6^3 proof body で
E の isomorphism と exactness から導出すべきなのかを判断するため、
direct premises / consumers / current literature reference を表示する。

実行内容
========

- pi_6^3 depth 2 / 3 の proof presentation を構築
- root Reference exclusion 前後の Reference entries を比較
- pi_5^2, pi_5^3, pi_6^5,
  E: pi_4^2 -> pi_5^3 isomorphism,
  H: pi_6^3 -> pi_6^5 surjective
  の rule / reference / premises / consumers を表示
- Proposition 5.1 aggregate step の higher eta result を確認
- JSON を phase156_r7_audit_output/phase156_r7_audit.json に保存
- 関連する既存 focused tests のみ実行

変更ファイル
============

Production:
- none

Tests:
- new/modified tests none

Audit package:
- phase156_r7_reference_attribution_map_property_ownership_audit/
  - __init__.py
  - audit_phase156_r7.py
  - run_phase156_r7.ps1
  - README.txt

Phase boundary
==============

R7 audit では修正しない。

監査結果に基づき、必要なら次の R7 implementation で
以下を一般規則として分離する。

- root theorem と同じ theorem 内の earlier sibling result
- theorem statement に属する fact
- theorem proof 内だけの derived fact
- EHP exactness から親 proof で再導出すべき map property

Repository-wide pytest は Phase156 closure でのみ実行する。
