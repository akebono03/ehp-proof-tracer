Phase 158-R5-4 — Post-unification public Narrative display audit
=================================================================

目的
----
Phase 158-R5-3 で public Narrative を generic multi-argument route に一本化した後の
実出力だけを監査する。

今回の変更
----------
Production code: 変更なし
Test code: 変更なし
pytest: 実行しない

監査対象
--------
代表群:
- pi_6^3   : 現在の表示基準
- pi_8^5   : 旧 dedicated route
- pi_15^8  : 旧 dedicated route
- pi_7^4   : 旧 legacy recursive route 代表
- pi_10^4  : 既存 generic route
- pi_12^5  : 既存 generic route
- pi_16^9  : 既存 generic route

監査項目
--------
1. 左側 proof item numbering
   - **(1)** ...
   - (1) ...

2. equation numbering
   - \tag{N} の出現数
   - 同じ tag の重複
   - 後で参照されない tag
   - 対応する tag が存在しない (N) 参照

3. public shell
   - # Group proof narrative
   - ## 証明対象
   - ## 使用する結果
   - ## 証明
   - ---
   - QED

4. 旧 dedicated route 表現の残存
   - Toda Proposition 5.6 のうち,
   - 直和因子の順序を入れ替えると,

重要
----
R5-4 は修正を行わない。
findings が出ても、この段階では分類と記録だけを行う。

番号付けの修正、文章修正、proof data / semantic structure の補完は、
監査結果を確認した後に別 repair として扱う。

R5-6 の repository-wide audit とは異なり、
R5-4 は route 統一直後の代表群 display audit に限定する。
