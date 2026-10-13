# Phase 165 R14-R17 — 基本事実の根拠付き ProofStep

変更対象（すべて新規）: `phase165_r14_r17_foundational_proofstep.py` の `derive_foundational_suspension_step()` と `audit_r17()`、`test_phase165_r14_r17_foundational_proofstep.py` の6テスト全文、`audit.py`、`run.ps1`、本書。

懸垂された恒等写像が恒等写像になるという周知の基本事実について、`FoundationalReferenceIdentity` を明示した `ProofStep` を生成する。`ProofRule.GIVEN` は「公理的な基本事実」を表し、Toda の文献を検証したという意味ではない。

証明探索全体への無制限の注入や Registry の書換えは行わない。Proposition 4.2 の原文同定・適用条件の検証は別途必要。完成条件は、正しい n>=1 で根拠付き基本事実が得られ、誤った次数や生成元対応が拒否されること。対象 pytest のみ実行。

次工程：共通探索器に foundational premise を認める明示的な安全な入口を設けること、および Prop. 4.2 の TeX 原文・適用条件を確定すること。全体 pytest は Phase 165 最後だけ。
