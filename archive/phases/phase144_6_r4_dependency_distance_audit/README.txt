Phase 144-6-R4 dependency-distance audit

変更なし。監査のみ。
既存の _argument_direct_dependency_indices() を使い、
各 argument conclusion から supporting block までの最短 dependency distance を表示する。

目的:
新しい探索機構や pi_6^3 固有条件を導入せずに、
deep supporting facts を generic に識別できるか確認する。

全体テストは実行しない。
