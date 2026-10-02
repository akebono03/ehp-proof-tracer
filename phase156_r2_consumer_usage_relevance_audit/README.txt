Phase156-R2 — consumer usage relevance audit

目的
====
Phase156-R1 で reference_side_overfull とされた 103 件を、
proof graph の consumer usage（実際の利用関係）だけで再分類する。

R2 は audit-only であり、production code の表示動作は変更しない。

対象
====
- n = 2..15
- k = 0..7
- depth = 2
- 112 groups
- R1 duplicate population = 117
- R1 reference_side_overfull population = 103

分類
====
1. boundary_direct_consumer
   選択 statement が、同じ Reference の外側にある proof step の
   direct premise（直接前提）として使われている。

2. internal_consumer_only
   選択 statement は同じ Reference ancestry 内だけで使われており、
   Reference 境界を直接越える consumer がない。

3. no_consumer
   選択 statement に outgoing proof edge がない。
   現在の fallback selection により表示されている候補。

4. aggregate_component_only
   Reference source は aggregate statement だが、
   現在の証明が実際に消費する一成分だけが選択・表示されている。

完了条件
========
- groups = 112
- exceptions = 0
- duplicate population = 117
- R1 overfull population = 103
- 103 件すべてが上記4分類のいずれかに入る
- focused classifier tests が PASS

R2 で変更しないもの
===================
- Reference theorem / lemma selection
- Reference statement selection
- Reference rendering
- proof body suppression
- proof data
- production code
- existing tests

次 Phase との境界
=================
Phase156-R3 で初めて、この監査結果を使って
minimal Reference statement selection（必要 statement の最小選択）
の一般規則を実装する。

実行
====
repository root で次を実行する。

powershell -ExecutionPolicy Bypass `
  -File ".\phase156_r2_consumer_usage_relevance_audit\run_phase156_r2_consumer_usage_relevance_audit.ps1"

repository-wide pytest は R2 では実行しない。
