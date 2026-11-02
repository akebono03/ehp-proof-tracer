# Phase 173 R4-R1 — 4前提の独立閉包監査

## 対象と背景

先行の source-bound 監査は Root Candidate 1件を生成したが、公開探索は `partial` のままだった。この結果だけでは、4つの Subgoal のどれが未証明か特定できない。

変更対象は新規ディレクトリ `phase173_r4_r1_subgoal_closure/` の7ファイルのみ。既存のソース・規則・文献・正式ドキュメント5件は変更しない。

## 検査する4前提

1. Toda Proposition 4.4 の引用済み一般命題（GIVEN）
2. 先行結果 $\pi_6^3=\mathbb Z/4\{\nu'\}$ の正確な型付き証明
3. $\pi_7^7=\mathbb Z\{\iota_7\}$ の推論による証明
4. $H(\nu_4)=\iota_7$ の推論による証明

4前提を、Root と同じ出典フィルタ済み Context（引用文脈）の下で別々に検査する。既存の `reconstruct_registered_goal()` を直接実行し、証明された場合だけ `PROVED` と記録する。

Toda Lemma 5.4 の原文トークン、アーカイブ件数、引用済み FIXED 証明の件数を別に記録する。原文・アーカイブの存在だけで証明済みとは認定しない。

## 監査の境界

- `rule.py` の改変も Provider の常設接続も行わない。
- DB Goal、歴史的ルール定義、アーカイブを GIVEN に昇格させない。
- 新しい源泉情報や位数を追加しない。
- 全体 pytest は Phase 173 終了まで実行しない。
- 完了条件は限定 pytest PASS、Source Guard PASS、各前提の真の証明状態を表示、JSON 保存。4前提が成立してもこの監査自体は Root の ProofStep を生成しない。

## 次 Phase との境界

次の変更は、未証明と確定した前提に限定する。$\pi_8^5$ の位数8・巡回構造（R4-R2）は実装しない。
