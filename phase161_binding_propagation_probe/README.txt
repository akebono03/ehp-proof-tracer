Phase 161: 結論パターンと変数束縛伝播の読み取り専用検証
対象: π_5^3 の E: π_4^2 → π_5^3 の同型性

1. 目標の写像を PatternVariable に束縛。
2. 同じ束縛から単射性・全射性の具体命題を生成。
3. 別の写像と混同しないことを assert。
4. Production Catalog の同じ結論型の規則について conclusion_pattern の有無と一致状況を一覧化。

既存本体コード・テスト変更なし。Phase 59 の専用データや規則ファミリー名は利用しない。
本検証は新しい目標指向証明探索を実装するものではない。
実行: .\phase161_binding_propagation_probe\run_phase161_binding_propagation.ps1
結果: phase161_binding_propagation_probe.json
関連軽量テスト: python -m pytest -q tests/test_phase103_premise_pattern_compatibility_search.py
