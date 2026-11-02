# Phase 173 R4-R1：Lemma 5.4 出典付き Hopf 関係の接続

## 直前の監査で確定したこと

- Proposition 4.4：`PROVED:given`
- $\pi_6^3=\mathbb Z/4\{\nu'\}$：`PROVED:inference`
- $\pi_7^7=\mathbb Z\{\iota_7\}$：`PROVED:inference`
- $H(\nu_4)=\iota_7$：`UNRESOLVED`、Root は等式対称性のみ
- Lemma 5.4：アーカイブ1件、SHA-256 検証済み、引用可能な固定 ProofStep 0件

## 変更対象

既存ファイルを変更しない。以下はすべて新規追加。

- `phase173_r4_r1_lemma54_source_bridge/source.py`：`TodaLemma54TypedSource`、`canonical_hopf_relation`、`validate_lemma54_text`、`_validated_archive`、`add_verified_lemma54_source`、`lemma54_hopf_inference_rule`、`expand_cited_lemma54_hopf`
- `phase173_r4_r1_lemma54_source_bridge/audit.py`：`git`、`validate_audit_additions`、`guard_sources`、`collect_ancestry`、`inspect_runtime`、`main`
- `phase173_r4_r1_lemma54_source_bridge/run.ps1`
- `phase173_r4_r1_lemma54_source_bridge/tests/test_source.py`、`tests/test_audit.py`
- `__init__.py`、`README.md`、本ファイル、`CODE_FULL_JA.md`

## 出典の扱い

出典のアーカイブ行は `SOURCE_ARCHIVE` のままとする。アーカイブと実在する Chapter V 原文を照合し、SHA-256 が一致し、Lemma 5.4 の正確な全3条件を持ち、さらに既存の引用位置で Proposition 5.6 より先行するときだけ、同一の文献 Reference のもとに `TodaLemma54TypedSource` を追加する。これは引用された固定文献命題であり、DB Goal や未証明の群構造を GIVEN にすることではない。

Hopf 等式 $H(\nu_4)=\iota_7$ は必ず `ProofRule.INFERENCE` によってその命題から導出する。原文不一致、引用順序不明、出典欠落では停止する。

## 試験の範囲

`shared_expansion_provider` に新規 Root と Hopf 断定の候補生成器を **実行時のみ** 加える。`search_shared_group_goal` の既存推論チェックを使う。完成した場合は真正な Root ProofStep の祖先に新規 Lemma 5.4 文献 GIVEN と Hopf INFERENCE の両方が含まれることを要求する。

本体コード・DB・引用台帳・公式文書に変更は加えない。Web 本番経路への常設接続と全体 pytest は行わない。
