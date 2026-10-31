
## Phase 171 — $\pi_6^3$ の完成証明と表示責務の境界（2026-10-31、Closeout R2）

Phase 171 は登録済み $\pi_6^3=\mathbb Z/4\{\nu'\}$ の公開 Backward Search（逆向き探索）を `complete` に到達させた。EHP 完全列の厳密性から $E:\pi_5^2\to\pi_6^3$ の単射性、$H:\pi_6^3\to\pi_6^5$ の全射性を導き、両端が位数2の群であることから

$$
0\longrightarrow\pi_5^2\xrightarrow{E}\pi_6^3\xrightarrow{H}\pi_6^5\longrightarrow0
$$

を証明する。したがって $|\pi_6^3|=4$ であり、出典に基づいて推論した $2\nu'=E(\eta_2^3)\ne0$ によって $\operatorname{ord}(\nu')=4$ を得る。結論を表示するために未証明の `GIVEN` を追加する方法は採用しない。

Proof Tree（証明木）は数学的事実・推論と依存を保持し、Proof Narrative Model（証明文章モデル）は実際の root ancestry（根の祖先）に結びつく引用のみを投影する。Renderer（表示器）はその検証済み内容だけを文章化する。Phase 171 R20R12 は証明済みの位数計算を文章化し、R20R13/R2 は同一の引用を持つ連続した検証済み $\eta$ 懸垂等式のみを統合する。複数の空行を越えることは許すが、非空の別の推論や異なる引用を飛び越えることはできない。ピリオド後の改行処理は完成証明の本文に限定し、Reference や数式内部を変更しない。

R20R13R3 はインストーラの HEAD 固定条件を内容検査へ変更し、R20R13R4 はテストの行頭一致判定を修正した。Closeout R1R1 は Phase 169 R3Z の歴史的な28ステップ固定を、探索結果との同一性、推論根、`complete`、未解決目標ゼロの検査へ置換した。これは数学的結果・探索規則・Reference に手を加えない**テストの意味的保守**である。限定回帰は Windows で 88 PASS、インストーラ検査 5 PASS。

Phase 171 の完全証明には引用8件が対応する。`generic-complete-proof`、出典に結びつく証明木、Web 表示が一致することを完了認定の対象とする。Phase 終了時の現行アクティブ `tests/` 全体 pytest は本 R2 の時点では未実施であり、Phase 171 正式終了はその Gate の検証後に確定する。$E(\eta_5)=\eta_6$ の同義反復、長い $H$ の途中式、全射性の重複、`DB prior` の説明改善は Phase 172 の表示品質候補であって、証明木に未証明の事実を追加する理由にはならない。
