# R52-R24 π3² 専用規則削除可否監査

判定: **DELETION_BLOCKED_BY_LEGACY_CONSUMERS**

## 現行依存

- legacy_bootstrap: 1 occurrences
- legacy_probe: 1 occurrences
- shared_search: 0 occurrences

共通探索での一般規則による証明と、旧経路の API 互換性は別の確認事項です。
旧経路の呼び出しが残る限り定義を削除しません。
