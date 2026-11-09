# Phase 174 R3-R7-R36 — 一般 Δ 核規則の共通 Provider 接続

## 変更対象

既存ファイル `phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py` の関数 `build_context_expansion_provider_registry()` **全体のみ**を置換する。トップレベル import、既存クラス、既存テストは変更しない。

新規ファイルは `phase174_r3_r7_r36_cited_kernel_provider_wiring/` のみに置く。`install.py`、`audit.py`、`tests/test_static.py`、`tests/test_context.py`、`tests/test_public.py`、`run.ps1` とレビュー済みの原本・置換ファイル全文を含む。

## 数学的契約

独立した3前提 $A=\mathbb Z\{g\}$、$B=\mathbb Z/m\{h\}$、$\Delta(g)=\pm h$ から $\ker\Delta=\langle mg\rangle$ を INFERENCE（推論）で導く、R35 の既存一般規則を再利用する。`Composition`（合成）の各因子の型を検査し、生成元を代理表現に置換しない。

Toda Proposition 5.8 と式 (5.10) の2つの出典付き証明葉は R34 のものを再利用する。対角群 $\pi_{11}^{11}=\mathbb Z\{\iota_{11}\}$ は Toda (5.1) の一般形から既存の特殊化規則で推論する。

## 既存テスト契約の保全

Context Provider Registry の旧テストは、任意のダミー文脈に対して Provider が4件であることを要求する。R36 はこの契約を保ち、有限巡回群の表示と Δ の生成元像が両方とも共通ソース文脈にあるときに限り第5 Provider を接続する。一般規則自体は $n,k$ や生成元名に依存しない。

## 実施順序

1. GitHub 現行 `develop` と R35 のコードをハッシュ検査する。R35 のみを追加した後継 HEAD は差分を照合した場合に限り許可する。
2. DryRun は書き込みを行わない。
3. Installer は1関数だけを置換し、CRLF/LF を保持する。
4. 共通 Provider で一般核規則の逆向き候補を確認する。
5. Toda (5.1) の一般形から対角群を INFERENCE で導き、R34 の2件の GIVEN と組み合わせた核 ProofStep の親を検査する。
6. 限定 pytest のみ実行する。全体 pytest は Phase 最終工程まで行わない。

予定 Gate: `PASS_R36_CITED_CYCLIC_KERNEL_PUBLIC_PROVIDER_CONNECTED_ROOT_PENDING`。

## 未実装・次工程

本工程は $E\pi_{10}^{5}=0$ の証明や $\Delta:\pi_{13}^{13}\to\pi_{11}^{6}$ の全射性を導かず、$\pi_{12}^{7}=0$ の完成を宣言しない。次工程で必要な EHP 完全性と上側 Δ 全射性を改めて監査する。
