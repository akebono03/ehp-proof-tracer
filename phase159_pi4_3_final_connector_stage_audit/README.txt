Phase 159 pi4_3 final connector stage audit

目的:
repair3 後、pi4_3 group conclusion の重複は解消したが、
「以上より,」が public proof から消えた。

この監査では production pipeline の各段階で

- root conclusion 出現数
- 「以上より,」出現数
- root conclusion を含む paragraph

を記録する。

特に connector count が最初に 1 -> 0 になる段階を特定する。

production code は変更しない。
pytest / 全体テストは実行しない。
