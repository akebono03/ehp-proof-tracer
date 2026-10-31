# Phase 171 R20R5 — 公開探索の位数4推論接続監査

## 監査の対象

R20R4 では $\pi_6^5=\mathbb Z/2\{\eta_5\}$ および $|\pi_6^3|=4$ は PROVED、$\operatorname{ord}(\nu')=4$ は未解決であった。

R4-R7 の既存の独立した証明木では、$2\nu'\neq0$ と $\operatorname{ord}(\nu')=4$ が型付き推論で導出される。この R20R5 はその完成証明を公開探索へ渡さず、公開 `shared_expansion_provider()` に同じ推論の backward proposal（後ろ向き証明候補）が登録されているかだけを検査する。

## 判定

* `CERTIFIED_PUBLIC_PROPOSAL_PRESENT`：規則名と順序付き Subgoal が合致し、既存の実際の ProofStep に対し matcher（照合器）が結論を再構成できる。
* `MISSING_MATCHING_PUBLIC_PROPOSAL`：同じ推論候補が公開 provider にない。
* `PUBLIC_RULE_DOES_NOT_CERTIFY_REAL_PARENTS`：候補が存在しても実際の親証明を照合できない。
* `PROVIDER_ERROR`：provider 自体が例外を出した。

## 信頼境界と Phase の範囲

新規 GIVEN 0件。本番コード変更なし。先行完成証明木は検査用の基準として使うだけで、公開探索器・Web に注入しない。数学的規則は追加しない。Web の完成判定もしない。全体 pytest は実行しない。

次の実装は、不足した backward proposal のみを追加する。既存の成功候補があるなら重複登録しない。
