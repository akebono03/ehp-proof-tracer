# Phase 174 R3-R7 — 実装前 Source-first 数学監査

## 変更対象

既存の本体ファイル、クラス、関数、メソッドは変更しない。

新規ファイル：`phase174_r3_r7_source_first_audit/audit.py`、`tests/test_audit.py`、`run.ps1`、`__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。新規関数は監査専用モジュールに追加し、既存の API に影響させない。

## 確認した出典

- Toda Chapter V (5.6)：任意の該当次元 $i$ について、$(\alpha,\beta)\mapsto E\alpha+\nu_4\circ\beta$ による $\pi_{i-1}^3\oplus\pi_i^7\cong\pi_i^4$。
- Toda Chapter VI Lemma 6.1：$H(\varepsilon_3)=\nu_5^2$、$2\varepsilon_n=0$。
- Toda Chapter VII Theorem 7.1 証明：$\pi_{12}^4$ に (5.6) と Proposition 5.9 を使用。
- Toda Chapter VII Theorem 7.2 証明：$\pi_{13}^4$ に (5.6) と先行群を使用。

文献の定理本文は実装上の GIVEN としない。原著版のページとの独立照合は、このパッケージでは未完了とする。

## 検査する証明義務

- $\pi_{11}^3$ の独立した完成証明と $\varepsilon_3$ の記名生成元。
- $\pi_{12}^7=0$ の独立した型付き証明。
- (5.6) の一般的な直和同型と生成元像 $E\alpha+\nu_4\circ\beta$ の型・適用条件。
- $\varepsilon_4=E\varepsilon_3$ の引用付き family 定義との一致。
- 次の stem に対する $\pi_{12}^3$ および $\pi_{13}^7$ の既存状態。
- $\pi_8^5$ が引き続き16段の完成証明であり、直接 GIVEN なしであること。

この段階では候補規則を実装しない。7件は先行監査の到達点に基づく代表的なサンプルであり、次に実装する群を決定するものではない。

## 実行方法と判定

`run.ps1 -DryRun` では関連限定 pytest と SHA／出典／保存済み記録だけを検査する。通常実行では限定的な実探索と Frontier 調査を追加する。双方ともリポジトリの本体ファイルを編集しない。監査 JSON は `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7\audit.json` に書く。

`PASS_PREFLIGHT` は出典の完全性を意味しない。`PASS_READ_ONLY` は検査が実行できたことを示し、新規の数学的完成証明や実装許可を意味しない。エラー時は `NEEDS_REVIEW` とし、推論規則追加に進まない。

次の実装単位は、ソースと未解決 Goal の型付き接続、前提の証明状況、公開経路を検証して初めて決める。全体 pytest は Phase 174 Closeout まで行わない。
