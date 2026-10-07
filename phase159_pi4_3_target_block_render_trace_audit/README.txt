Phase 159 pi4_3 target block render trace audit

目的:
base multi-argument renderer 内で pi4_3 root conclusion が2回描画される
正確な生成元を特定する。

確認対象:
- target block の ProofStep
- direct derivation premises
- direct derivation support steps
- relocatable direct premises
- generic target-block render
- relocated premise 挿入後
- connector 挿入後

各 ProofStep について:
- inference rule
- root step と同一 object か
- semantic key が root と一致するか
- rendered line が root 表示になるか
- conclusion の型と repr

production code は変更しない。
pytest / 全体テストは実行しない。
