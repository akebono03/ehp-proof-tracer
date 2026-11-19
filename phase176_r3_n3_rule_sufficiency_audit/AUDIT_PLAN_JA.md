# Phase 176 R3 — 一般推論規則の充足性監査

## 変更対象

- 新規 `phase176_r3_n3_rule_sufficiency_audit/audit.py`：`git`、`check_source_anchors`、`preflight`、`safe_detail`、`describe_expansion`、`summarize_proposals`、`observe`、`worker`、`report_path`、`execute`、`main`。
- 新規 `phase176_r3_n3_rule_sufficiency_audit/run.ps1`：DryRun・限定 pytest・監査本実行。
- 新規 `phase176_r3_n3_rule_sufficiency_audit/tests/test_audit.py`：監査契約の限定テスト5件。
- 新規 `__init__.py` 2件、README、監査仕様と全コード。

既存の数学規則・Provider・GIVEN・Web Renderer・主要5文書・関連テストを変更しない。

## 数学的対象と型付き証明義務

対象は $\pi_8^3=\mathbb Z/2\{\nu'\eta_6^2\}$。R2 の探索は `search_failed`、Open Goals 3件。これは下記3系統の証明義務と1対1の対応を保証しない。

1. Lemma 5.7 と Proposition 5.8 による $E\pi_7^2=0$、EHP 完全性 (4.4) による $H$ の単射性。
2. Proposition 5.6 の $\pi_8^5=\mathbb Z/8\{\nu_5\}$、(5.5) の $4\nu_5=\eta_5^3$、Lemma 5.7 の $\Delta\nu_5=\pm\eta_2\nu'$、(5.2) の $\pi_6^2$ を合わせた $\ker\Delta=\langle4\nu_5\rangle$。
3. Proposition 2.2 と (5.3) による $H(\nu'\eta_6^2)=\eta_5^3$、単射性と生成元像を用いる群構造決定。

## 監査方法と完了条件

- R2 確認済み HEAD を祖先に持つ `develop`、追跡ファイル clean、原文アンカーを DryRun で確認。
- 公開 `search_group_from_registered_goal(3,5)` の現行結果から未解決 Goal の型、文字列、診断、ProofStep を取得。
- `build_shared_typed_bridge()` で登録済み FIXED_STATEMENT と GIVEN のリンクを読み、共有 Provider を未解決 Goal に対して**提案取得だけ**行う。
- 提案は未証明であり、Rule の存在も数学的充足性を保証しない。`proposal_count=0` はこの監査構成での候補ゼロを意味する。
- stdout に各 Goal の提案数、JSON に証拠詳細を保存。全体 pytest は Phase 最終工程まで実施しない。
- R3 監査の成功は証明完成ではない。次の実装 Phase は各 Goal の出典・型・既存規則の欠落をレポートに基づき限定する。
